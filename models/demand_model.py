"""
Model 2: Poisson Demand Modeling
Dark Store Unit Economics - Indian Quick Commerce

Models intraday order arrival patterns using a Poisson distribution,
compares against fixed staffing capacity, and quantifies idle-time cost
and capacity crash probability across a 24-hour day.

IMPORTANT ASSUMPTION FLAGGED:
The hourly distribution SHAPE (which hours are busiest) is constructed
from the qualitative peak-window description in industry sources
(morning rush 7-11am, evening rush 6-10pm). No source provided an actual
hour-by-hour order count. The daily TOTAL (orders/day) is sourced from
the assumptions CSV; the hourly split is a documented modelling choice,
not measured data. This is disclosed in the appendix.

Run: python models/demand_model.py
"""

import pandas as pd
import numpy as np
from scipy.stats import poisson
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
# 1. Build the hourly lambda curve from a documented weight shape
# ---------------------------------------------------------------

# Relative intensity weights by hour, reflecting the qualitative
# morning rush (7-11am) / evening rush (6-10pm) pattern described
# in industry sources. This shape is a modelling assumption.
HOURLY_WEIGHTS = {
    0: 0.10, 1: 0.05, 2: 0.02, 3: 0.02, 4: 0.05, 5: 0.20,
    6: 0.50, 7: 1.50, 8: 2.00, 9: 1.80, 10: 1.30, 11: 1.00,
    12: 1.10, 13: 1.00, 14: 0.90, 15: 0.90, 16: 1.00, 17: 1.30,
    18: 1.80, 19: 2.20, 20: 2.00, 21: 1.50, 22: 0.80, 23: 0.30,
}


def build_hourly_lambda(daily_orders):
    """Distribute a known daily order total across 24 hours using the weight shape."""
    total_weight = sum(HOURLY_WEIGHTS.values())
    return {h: daily_orders * w / total_weight for h, w in HOURLY_WEIGHTS.items()}


# ---------------------------------------------------------------
# 2. Staffing capacity and crash/idle analysis
# ---------------------------------------------------------------

def analyse_staffing(daily_orders, picker_throughput, fixed_staff_count,
                       idle_cost_per_staff_hour, crash_cost_per_order=15):
    """
    For each hour, compare expected demand (lambda) against fixed staff
    capacity. Quantify:
      - idle staff-hours and their cost (when capacity > demand)
      - expected crashed/delayed orders and their cost (when demand > capacity)
      - P(crash) using the Poisson CDF: probability that actual orders in
        that hour exceed capacity, given lambda.
    """
    lambdas = build_hourly_lambda(daily_orders)
    capacity_per_hour = fixed_staff_count * picker_throughput

    records = []
    for hour, lam in lambdas.items():
        # Probability that actual demand exceeds capacity in this hour
        # P(X > capacity) = 1 - P(X <= capacity)
        p_crash = 1 - poisson.cdf(capacity_per_hour, lam)

        expected_orders = lam
        excess_orders = max(0, expected_orders - capacity_per_hour)
        idle_capacity = max(0, capacity_per_hour - expected_orders)

        # Idle cost: capacity sitting unused, valued at staff cost per hour
        idle_staff_hours = idle_capacity / picker_throughput if picker_throughput > 0 else 0
        idle_cost = idle_staff_hours * idle_cost_per_staff_hour

        # Crash cost: excess orders are either delayed or lost - apply a
        # flat estimated cost per excess order (delay penalty / refund risk)
        crash_cost = excess_orders * crash_cost_per_order

        records.append({
            "hour": hour,
            "lambda_expected_orders": round(lam, 1),
            "capacity_per_hour": capacity_per_hour,
            "excess_orders": round(excess_orders, 1),
            "idle_capacity_orders": round(idle_capacity, 1),
            "p_crash": round(p_crash, 4),
            "idle_cost_inr": round(idle_cost, 2),
            "crash_cost_inr": round(crash_cost, 2),
        })
    return pd.DataFrame(records)


