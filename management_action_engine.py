import pandas as pd

# Load sales data
df = pd.read_csv("sales_forecasting_sample_data.csv")

# -----------------------------------------
# FORECAST PERIOD
# -----------------------------------------

AS_OF_MONTH = "Sep-26"

month_order = [
    "Apr-26", "May-26", "Jun-26", "Jul-26",
    "Aug-26", "Sep-26", "Oct-26", "Nov-26",
    "Dec-26", "Jan-27", "Feb-27", "Mar-27"
]

months_elapsed = month_order.index(AS_OF_MONTH) + 1
months_remaining = 12 - months_elapsed

# YTD data
ytd_df = df[
    df["Month"].isin(month_order[:months_elapsed])
].copy()

# -----------------------------------------
# OVERALL PERFORMANCE
# -----------------------------------------

ytd_sales = ytd_df["Current_Sales_Lakh"].sum()
ytd_target = ytd_df["Target_Lakh"].sum()

ytd_achievement = (
    ytd_sales / ytd_target
) * 100

monthly_run_rate = (
    ytd_sales / months_elapsed
)

full_year_target = df["Target_Lakh"].sum()

projected_revenue = (
    monthly_run_rate * 12
)

projected_achievement = (
    projected_revenue / full_year_target
) * 100

projected_gap = (
    full_year_target - projected_revenue
)

required_remaining_sales = (
    full_year_target - ytd_sales
)

required_monthly_run_rate = (
    required_remaining_sales / months_remaining
)

run_rate_improvement = (
    (required_monthly_run_rate / monthly_run_rate) - 1
) * 100

# -----------------------------------------
# REGION PRIORITY
# -----------------------------------------

region_analysis = (
    ytd_df.groupby("Region")
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

region_analysis["Gap_Lakh"] = (
    region_analysis["Target_Lakh"]
    - region_analysis["Sales_Lakh"]
)

region_analysis["Achievement_%"] = (
    region_analysis["Sales_Lakh"]
    / region_analysis["Target_Lakh"]
) * 100

primary_region = region_analysis.loc[
    region_analysis["Gap_Lakh"].idxmax()
]

# -----------------------------------------
# CHANNEL PRIORITY
# -----------------------------------------

channel_analysis = (
    ytd_df.groupby("Channel")
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum")
    )
    .reset_index()
)

channel_analysis["Gap_Lakh"] = (
    channel_analysis["Target_Lakh"]
    - channel_analysis["Sales_Lakh"]
)

channel_analysis["Achievement_%"] = (
    channel_analysis["Sales_Lakh"]
    / channel_analysis["Target_Lakh"]
) * 100

primary_channel = channel_analysis.loc[
    channel_analysis["Gap_Lakh"].idxmax()
]

# -----------------------------------------
# MANAGEMENT STATUS
# -----------------------------------------

if projected_achievement >= 100:
    overall_status = "ON TRACK"
elif projected_achievement >= 90:
    overall_status = "WATCH"
else:
    overall_status = "ACTION REQUIRED"

# -----------------------------------------
# MANAGEMENT ACTIONS
# -----------------------------------------

if overall_status == "ON TRACK":
    action_1 = "Maintain current sales velocity"
elif overall_status == "WATCH":
    action_1 = "Accelerate revenue conversion and close the projected gap"
else:
    action_1 = "Immediate revenue recovery plan required"

action_2 = (
    f"Prioritize {primary_channel['Channel']} channel "
    f"with ₹{primary_channel['Gap_Lakh']:.1f}L YTD gap"
)

action_3 = (
    f"Prioritize {primary_region['Region']} region "
    f"with ₹{primary_region['Gap_Lakh']:.1f}L YTD gap"
)

action_4 = (
    f"Increase monthly run rate by approximately "
    f"{run_rate_improvement:.1f}% to achieve the annual target"
)

# -----------------------------------------
# MANAGEMENT OUTPUT
# -----------------------------------------

print("\n========================================")
print("MANAGEMENT ACTION ENGINE")
print("========================================\n")

print(f"As of Month: {AS_OF_MONTH}")
print(f"Overall Status: {overall_status}")

print("\n--- Performance Outlook ---")
print(f"YTD Sales: ₹{ytd_sales:.2f} Lakh")
print(f"YTD Achievement: {ytd_achievement:.1f}%")
print(f"Current Monthly Run Rate: ₹{monthly_run_rate:.2f} Lakh")
print(f"Projected Full-Year Revenue: ₹{projected_revenue:.2f} Lakh")
print(f"Projected Achievement: {projected_achievement:.1f}%")
print(f"Projected Gap: ₹{projected_gap:.2f} Lakh")

print("\n--- Management Priorities ---")
print(f"1. {action_1}")
print(f"2. {action_2}")
print(f"3. {action_3}")
print(f"4. {action_4}")

print("\n--- Required Revenue Run Rate ---")
print(
    f"Required Remaining Monthly Run Rate: "
    f"₹{required_monthly_run_rate:.2f} Lakh"
)

print(
    f"Current Monthly Run Rate: "
    f"₹{monthly_run_rate:.2f} Lakh"
)
