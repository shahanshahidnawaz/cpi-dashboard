# Import the system module so we can write the data to stdout, a technique recommended by Observable
import sys

# Import the cpi module so we can get the data we need
import cpi

# Get the standard CPI-U series, seasonally adjusted, so we can compare it month-to-month
df = cpi.series.get(seasonally_adjusted=True).to_dataframe()

# Filter it down to monthly values, excluding annual averages
df = df[df.period_type == "monthly"].copy()

# Sort it by date so we can calculate the percentage change
df = df.sort_values("date")

# Cut it down to the last 13 months, plus one, so we can cover the same time range as the BLS's PDF chart
df = df.tail(13 + 1)

# Calculate the percentage change and round it to one decimal place, as the BLS does
df["change"] = (df.value.pct_change() * 100).round(1)

# Drop the first value, which is the 14th month we only needed for the calculation
df = df.iloc[1:]

# Output the results to stdout in JSON format
df.to_json(sys.stdout, orient="records", date_format="iso")