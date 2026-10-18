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

# -----------------------------------------
# YTD DATA
# -----------------------------------------

ytd_df = df[
    df["Month"].isin(month_order[:months_elapsed])
].copy()

# -----------------------------------------
# BASELINE
# -----------------------------------------

ytd_sales = ytd_df["Current_Sales_Lakh"].sum()
full_year_target = df["Target_Lakh"].sum()

monthly_run_rate = ytd_sales / months_elapsed

baseline_remaining_sales = (
    monthly_run_rate * months_remaining
)

baseline_forecast = (
    ytd_sales + baseline_remaining_sales
)

baseline_gap = (
    full_year_target - baseline_forecast
)

# -----------------------------------------
# SEGMENT BASELINES
# -----------------------------------------

gt_ytd_sales = ytd_df.loc[
    ytd_df["Channel"] == "GT",
    "Current_Sales_Lakh"
].sum()

west_ytd_sales = ytd_df.loc[
    ytd_df["Region"] == "West",
    "Current_Sales_Lakh"
].sum()

gt_monthly_run_rate = gt_ytd_sales / months_elapsed
west_monthly_run_rate = west_ytd_sales / months_elapsed

gt_remaining_baseline = (
    gt_monthly_run_rate * months_remaining
)

west_remaining_baseline = (
    west_monthly_run_rate * months_remaining
)

# -----------------------------------------
# SCENARIOS
# -----------------------------------------

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

# -----------------------------------------
# SCENARIO ENGINE
# -----------------------------------------

results = []

for scenario_name, assumptions in scenarios.items():

    gt_impact = (
        gt_remaining_baseline *
        assumptions["GT"] / 100
    )

    west_impact = (
        west_remaining_baseline *
        assumptions["WEST"] / 100
    )

    total_incremental = (
        gt_impact + west_impact
    )

    projected_revenue = (
        baseline_forecast +
        total_incremental
    )

    projected_achievement = (
        projected_revenue /
        full_year_target
    ) * 100

    projected_gap = (
        full_year_target -
        projected_revenue
    )

    gap_closed = (
        total_incremental /
        baseline_gap
    ) * 100

    if projected_achievement >= 100:
        status = "ON TRACK"
    elif projected_achievement >= 90:
        status = "WATCH"
    else:
        status = "ACTION REQUIRED"

    results.append({
        "Scenario": scenario_name,
        "GT Improvement %": assumptions["GT"],
        "West Improvement %": assumptions["WEST"],
        "Incremental Revenue Lakh": total_incremental,
        "Projected Revenue Lakh": projected_revenue,
        "Achievement %": projected_achievement,
        "Gap Lakh": max(projected_gap, 0),
        "Gap Closed %": gap_closed,
        "Status": status
    })

# -----------------------------------------
# OUTPUT
# -----------------------------------------

results_df = pd.DataFrame(results)

print("\n========================================")
print("MULTI-SCENARIO COMMERCIAL ENGINE")
print("========================================\n")

print(f"As of Month: {AS_OF_MONTH}")
print(f"Months Remaining: {months_remaining}")

print("\n--- Baseline ---")
print(f"YTD Sales: ₹{ytd_sales:.2f} Lakh")
print(f"Monthly Run Rate: ₹{monthly_run_rate:.2f} Lakh")
print(f"Annual Target: ₹{full_year_target:.2f} Lakh")
print(f"Baseline Forecast: ₹{baseline_forecast:.2f} Lakh")
print(f"Baseline Gap: ₹{baseline_gap:.2f} Lakh")

print("\n--- Scenario Comparison ---")

for _, row in results_df.iterrows():

    print(f"\n{row['Scenario']} CASE")
    print(
        f"GT Improvement: "
        f"{row['GT Improvement %']:.0f}%"
    )
    print(
        f"West Improvement: "
        f"{row['West Improvement %']:.0f}%"
    )
    print(
        f"Incremental Revenue: "
        f"+₹{row['Incremental Revenue Lakh']:.2f} Lakh"
    )
    print(
        f"Projected Revenue: "
        f"₹{row['Projected Revenue Lakh']:.2f} Lakh"
    )
    print(
        f"Achievement: "
        f"{row['Achievement %']:.1f}%"
    )
    print(
        f"Remaining Gap: "
        f"₹{row['Gap Lakh']:.2f} Lakh"
    )
    print(
        f"Gap Closed: "
        f"{row['Gap Closed %']:.1f}%"
    )
    print(
        f"Management Status: "
        f"{row['Status']}"
    )
