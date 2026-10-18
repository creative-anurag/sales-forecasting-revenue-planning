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
# BASELINE FORECAST
# -----------------------------------------

ytd_sales = ytd_df["Current_Sales_Lakh"].sum()
full_year_target = df["Target_Lakh"].sum()

monthly_run_rate = ytd_sales / months_elapsed

baseline_forecast = monthly_run_rate * 12

baseline_gap = full_year_target - baseline_forecast

# -----------------------------------------
# SCENARIO ASSUMPTIONS
# -----------------------------------------

GT_IMPROVEMENT = 10
WEST_IMPROVEMENT = 10

# -----------------------------------------
# GT SCENARIO
# -----------------------------------------

gt_sales = ytd_df.loc[
    ytd_df["Channel"] == "GT",
    "Current_Sales_Lakh"
].sum()

gt_scenario_impact = (
    gt_sales * (GT_IMPROVEMENT / 100)
)

# -----------------------------------------
# WEST SCENARIO
# -----------------------------------------

west_sales = ytd_df.loc[
    ytd_df["Region"] == "West",
    "Current_Sales_Lakh"
].sum()

west_scenario_impact = (
    west_sales * (WEST_IMPROVEMENT / 100)
)

# -----------------------------------------
# COMBINED SCENARIO
# -----------------------------------------

combined_impact = (
    gt_scenario_impact +
    west_scenario_impact
)

scenario_forecast = (
    baseline_forecast +
    combined_impact
)

scenario_gap = (
    full_year_target -
    scenario_forecast
)

scenario_achievement = (
    scenario_forecast /
    full_year_target
) * 100

gap_closed = (
    combined_impact /
    baseline_gap
) * 100

# -----------------------------------------
# MANAGEMENT OUTPUT
# -----------------------------------------

print("\n========================================")
print("COMMERCIAL SCENARIO SIMULATOR")
print("========================================\n")

print(f"As of Month: {AS_OF_MONTH}")

print("\n--- Baseline ---")
print(f"Projected Revenue: ₹{baseline_forecast:.2f} Lakh")
print(f"Projected Gap: ₹{baseline_gap:.2f} Lakh")

print("\n--- Scenario Assumptions ---")
print(f"GT Improvement: {GT_IMPROVEMENT}%")
print(f"West Improvement: {WEST_IMPROVEMENT}%")

print("\n--- Scenario Impact ---")
print(
    f"GT Revenue Impact: "
    f"+₹{gt_scenario_impact:.2f} Lakh"
)

print(
    f"West Revenue Impact: "
    f"+₹{west_scenario_impact:.2f} Lakh"
)

print(
    f"Combined Revenue Impact: "
    f"+₹{combined_impact:.2f} Lakh"
)

print("\n--- Scenario Outcome ---")
print(
    f"Scenario Projected Revenue: "
    f"₹{scenario_forecast:.2f} Lakh"
)

print(
    f"Scenario Achievement: "
    f"{scenario_achievement:.1f}%"
)

print(
    f"Scenario Gap: "
    f"₹{scenario_gap:.2f} Lakh"
)

print(
    f"Projected Gap Closed: "
    f"{gap_closed:.1f}%"
)
