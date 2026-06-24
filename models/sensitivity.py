"""
Model 3: Sensitivity & Correlation Analysis
Dark Store Unit Economics - Indian Quick Commerce

Varies each key input variable independently by +/-20% from its base
value while holding all others constant. Measures the resulting change
in contribution margin per order. Results ranked by impact magnitude
and visualized as a tornado chart.

Also plots the delivery time vs retention curve to identify the
retention cliff.

Run: python models/sensitivity.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = "data/processed"
OUTPUT_FIG_DIR = "outputs/figures"
OUTPUT_TABLE_DIR = "outputs/tables"

os.makedirs(OUTPUT_FIG_DIR, exist_ok=True)
os.makedirs(OUTPUT_TABLE_DIR, exist_ok=True)


def load_assumptions(tier):
    path = os.path.join(DATA_DIR, f"{tier}_assumptions.csv")
    df = pd.read_csv(path)
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
# 1. Base case contribution margin (same formula as Model 1)
# ---------------------------------------------------------------

def contribution_margin(aov, take_rate_pct, delivery_fee, rider_payout,
                         picking_cost, monthly_rent, orders_per_day,
                         overhead, grocery_share, expiry_pct,
                         days_per_month=30):
    grocery_margin = 0.125
    non_grocery_margin = 0.425
    blended_margin = grocery_share * grocery_margin + (1 - grocery_share) * non_grocery_margin
    cogs = aov * (1 - blended_margin)
    expiry = cogs * (expiry_pct / 100)
    rent_per_order = monthly_rent / (orders_per_day * days_per_month)
    revenue = aov * (take_rate_pct / 100)
    return revenue + delivery_fee - rider_payout - picking_cost - rent_per_order - overhead - expiry


def get_base_inputs(assumptions):
    return dict(
        aov=float(assumptions.get("aov_assumption") or assumptions.get("aov_gross_assumption")),
        take_rate_pct=float(assumptions.get("take_rate_assumption", 18.0)),
        delivery_fee=float(assumptions.get("delivery_fee_per_order", 25)),
        rider_payout=float(assumptions.get("rider_payout_assumption") or assumptions.get("rider_payout_per_order", 50)),
        picking_cost=float(assumptions.get("picking_packing_cost_per_order", 15)),
        monthly_rent=float(assumptions.get("monthly_rent_assumption", 200000)),
        orders_per_day=float(assumptions.get("orders_per_day_assumption") or assumptions.get("orders_per_day_mature_store", 1000)),
        overhead=float(assumptions.get("overhead_allocation_per_order", 20)),
        grocery_share=float(assumptions.get("grocery_share_gov", 74.0)) / 100,
        expiry_pct=float(assumptions.get("expiry_provision_pct_cogs", 3.0)),
    )


# ---------------------------------------------------------------
# 2. Sensitivity sweep: vary each variable +/-20%
# ---------------------------------------------------------------

# Human-readable labels for the tornado chart
VARIABLE_LABELS = {
    "aov": "Average Order Value (AOV)",
    "take_rate_pct": "Platform Take Rate",
    "delivery_fee": "Delivery Fee Charged",
    "rider_payout": "Rider Payout per Order",
    "picking_cost": "Picking & Packing Cost",
    "monthly_rent": "Monthly Dark Store Rent",
    "orders_per_day": "Orders per Day (Volume)",
    "overhead": "Overhead per Order",
    "grocery_share": "Grocery Share of SKU Mix",
    "expiry_pct": "Inventory Expiry Provision",
}

DELTA = 0.20  # 20% variation


def run_sensitivity(assumptions, tier_name):
    base_inputs = get_base_inputs(assumptions)
    base_cm = contribution_margin(**base_inputs)

    records = []
    for var in VARIABLE_LABELS:
        inputs_up = base_inputs.copy()
        inputs_dn = base_inputs.copy()
        inputs_up[var] = base_inputs[var] * (1 + DELTA)
        inputs_dn[var] = base_inputs[var] * (1 - DELTA)

        cm_up = contribution_margin(**inputs_up)
        cm_dn = contribution_margin(**inputs_dn)

        swing_up = cm_up - base_cm
        swing_dn = cm_dn - base_cm
        total_swing = abs(swing_up) + abs(swing_dn)

        records.append({
            "tier": tier_name,
            "variable": var,
            "label": VARIABLE_LABELS[var],
            "base_cm": round(base_cm, 2),
            "cm_plus_20pct": round(cm_up, 2),
            "cm_minus_20pct": round(cm_dn, 2),
            "swing_plus": round(swing_up, 2),
            "swing_minus": round(swing_dn, 2),
            "total_swing": round(total_swing, 2),
        })

    df = pd.DataFrame(records).sort_values("total_swing", ascending=False)
    return df, base_cm


df_sens_t1, base_cm_t1 = run_sensitivity(tier1, "Tier-1")
df_sens_t2, base_cm_t2 = run_sensitivity(tier2, "Tier-2")

df_sens_all = pd.concat([df_sens_t1, df_sens_t2], ignore_index=True)
df_sens_all.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model3_sensitivity.csv"), index=False)

print("Tier-1 sensitivity ranking:")
print(df_sens_t1[["label", "swing_plus", "swing_minus", "total_swing"]].to_string(index=False))
print()
print("Tier-2 sensitivity ranking:")
print(df_sens_t2[["label", "swing_plus", "swing_minus", "total_swing"]].to_string(index=False))


# ---------------------------------------------------------------
# 3. Plot: Tornado charts
# ---------------------------------------------------------------

def plot_tornado(df, base_cm, tier_name, ax):
    df_plot = df.sort_values("total_swing", ascending=True)
    labels = df_plot["label"].tolist()
    swing_up = df_plot["swing_plus"].tolist()
    swing_dn = df_plot["swing_minus"].tolist()
    y_pos = range(len(labels))

    for i, (up, dn) in enumerate(zip(swing_up, swing_dn)):
        ax.barh(i, up, color="#16a34a", alpha=0.85, height=0.6)
        ax.barh(i, dn, color="#dc2626", alpha=0.85, height=0.6)

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Change in contribution margin per order (INR)")
    ax.set_title(f"{tier_name} — Sensitivity Tornado (±20% input variation)\nBase CM: ₹{base_cm:.2f}/order")
    ax.grid(axis="x", alpha=0.3)


fig, axes = plt.subplots(1, 2, figsize=(14, 7))
plot_tornado(df_sens_t1, base_cm_t1, "Tier-1", axes[0])
plot_tornado(df_sens_t2, base_cm_t2, "Tier-2", axes[1])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model3_tornado_chart.png"), dpi=150)
plt.close()


# ---------------------------------------------------------------
# 4. Retention cliff: delivery time vs customer retention
#
# No source gave us an exact curve, so we model a plausible S-curve
# decay: retention stays high until ~15 minutes, then drops sharply.
# This shape is consistent with qualitative evidence that platforms
# switched from promising 10 mins to 13-15 mins as their standard.
# Documented as a modelling assumption, not measured data.
# ---------------------------------------------------------------

delivery_times = np.linspace(5, 45, 200)

def retention_curve(t, cliff=15, steepness=0.4):
    """
    Logistic decay: retention is high below the cliff, drops sharply around it.
    cliff: the delivery time (minutes) where retention starts to fall sharply.
    steepness: controls how fast the drop is.
    """
    return 1 / (1 + np.exp(steepness * (t - cliff)))

retention = retention_curve(delivery_times)

plt.figure(figsize=(9, 5))
plt.plot(delivery_times, retention * 100, color="#2563eb", linewidth=2)
plt.axvline(13, color="#16a34a", linestyle="--", linewidth=1.5, label="Instamart avg (13 min)")
plt.axvline(15, color="#f59e0b", linestyle="--", linewidth=1.5, label="Retention cliff (~15 min)")
plt.axvline(20, color="#dc2626", linestyle="--", linewidth=1.5, label="Tier-2 estimated avg (20 min)")
plt.xlabel("Delivery time (minutes)")
plt.ylabel("Relative customer retention (%)")
plt.title("Delivery Time vs Customer Retention\n(modelled S-curve — shape is a documented assumption)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model3_retention_cliff.png"), dpi=150)
plt.close()

# Save retention curve as table
df_retention = pd.DataFrame({
    "delivery_time_minutes": np.round(delivery_times, 1),
    "relative_retention_pct": np.round(retention * 100, 2),
})
df_retention.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model3_retention_curve.csv"), index=False)


print("\nModel 3 complete.")
print(f"Tables saved to {OUTPUT_TABLE_DIR}/")
print(f"Figures saved to {OUTPUT_FIG_DIR}/")