def run_tier_analysis(tier_name, assumptions):
    daily_orders = assumptions.get("orders_per_day_assumption") or assumptions.get("orders_per_day_mature_store", 1000)
    picker_throughput = assumptions.get("picker_throughput_per_hour", 12)

    # Fixed staff count: derive from project charter base staffing assumption.
    # Tier-1: 8-12 base -> use 10. Tier-2: 4-6 base -> use 5.
    fixed_staff_count = 10 if tier_name == "Tier-1" else 5

    # Idle cost per staff hour: derive from rider/picker monthly earnings
    # assumption, converted to an hourly rate (26 days x 8 hours/day basis)
    monthly_earnings = assumptions.get("rider_monthly_earnings_consistent") or assumptions.get("rider_monthly_earnings_assumption", 20000)
    idle_cost_per_staff_hour = monthly_earnings / (26 * 8)

    df = analyse_staffing(daily_orders, picker_throughput, fixed_staff_count, idle_cost_per_staff_hour)
    df["tier"] = tier_name
    df["fixed_staff_count"] = fixed_staff_count
    df["idle_cost_per_staff_hour"] = round(idle_cost_per_staff_hour, 2)
    return df


df_tier1 = run_tier_analysis("Tier-1", tier1)
df_tier2 = run_tier_analysis("Tier-2", tier2)

df_combined = pd.concat([df_tier1, df_tier2], ignore_index=True)
df_combined.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model2_hourly_staffing.csv"), index=False)


# ---------------------------------------------------------------
# 3. Daily summary: total idle cost vs total crash cost
# ---------------------------------------------------------------

def daily_summary(df, tier_name):
    total_idle_cost = df["idle_cost_inr"].sum()
    total_crash_cost = df["crash_cost_inr"].sum()
    hours_with_crash_risk = (df["p_crash"] > 0.5).sum()
    hours_idle = (df["idle_capacity_orders"] > 0).sum()
    return {
        "tier": tier_name,
        "total_daily_idle_cost_inr": round(total_idle_cost, 2),
        "total_daily_crash_cost_inr": round(total_crash_cost, 2),
        "total_daily_waste_inr": round(total_idle_cost + total_crash_cost, 2),
        "hours_with_high_crash_risk": int(hours_with_crash_risk),
        "hours_with_idle_capacity": int(hours_idle),
    }


summary = pd.DataFrame([
    daily_summary(df_tier1, "Tier-1"),
    daily_summary(df_tier2, "Tier-2"),
])
summary.to_csv(os.path.join(OUTPUT_TABLE_DIR, "model2_daily_summary.csv"), index=False)

print(summary.to_string(index=False))


# ---------------------------------------------------------------
# 4. Plot: Intraday demand curve vs fixed capacity
# ---------------------------------------------------------------

fig, axes = plt.subplots(2, 1, figsize=(11, 9), sharex=True)

for ax, df, tier_name in zip(axes, [df_tier1, df_tier2], ["Tier-1", "Tier-2"]):
    capacity = df["capacity_per_hour"].iloc[0]
    ax.plot(df["hour"], df["lambda_expected_orders"], label="Expected demand (lambda)",
            color="#2563eb", linewidth=2, marker="o", markersize=3)
    ax.axhline(capacity, color="#dc2626", linestyle="--", linewidth=2, label=f"Fixed capacity ({capacity}/hr)")
    ax.fill_between(df["hour"], df["lambda_expected_orders"], capacity,
                     where=(df["lambda_expected_orders"] > capacity),
                     color="#dc2626", alpha=0.2, label="Capacity crash zone")
    ax.fill_between(df["hour"], df["lambda_expected_orders"], capacity,
                     where=(df["lambda_expected_orders"] <= capacity),
                     color="#16a34a", alpha=0.15, label="Idle capacity zone")
    ax.set_title(f"{tier_name} — Intraday Demand vs Fixed Staffing Capacity")
    ax.set_ylabel("Orders per hour")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(alpha=0.3)

axes[-1].set_xlabel("Hour of day")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model2_demand_vs_capacity.png"), dpi=150)
plt.close()


# ---------------------------------------------------------------
# 5. Plot: Crash probability by hour
# ---------------------------------------------------------------

plt.figure(figsize=(10, 5))
plt.plot(df_tier1["hour"], df_tier1["p_crash"], label="Tier-1", linewidth=2, color="#2563eb", marker="o", markersize=3)
plt.plot(df_tier2["hour"], df_tier2["p_crash"], label="Tier-2", linewidth=2, color="#dc2626", marker="o", markersize=3)
plt.xlabel("Hour of day")
plt.ylabel("P(demand exceeds capacity)")
plt.title("Capacity Crash Probability by Hour")
plt.xticks(range(0, 24, 2))
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIG_DIR, "model2_crash_probability.png"), dpi=150)
plt.close()


print("\nModel 2 complete.")
print(f"Tables saved to {OUTPUT_TABLE_DIR}/")
print(f"Figures saved to {OUTPUT_FIG_DIR}/")