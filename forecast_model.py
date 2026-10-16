import pandas as pd

# Load sample sales data
df = pd.read_csv("sales_forecasting_sample_data.csv")

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

print("\n--- Management Summary ---")
print(f"Current Sales: ₹{total_current:.2f} Lakh")
print(f"Target: ₹{total_target:.2f} Lakh")
print(f"Achievement: {overall_achievement:.1f}%")
print(f"Gap to Target: ₹{total_gap:.2f} Lakh")
total_forecast = df["Forecast_Lakh"].sum()
forecast_gap = total_target - total_forecast

print(f"Forecast: ₹{total_forecast:.2f} Lakh")
print(f"Forecast Gap: ₹{forecast_gap:.2f} Lakh")
