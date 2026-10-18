import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# VISUAL EXECUTIVE MANAGEMENT DASHBOARD
# ========================================

FILE_NAME = "sales_forecasting_sample_data.csv"
AS_OF_MONTH = "Sep-26"

month_order = [
    "Apr-26", "May-26", "Jun-26", "Jul-26",
    "Aug-26", "Sep-26", "Oct-26", "Nov-26",
    "Dec-26", "Jan-27", "Feb-27", "Mar-27"
]

# ----------------------------------------
# Load Data
# ----------------------------------------

df = pd.read_csv(FILE_NAME)

df["Month"] = pd.Categorical(
    df["Month"],
    categories=month_order,
    ordered=True
)

as_of_index = month_order.index(AS_OF_MONTH)

months_completed = as_of_index + 1
months_remaining = len(month_order) - months_completed

ytd_df = df[
    df["Month"].cat.codes <= as_of_index
].copy()

# ----------------------------------------
# Revenue Metrics
# ----------------------------------------

ytd_sales = ytd_df["Current_Sales_Lakh"].sum()
ytd_target = ytd_df["Target_Lakh"].sum()

ytd_achievement = (
    ytd_sales / ytd_target * 100
)

monthly_run_rate = (
    ytd_sales / months_completed
)

full_year_target = df["Target_Lakh"].sum()

projected_revenue = (
    monthly_run_rate * len(month_order)
)

projected_achievement = (
    projected_revenue / full_year_target * 100
)

projected_gap = (
    full_year_target - projected_revenue
)

required_remaining_sales = (
    full_year_target - ytd_sales
)

required_monthly_run_rate = (
    required_remaining_sales / months_remaining
)

run_rate_uplift = (
    required_monthly_run_rate / monthly_run_rate - 1
) * 100


# ========================================
# REGION ANALYSIS
# ========================================

region = (
    ytd_df
    .groupby("Region", observed=True)
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

region["Achievement_%"] = (
    region["Sales_Lakh"]
    / region["Target_Lakh"] * 100
)

region["Gap_Lakh"] = (
    region["Target_Lakh"]
    - region["Sales_Lakh"]
)


# ========================================
# CHANNEL ANALYSIS
# ========================================

channel = (
    ytd_df
    .groupby("Channel", observed=True)
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

channel["Achievement_%"] = (
    channel["Sales_Lakh"]
    / channel["Target_Lakh"] * 100
)

channel["Gap_Lakh"] = (
    channel["Target_Lakh"]
    - channel["Sales_Lakh"]
)


# ========================================
# SCENARIO ANALYSIS
# ========================================

gt_ytd = ytd_df[
    ytd_df["Channel"] == "GT"
]["Current_Sales_Lakh"].sum()

west_ytd = ytd_df[
    ytd_df["Region"] == "West"
]["Current_Sales_Lakh"].sum()

gt_monthly = gt_ytd / months_completed
west_monthly = west_ytd / months_completed

scenarios = {
    "Base": (0, 0),
    "Upside": (10, 10),
    "Stretch": (15, 15)
}

scenario_data = []

for name, (gt_improvement, west_improvement) in scenarios.items():

    incremental_revenue = (
        gt_monthly
        * months_remaining
        * gt_improvement / 100
        +
        west_monthly
        * months_remaining
        * west_improvement / 100
    )

    scenario_revenue = (
        projected_revenue + incremental_revenue
    )

    scenario_achievement = (
        scenario_revenue / full_year_target * 100
    )

    scenario_gap = max(
        full_year_target - scenario_revenue,
        0
    )

    scenario_data.append({
        "Scenario": name,
        "Projected Revenue": scenario_revenue,
        "Achievement": scenario_achievement,
        "Gap": scenario_gap
    })

scenario_df = pd.DataFrame(scenario_data)


# ========================================
# DASHBOARD HEADER
# ========================================

print("=" * 70)
print("             EXECUTIVE MANAGEMENT DASHBOARD")
print("=" * 70)

print(f"\nAs of Month: {AS_OF_MONTH}")

print("\nKEY MANAGEMENT METRICS")
print("-" * 70)

print(f"YTD Sales              : ₹{ytd_sales:.2f} Lakh")
print(f"YTD Achievement        : {ytd_achievement:.1f}%")
print(f"FY Target              : ₹{full_year_target:.2f} Lakh")
print(f"FY Forecast            : ₹{projected_revenue:.2f} Lakh")
print(f"Projected Gap          : ₹{projected_gap:.2f} Lakh")
print(f"Current Run Rate       : ₹{monthly_run_rate:.2f} Lakh")
print(f"Required Run Rate      : ₹{required_monthly_run_rate:.2f} Lakh")
print(f"Required Run-Rate Uplift: {run_rate_uplift:.1f}%")

print("\n" + "=" * 70)


# ========================================
# CHART 1 — REVENUE HEALTH
# ========================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["YTD Sales", "YTD Target"],
    [ytd_sales, ytd_target]
)

plt.title("Revenue Health — YTD")
plt.ylabel("₹ Lakh")
plt.tight_layout()
plt.show()


# ========================================
# CHART 2 — REGION PERFORMANCE
# ========================================

plt.figure(figsize=(8, 5))

plt.bar(
    region["Region"],
    region["Achievement_%"]
)

plt.axhline(
    100,
    linestyle="--",
    linewidth=1
)

plt.title("Region Performance — YTD Achievement")
plt.ylabel("Achievement %")
plt.ylim(0, max(110, region["Achievement_%"].max() + 10))

plt.tight_layout()
plt.show()


# ========================================
# CHART 3 — CHANNEL PERFORMANCE
# ========================================

plt.figure(figsize=(8, 5))

plt.bar(
    channel["Channel"],
    channel["Achievement_%"]
)

plt.axhline(
    100,
    linestyle="--",
    linewidth=1
)

plt.title("Channel Performance — YTD Achievement")
plt.ylabel("Achievement %")
plt.ylim(0, max(110, channel["Achievement_%"].max() + 10))

plt.tight_layout()
plt.show()


# ========================================
# CHART 4 — SCENARIO PLANNING
# ========================================

plt.figure(figsize=(8, 5))

plt.bar(
    scenario_df["Scenario"],
    scenario_df["Projected Revenue"]
)

plt.axhline(
    full_year_target,
    linestyle="--",
    linewidth=1
)

plt.title("Scenario Planning — Projected Revenue")
plt.ylabel("₹ Lakh")

plt.tight_layout()
plt.show()


# ========================================
# EXECUTIVE ACTION PANEL
# ========================================

primary_channel = (
    channel
    .sort_values("Gap_Lakh", ascending=False)
    .iloc[0]
)

primary_region = (
    region
    .sort_values("Gap_Lakh", ascending=False)
    .iloc[0]
)

print("\n" + "=" * 70)
print("EXECUTIVE ACTION PANEL")
print("=" * 70)

print(
    f"\n1. Channel Priority : {primary_channel['Channel']}"
    f" | Gap ₹{primary_channel['Gap_Lakh']:.2f}L"
)

print(
    f"2. Region Priority  : {primary_region['Region']}"
    f" | Gap ₹{primary_region['Gap_Lakh']:.2f}L"
)

print(
    f"3. Revenue Challenge: Increase monthly run rate "
    f"by {run_rate_uplift:.1f}%"
)

print(
    "4. Scenario Focus    : Track GT and West interventions "
    "against incremental revenue delivered."
)

print("\n" + "=" * 70)
