import pandas as pd

# ========================================
# EXECUTIVE MANAGEMENT DASHBOARD
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

# ----------------------------------------
# YTD Calculation
# ----------------------------------------

as_of_index = month_order.index(AS_OF_MONTH)

months_completed = as_of_index + 1
months_remaining = len(month_order) - months_completed

ytd_df = df[
    df["Month"].cat.codes <= as_of_index
].copy()

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
    management_status = "ON TRACK"
elif projected_achievement >= 90:
    management_status = "WATCH"
else:
    management_status = "ACTION REQUIRED"


# ----------------------------------------
# Region Analysis
# ----------------------------------------

region = (
    ytd_df
    .groupby("Region", observed=True)
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum"),
        Previous_Year_Sales_Lakh=(
            "Previous_Year_Sales_Lakh",
            "sum"
        )
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

region["Growth_%"] = (
    (
        region["Sales_Lakh"]
        / region["Previous_Year_Sales_Lakh"]
    ) - 1
) * 100

region["Contribution_%"] = (
    region["Sales_Lakh"]
    / region["Sales_Lakh"].sum()
) * 100

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
        Target_Lakh=("Target_Lakh", "sum"),
        Previous_Year_Sales_Lakh=(
            "Previous_Year_Sales_Lakh",
            "sum"
        )
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

channel["Growth_%"] = (
    (
        channel["Sales_Lakh"]
        / channel["Previous_Year_Sales_Lakh"]
    ) - 1
) * 100

channel["Contribution_%"] = (
    channel["Sales_Lakh"]
    / channel["Sales_Lakh"].sum()
) * 100

primary_channel = (
    channel
    .sort_values("Gap_Lakh", ascending=False)
    .iloc[0]
)


# ----------------------------------------
# Scenario Planning
# ----------------------------------------

scenarios = {
    "BASE": {
        "GT": 0,
        "WEST": 0
    },
    "UPSIDE": {
        "GT": 10,
        "WEST": 10
    },
    "STRETCH": {
        "GT": 15,
        "WEST": 15
    }
}

gt_ytd = ytd_df[
    ytd_df["Channel"] == "GT"
]["Current_Sales_Lakh"].sum()

west_ytd = ytd_df[
    ytd_df["Region"] == "West"
]["Current_Sales_Lakh"].sum()

gt_monthly = gt_ytd / months_completed
west_monthly = west_ytd / months_completed

scenario_results = []

for name, assumption in scenarios.items():

    gt_increment = (
        gt_monthly
        * months_remaining
        * assumption["GT"] / 100
    )

    west_increment = (
        west_monthly
        * months_remaining
        * assumption["WEST"] / 100
    )

    incremental_revenue = (
        gt_increment + west_increment
    )

    projected = (
        projected_revenue
        + incremental_revenue
    )

    achievement = (
        projected / full_year_target * 100
    )

    remaining_gap = max(
        full_year_target - projected,
        0
    )

    gap_closed = (
        incremental_revenue
        / projected_gap * 100
        if projected_gap > 0
        else 0
    )

    if achievement >= 100:
        status = "ON TRACK"
    elif achievement >= 90:
        status = "WATCH"
    else:
        status = "ACTION REQUIRED"

    scenario_results.append([
        name,
        assumption["GT"],
        assumption["WEST"],
        incremental_revenue,
        projected,
        achievement,
        remaining_gap,
        gap_closed,
        status
    ])


# ========================================
# AI MANAGEMENT COMMENTARY
# ========================================

stretch_result = next(
    result for result in scenario_results
    if result[0] == "STRETCH"
)

(
    stretch_name,
    stretch_gt,
    stretch_west,
    stretch_incremental,
    stretch_revenue,
    stretch_achievement,
    stretch_gap,
    stretch_gap_closed,
    stretch_status
) = stretch_result


# ========================================
# EXECUTIVE DASHBOARD OUTPUT
# ========================================

print("=" * 70)
print("             EXECUTIVE MANAGEMENT DASHBOARD")
print("=" * 70)

print(f"\nAs of Month: {AS_OF_MONTH}")


# ----------------------------------------
# Revenue Health
# ----------------------------------------

print("\n--- REVENUE HEALTH ---")

print(f"YTD Sales: ₹{ytd_sales:.2f} Lakh")
print(f"YTD Achievement: {ytd_achievement:.1f}%")
print(f"Current Monthly Run Rate: ₹{monthly_run_rate:.2f} Lakh")
print(f"Full-Year Target: ₹{full_year_target:.2f} Lakh")
print(f"Projected Revenue: ₹{projected_revenue:.2f} Lakh")
print(f"Projected Achievement: {projected_achievement:.1f}%")
print(f"Projected Gap: ₹{projected_gap:.2f} Lakh")
print(f"Management Status: {management_status}")


# ----------------------------------------
# Performance Alerts
# ----------------------------------------

print("\n--- PERFORMANCE ALERTS ---")

print(
    f"Priority Channel: {primary_channel['Channel']} "
    f"| Gap: ₹{primary_channel['Gap_Lakh']:.2f}L"
)

print(
    f"Priority Region: {primary_region['Region']} "
    f"| Gap: ₹{primary_region['Gap_Lakh']:.2f}L"
)

print(
    f"Required Monthly Run Rate: "
    f"₹{required_monthly_run_rate:.2f}L"
)

print(
    f"Required Run-Rate Uplift: "
    f"{run_rate_uplift:.1f}%"
)


# ----------------------------------------
# Scenario Outlook
# ----------------------------------------

print("\n--- SCENARIO OUTLOOK ---")

for result in scenario_results:

    (
        name,
        gt_improvement,
        west_improvement,
        incremental,
        projected,
        achievement,
        remaining_gap,
        gap_closed,
        status
    ) = result

    print(f"\n{name} CASE")

    print(
        f"GT: +{gt_improvement}% | "
        f"West: +{west_improvement}%"
    )

    print(
        f"Incremental Revenue: "
        f"+₹{incremental:.2f}L"
    )

    print(
        f"Projected Revenue: "
        f"₹{projected:.2f}L"
    )

    print(
        f"Achievement: "
        f"{achievement:.1f}%"
    )

    print(
        f"Remaining Gap: "
        f"₹{remaining_gap:.2f}L"
    )

    print(
        f"Gap Closed: "
        f"{gap_closed:.1f}%"
    )

    print(
        f"Status: {status}"
    )


# ========================================
# AI MANAGEMENT COMMENTARY
# ========================================

print("\n--- AI MANAGEMENT COMMENTARY ---")

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

print("\nKEY BUSINESS RISK")

print(
    f"The business needs to increase its monthly "
    f"run rate from ₹{monthly_run_rate:.2f}L to "
    f"₹{required_monthly_run_rate:.2f}L."
)

print(
    f"This represents a required uplift of "
    f"approximately {run_rate_uplift:.1f}%."
)

print("\nPRIORITY AREAS")

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

print("\nSCENARIO INSIGHT")

print(
    f"Under the Stretch scenario, with "
    f"{stretch_gt}% improvement in both GT and West, "
    f"projected revenue increases to "
    f"₹{stretch_revenue:.2f}L."
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


# ----------------------------------------
# Executive Recommendation
# ----------------------------------------

print("\n--- EXECUTIVE RECOMMENDATION ---")

print(
    f"1. Focus immediate commercial intervention on "
    f"{primary_channel['Channel']} and "
    f"{primary_region['Region']}."
)

print(
    f"2. Raise the monthly run rate by at least "
    f"{run_rate_uplift:.1f}%."
)

print(
    "3. Track incremental revenue generated from "
    "each commercial intervention."
)

print(
    "4. Use the Stretch scenario as the minimum "
    "recovery benchmark rather than the final objective."
)

print("\n" + "=" * 70)
