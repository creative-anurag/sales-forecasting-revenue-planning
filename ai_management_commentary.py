import pandas as pd

# ========================================
# AI MANAGEMENT COMMENTARY ENGINE
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


# ----------------------------------------
# Management Status
# ----------------------------------------

if projected_achievement >= 100:
    status = "ON TRACK"
elif projected_achievement >= 90:
    status = "WATCH"
else:
    status = "ACTION REQUIRED"


# ----------------------------------------
# Region Analysis
# ----------------------------------------

region = (
    ytd_df
    .groupby("Region", observed=True)
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

region["Gap_Lakh"] = (
    region["Target_Lakh"] -
    region["Sales_Lakh"]
)

primary_region = (
    region
    .sort_values("Gap_Lakh", ascending=False)
    .iloc[0]
)


# ----------------------------------------
# Channel Analysis
# ----------------------------------------

channel = (
    ytd_df
    .groupby("Channel", observed=True)
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

channel["Gap_Lakh"] = (
    channel["Target_Lakh"] -
    channel["Sales_Lakh"]
)

primary_channel = (
    channel
    .sort_values("Gap_Lakh", ascending=False)
    .iloc[0]
)


# ----------------------------------------
# Scenario Analysis
# ----------------------------------------

gt_ytd = ytd_df[
    ytd_df["Channel"] == "GT"
]["Current_Sales_Lakh"].sum()

west_ytd = ytd_df[
    ytd_df["Region"] == "West"
]["Current_Sales_Lakh"].sum()

gt_monthly = gt_ytd / months_completed
west_monthly = west_ytd / months_completed

stretch_incremental = (
    gt_monthly * months_remaining * 0.15
    +
    west_monthly * months_remaining * 0.15
)

stretch_revenue = (
    projected_revenue + stretch_incremental
)

stretch_achievement = (
    stretch_revenue / full_year_target * 100
)

stretch_gap = max(
    full_year_target - stretch_revenue,
    0
)

stretch_gap_closed = (
    stretch_incremental / projected_gap * 100
    if projected_gap > 0
    else 0
)


# ========================================
# MANAGEMENT COMMENTARY
# ========================================

print("=" * 70)
print("             AI MANAGEMENT COMMENTARY ENGINE")
print("=" * 70)

print(f"\nAs of Month: {AS_OF_MONTH}")
print(f"Management Status: {status}")

print("\n--- EXECUTIVE OUTLOOK ---")

print(
    f"Business is currently tracking at "
    f"{ytd_achievement:.1f}% YTD achievement."
)

print(
    f"The current run rate of ₹{monthly_run_rate:.2f}L "
    f"projects full-year revenue of "
    f"₹{projected_revenue:.2f}L."
)

print(
    f"This creates a projected annual gap of "
    f"₹{projected_gap:.2f}L against the "
    f"₹{full_year_target:.2f}L target."
)


print("\n--- KEY BUSINESS RISK ---")

print(
    f"The business needs to increase its monthly "
    f"run rate from ₹{monthly_run_rate:.2f}L to "
    f"₹{required_monthly_run_rate:.2f}L."
)

print(
    f"This represents a required uplift of "
    f"approximately {run_rate_uplift:.1f}%."
)


print("\n--- PRIORITY AREAS ---")

print(
    f"{primary_channel['Channel']} is the highest-priority "
    f"channel with a YTD gap of "
    f"₹{primary_channel['Gap_Lakh']:.2f}L."
)

print(
    f"{primary_region['Region']} is the highest-priority "
    f"region with a YTD gap of "
    f"₹{primary_region['Gap_Lakh']:.2f}L."
)


print("\n--- SCENARIO INSIGHT ---")

print(
    f"Under the Stretch scenario, with 15% improvement "
    f"in both GT and West, projected revenue increases "
    f"to ₹{stretch_revenue:.2f}L."
)

print(
    f"This represents {stretch_achievement:.1f}% achievement "
    f"and closes approximately "
    f"{stretch_gap_closed:.1f}% of the projected gap."
)

print(
    f"Even under the Stretch scenario, approximately "
    f"₹{stretch_gap:.2f}L remains to be closed."
)


print("\n--- MANAGEMENT RECOMMENDATION ---")

print(
    "1. Focus immediate commercial intervention on GT "
    "and West."
)

print(
    f"2. Raise the monthly run rate by at least "
    f"{run_rate_uplift:.1f}%."
)

print(
    "3. Track incremental revenue generated from each "
    "commercial intervention."
)

print(
    "4. Use the Stretch scenario as the minimum "
    "recovery benchmark rather than the final objective."
)

print("\n" + "=" * 70)
