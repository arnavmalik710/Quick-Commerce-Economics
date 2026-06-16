"""
Model 1: Unit Economics P&L Waterfall
Dark Store Unit Economics - Indian Quick Commerce

Calculates contribution margin per order for Tier-1 and Tier-2 dark stores
across a range of AOV and order-volume scenarios, and identifies the
breakeven order volume per day.

Run: python models/unit_economics.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------
# 1. Load assumptions
# ---------------------------------------------------------------

DATA_DIR = "data/processed"
OUTPUT_FIG_DIR = "outputs/figures"
OUTPUT_TABLE_DIR = "outputs/tables"

os.makedirs(OUTPUT_FIG_DIR, exist_ok=True)
os.makedirs(OUTPUT_TABLE_DIR, exist_ok=True)


def load_assumptions(tier):
    """Load a tier's assumptions CSV into a simple dict of {parameter: value}."""
    path = os.path.join(DATA_DIR, f"{tier}_assumptions.csv")
    df = pd.read_csv(path)
    # value column may contain numbers or strings (e.g. "Q3FY26") - coerce numerics
    lookup = {}
    for _, row in df.iterrows():
        val = row["value"]
        try:
            val = float(val)
        except (ValueError, TypeError):
            pass
        lookup[row["parameter"]] = val
    return lookup


tier1 = load_assumptions("tier1")
tier2 = load_assumptions("tier2")


# ---------------------------------------------------------------
# 2. Core contribution margin function
# ---------------------------------------------------------------

def contribution_margin_per_order(aov, take_rate_pct, delivery_fee, rider_payout,
                                    picking_cost, monthly_rent, orders_per_day,
                                    overhead, expiry_pct, grocery_share, days_per_month=30):
    """
    CM = (AOV x Take Rate) + Delivery Fee - Rider Payout - Picking Cost
         - Rent per Order - Overhead - Expiry Provision

    Expiry provision is modelled as a percentage of COGS. COGS is approximated
    as AOV x (1 - blended margin), where blended margin depends on grocery share.
    """
    grocery_margin = 0.125
    non_grocery_margin = 0.425
    blended_margin = grocery_share * grocery_margin + (1 - grocery_share) * non_grocery_margin
    cogs = aov * (1 - blended_margin)
    expiry_provision = cogs * (expiry_pct / 100)

    rent_per_order = monthly_rent / (orders_per_day * days_per_month)

    revenue_from_take_rate = aov * (take_rate_pct / 100)
    cm = (revenue_from_take_rate + delivery_fee
          - rider_payout - picking_cost - rent_per_order
          - overhead - expiry_provision)

    return cm, rent_per_order, expiry_provision


