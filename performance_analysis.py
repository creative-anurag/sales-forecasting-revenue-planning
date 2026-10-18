import pandas as pd

# Load sales data
df = pd.read_csv("sales_forecasting_sample_data.csv")

# Calculate growth
df["Growth_%"] = (
    (df["Current_Sales_Lakh"] - df["Previous_Year_Sales_Lakh"])
    / df["Previous_Year_Sales_Lakh"]
) * 100

# Calculate achievement
df["Achievement_%"] = (
    df["Current_Sales_Lakh"] / df["Target_Lakh"]
) * 100

# Calculate gap
df["Gap_Lakh"] = (
    df["Target_Lakh"] - df["Current_Sales_Lakh"]
)

# -----------------------------------------
# REGION PERFORMANCE
# -----------------------------------------

region_analysis = (
    df.groupby("Region")
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum"),
        Previous_Year_Sales_Lakh=("Previous_Year_Sales_Lakh", "sum")
    )
    .reset_index()
)

region_analysis["Achievement_%"] = (
    region_analysis["Sales_Lakh"]
    / region_analysis["Target_Lakh"]
) * 100

region_analysis["Growth_%"] = (
    (region_analysis["Sales_Lakh"]
     - region_analysis["Previous_Year_Sales_Lakh"])
    / region_analysis["Previous_Year_Sales_Lakh"]
) * 100

region_analysis["Gap_Lakh"] = (
    region_analysis["Target_Lakh"]
    - region_analysis["Sales_Lakh"]
)

region_analysis["Contribution_%"] = (
    region_analysis["Sales_Lakh"]
    / region_analysis["Sales_Lakh"].sum()
) * 100

region_analysis["Status"] = region_analysis["Achievement_%"].apply(
    lambda x:
    "On Track" if x >= 100
    else "Watch" if x >= 90
    else "Action Required"
)

# -----------------------------------------
# CHANNEL PERFORMANCE
# -----------------------------------------

channel_analysis = (
    df.groupby("Channel")
    .agg(
        Sales_Lakh=("Current_Sales_Lakh", "sum"),
        Target_Lakh=("Target_Lakh", "sum"),
        Previous_Year_Sales_Lakh=("Previous_Year_Sales_Lakh", "sum")
    )
    .reset_index()
)

channel_analysis["Achievement_%"] = (
    channel_analysis["Sales_Lakh"]
    / channel_analysis["Target_Lakh"]
) * 100

channel_analysis["Growth_%"] = (
    (channel_analysis["Sales_Lakh"]
     - channel_analysis["Previous_Year_Sales_Lakh"])
    / channel_analysis["Previous_Year_Sales_Lakh"]
) * 100

channel_analysis["Gap_Lakh"] = (
    channel_analysis["Target_Lakh"]
    - channel_analysis["Sales_Lakh"]
)

channel_analysis["Contribution_%"] = (
    channel_analysis["Sales_Lakh"]
    / channel_analysis["Sales_Lakh"].sum()
) * 100

channel_analysis["Status"] = channel_analysis["Achievement_%"].apply(
    lambda x:
    "On Track" if x >= 100
    else "Watch" if x >= 90
    else "Action Required"
)

# -----------------------------------------
# MANAGEMENT OUTPUT
# -----------------------------------------

print("\n========================================")
print("REGION PERFORMANCE")
print("========================================\n")

print(
    region_analysis[
        [
            "Region",
            "Sales_Lakh",
            "Target_Lakh",
            "Achievement_%",
            "Growth_%",
            "Gap_Lakh",
            "Contribution_%",
            "Status"
        ]
    ].round(1).to_string(index=False)
)

print("\n========================================")
print("CHANNEL PERFORMANCE")
print("========================================\n")

print(
    channel_analysis[
        [
            "Channel",
            "Sales_Lakh",
            "Target_Lakh",
            "Achievement_%",
            "Growth_%",
            "Gap_Lakh",
            "Contribution_%",
            "Status"
        ]
    ].round(1).to_string(index=False)
)
