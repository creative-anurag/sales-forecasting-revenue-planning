import pandas as pd

# Load sample sales data
df = pd.read_csv("sales_forecasting_sample_data.csv")

# Forecast as of a specific month
AS_OF_MONTH = "Sep-26"

# Define financial year month sequence
month_order = [
    "Apr-26", "May-26", "Jun-26", "Jul-26",
    "Aug-26", "Sep-26", "Oct-26", "Nov-26",
    "Dec-26", "Jan-27", "Feb-27", "Mar-27"
]

# Identify months completed
months_elapsed = month_order.index(AS_OF_MONTH) + 1
months_remaining = 12 - months_elapsed

# Keep only sales achieved up to the forecast date
ytd_df = df[df["Month"].isin(month_order[:months_elapsed])].copy()

# YTD sales
ytd_sales = ytd_df["Current_Sales_Lakh"].sum()

# Full-year target
full_year_target = df["Target_Lakh"].sum()

# YTD achievement against proportional target
ytd_target = full_year_target * (months_elapsed / 12)
ytd_achievement = (ytd_sales / ytd_target) * 100

# Average monthly run rate
monthly_run_rate = ytd_sales / months_elapsed

# Projected full-year revenue
projected_revenue = monthly_run_rate * 12

# Projected achievement
projected_achievement = (
    projected_revenue / full_year_target
) * 100

# Projected gap
projected_gap = full_year_target - projected_revenue

# Management status
if projected_achievement >= 100:
    management_status = "On Track"
elif projected_achievement >= 90:
    management_status = "Watch"
else:
    management_status = "Action Required"

# Calculate year-on-year growth
df["Growth_%"] = (
    (df["Current_Sales_Lakh"] - df["Previous_Year_Sales_Lakh"])
    / df["Previous_Year_Sales_Lakh"]
) * 100

# Calculate target achievement
df["Achievement_%"] = (
    df["Current_Sales_Lakh"] / df["Target_Lakh"]
) * 100

# Calculate sales gap against target
df["Gap_Lakh"] = df["Target_Lakh"] - df["Current_Sales_Lakh"]

# Calculate forecast using current growth rate
df["Forecast_Lakh"] = (
    df["Previous_Year_Sales_Lakh"] * (1 + df["Growth_%"] / 100)
)

# Calculate forecast gap against target
df["Forecast_Gap_Lakh"] = (
    df["Target_Lakh"] - df["Forecast_Lakh"]
)

# Forecast status
df["Forecast_Status"] = df["Forecast_Gap_Lakh"].apply(
    lambda x: "Expected Surplus" if x <= 0 else "Expected Gap"
)
# Create management status
df["Status"] = df["Achievement_%"].apply(
    lambda x: "On Track" if x >= 100 else "Gap to Target"
)

# Display results
print("\nSales Forecasting & Revenue Planning Analysis\n")
print(df.to_string(index=False))

# Summary
total_current = df["Current_Sales_Lakh"].sum()
total_target = df["Target_Lakh"].sum()
total_gap = df["Gap_Lakh"].sum()

overall_achievement = (total_current / total_target) * 100

print("\nSales Forecasting & Revenue Planning Analysis\n")

print(f"As of Month: {AS_OF_MONTH}")
print(f"Months Completed: {months_elapsed}")
print(f"Months Remaining: {months_remaining}")

print("\n--- Management Forecast ---")
print(f"YTD Sales: ₹{ytd_sales:.2f} Lakh")
print(f"YTD Target: ₹{ytd_target:.2f} Lakh")
print(f"YTD Achievement: {ytd_achievement:.1f}%")
print(f"Monthly Run Rate: ₹{monthly_run_rate:.2f} Lakh")
print(f"Projected Full-Year Revenue: ₹{projected_revenue:.2f} Lakh")
print(f"Full-Year Target: ₹{full_year_target:.2f} Lakh")
print(f"Projected Achievement: {projected_achievement:.1f}%")
print(f"Projected Gap: ₹{projected_gap:.2f} Lakh")
print(f"Management Status: {management_status}")