def build_scenario(tier_name, assumptions, orders_per_day_range, aov_override=None):
    """Run the CM calculation across a range of orders/day for a fixed AOV scenario."""

    aov = aov_override if aov_override is not None else (
        assumptions.get("aov_assumption") or assumptions.get("aov_gross_assumption")
    )
    take_rate = assumptions.get("take_rate_assumption", 18.0)
    delivery_fee = assumptions.get("delivery_fee_per_order", 25)
    rider_payout = assumptions.get("rider_payout_assumption") or assumptions.get("rider_payout_per_order", 50)
    picking_cost = assumptions.get("picking_packing_cost_per_order", 15)
    monthly_rent = assumptions.get("monthly_rent_assumption", 200000)
    overhead = assumptions.get("overhead_allocation_per_order", 20)
    expiry_pct = assumptions.get("expiry_provision_pct_cogs", 3.0)
    grocery_share = assumptions.get("grocery_share_gov", 74.0) / 100

    records = []
    for opd in orders_per_day_range:
        cm, rent_per_order, expiry = contribution_margin_per_order(
            aov, take_rate, delivery_fee, rider_payout, picking_cost,
            monthly_rent, opd, overhead, expiry_pct, grocery_share
        )
        monthly_fixed_cost = monthly_rent  # rent is the main pure fixed cost isolated here
        records.append({
            "tier": tier_name,
            "orders_per_day": opd,
            "aov": aov,
            "contribution_margin_per_order": round(cm, 2),
            "rent_per_order": round(rent_per_order, 2),
            "expiry_provision_per_order": round(expiry, 2),
            "daily_contribution_total": round(cm * opd, 2),
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------
# 3. Run scenarios: orders/day sweep for Tier-1 and Tier-2
# ---------------------------------------------------------------

orders_range = np.arange(200, 2001, 50)

df_tier1 = build_scenario("Tier-1", tier1, orders_range)
df_tier2 = build_scenario("Tier-2", tier2, orders_range)

df_combined = pd.concat([df_tier1, df_tier2], ignore_index=True)
df_combined.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model1_cm_vs_orders.csv"), index=False)


# ---------------------------------------------------------------
# 4. Find breakeven order volume (where CM per order = 0)
# ---------------------------------------------------------------

def find_breakeven(df):
    """Find approximate order volume where contribution margin per order crosses zero."""
    df_sorted = df.sort_values("orders_per_day")
    crossing = df_sorted[df_sorted["contribution_margin_per_order"] >= 0]
    if len(crossing) == 0:
        return None
    return crossing.iloc[0]["orders_per_day"]


breakeven_t1 = find_breakeven(df_tier1)
breakeven_t2 = find_breakeven(df_tier2)

print(f"Tier-1 breakeven order volume (CM >= 0): {breakeven_t1} orders/day")
print(f"Tier-2 breakeven order volume (CM >= 0): {breakeven_t2} orders/day")


# ---------------------------------------------------------------
# 5. SKU mix sensitivity: grocery-only vs mixed vs non-grocery-led
# ---------------------------------------------------------------

def sku_mix_scenarios(tier_name, assumptions, fixed_opd):
    """
    SKU mix affects two things, not one:
    1. The expiry provision (via blended margin / COGS) - captured already
    2. The AOV itself - non-grocery baskets (electronics, beauty) cost more
       per item than grocery baskets. This is the dominant real-world lever
       and was missing from the first pass of this model.

    AOV uplift is approximated linearly: a fully non-grocery basket is
    assumed to carry ~40% higher AOV than a fully grocery basket.
    """
    base_aov = assumptions.get("aov_assumption") or assumptions.get("aov_gross_assumption")
    take_rate = assumptions.get("take_rate_assumption", 18.0)
    delivery_fee = assumptions.get("delivery_fee_per_order", 25)
    rider_payout = assumptions.get("rider_payout_assumption") or assumptions.get("rider_payout_per_order", 50)
    picking_cost = assumptions.get("picking_packing_cost_per_order", 15)
    monthly_rent = assumptions.get("monthly_rent_assumption", 200000)
    overhead = assumptions.get("overhead_allocation_per_order", 20)
    expiry_pct = assumptions.get("expiry_provision_pct_cogs", 3.0)

    aov_uplift_max = 0.40  # 100% non-grocery basket carries 40% higher AOV

    scenarios = {
        "Grocery-only (0% non-grocery)": 1.0,
        "Current mix (74% grocery)": 0.74,
        "Mixed (50/50)": 0.50,
        "Non-grocery-led (20% grocery)": 0.20,
    }

    records = []
    for label, grocery_share in scenarios.items():
        non_grocery_share = 1 - grocery_share
        scenario_aov = base_aov * (1 + non_grocery_share * aov_uplift_max)

        cm, _, _ = contribution_margin_per_order(
            scenario_aov, take_rate, delivery_fee, rider_payout, picking_cost,
            monthly_rent, fixed_opd, overhead, expiry_pct, grocery_share
        )
        records.append({
            "tier": tier_name,
            "scenario": label,
            "grocery_share_pct": grocery_share * 100,
            "scenario_aov": round(scenario_aov, 2),
            "contribution_margin_per_order": round(cm, 2),
        })
    return pd.DataFrame(records)


df_sku_t1 = sku_mix_scenarios("Tier-1", tier1, fixed_opd=1300)
df_sku_t2 = sku_mix_scenarios("Tier-2", tier2, fixed_opd=800)
df_sku_combined = pd.concat([df_sku_t1, df_sku_t2], ignore_index=True)
df_sku_combined.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model1_sku_mix_scenarios.csv"), index=False)


# ---------------------------------------------------------------
# 6. Plot: Contribution margin vs orders/day (breakeven chart)
# ---------------------------------------------------------------

plt.figure(figsize=(9, 6))
plt.plot(df_tier1["orders_per_day"], df_tier1["contribution_margin_per_order"],
         label="Tier-1", linewidth=2, color="#2563eb")
plt.plot(df_tier2["orders_per_day"], df_tier2["contribution_margin_per_order"],
         label="Tier-2", linewidth=2, color="#dc2626")
plt.axhline(0, color="gray", linestyle="--", linewidth=1)
plt.xlabel("Orders per day")
plt.ylabel("Contribution margin per order (INR)")
plt.title("Breakeven Analysis: Contribution Margin vs Order Volume")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model1_breakeven_chart.png"), dpi=150)
plt.close()


# ---------------------------------------------------------------
# 7. Plot: SKU mix waterfall
# ---------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=False)

for ax, df_sku, tier_label in zip(axes, [df_sku_t1, df_sku_t2], ["Tier-1", "Tier-2"]):
    colors = ["#dc2626" if v < 0 else "#16a34a" for v in df_sku["contribution_margin_per_order"]]
    ax.barh(df_sku["scenario"], df_sku["contribution_margin_per_order"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"{tier_label} — SKU Mix Impact on CM/order")
    ax.set_xlabel("Contribution margin per order (INR)")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model1_sku_mix_waterfall.png"), dpi=150)
plt.close()


print("\nModel 1 complete.")
print(f"Tables saved to {OUTPUT_TABLE_DIR}/")
print(f"Figures saved to {OUTPUT_FIG_DIR}/")
