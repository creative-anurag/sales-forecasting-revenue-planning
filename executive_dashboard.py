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

ytd_df = df.iloc[:0].copy()

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
# EXECUTIVE DASHBOARD OUTPUT
# ========================================

print("=" * 55)
print("        EXECUTIVE MANAGEMENT DASHBOARD")
print("=" * 55)

print(f"\nAs of Month: {AS_OF_MONTH}")

print("\n--- REVENUE HEALTH ---")

print(f"YTD Sales: ₹{ytd_sales:.2f} Lakh")
print(f"YTD Achievement: {ytd_achievement:.1f}%")
print(f"Current Monthly Run Rate: ₹{monthly_run_rate:.2f} Lakh")
print(f"Full-Year Target: ₹{full_year_target:.2f} Lakh")
print(f"Projected Revenue: ₹{projected_revenue:.2f} Lakh")
print(f"Projected Achievement: {projected_achievement:.1f}%")
print(f"Projected Gap: ₹{projected_gap:.2f} Lakh")
print(f"Management Status: {management_status}")


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


print("\n--- EXECUTIVE RECOMMENDATION ---")

print(
    f"1. Prioritize {primary_channel['Channel']} "
    f"to address the largest channel gap."
)

print(
    f"2. Prioritize {primary_region['Region']} "
    f"to address the largest regional gap."
)

print(
    f"3. Lift monthly run rate by approximately "
    f"{run_rate_uplift:.1f}%."
)

print(
    "4. Use scenario planning to track whether "
    "commercial interventions are sufficient."
)

print("\n" + "=" * 55)
