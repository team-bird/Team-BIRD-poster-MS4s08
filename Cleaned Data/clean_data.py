
import pandas as pd

INPUT_FILE = "aff5ratioofhousepriceexistingtoworkplacebasedearnings.xlsx"

# ---------------------------------------------------------------
# 1. LOAD THE CONFIRMED SHEET
# ---------------------------------------------------------------
# Sheet "5c" = "Ratio of median house price (existing dwellings) to
# median gross annual workplace-based earnings by local authority
# district, England and Wales, 1997 to 2025" - confirmed by
# inspecting the actual file. Header is on row 2 (1-indexed), so
# skiprows=1 with header=0 lands on the real header row.
df = pd.read_excel(INPUT_FILE, sheet_name="5c", skiprows=1, header=0)
print(df.columns.tolist())
print(df.head())
print("Rows:", len(df))

# ---------------------------------------------------------------
# 2. RENAME THE ID COLUMNS (confirmed real column names)
# ---------------------------------------------------------------
df = df.rename(columns={
    "Local authority code": "la_code",
    "Local authority name": "local_authority",
})

# ---------------------------------------------------------------
# 4. RESHAPE FROM WIDE (one column per year) TO LONG
# ---------------------------------------------------------------
# Confirmed: year columns are 1997-2025 (as column headers like
# "1997", "1998", etc). There's also a "5-Year Average" column
# which is NOT a year, so it's correctly excluded by the isdigit()
# check below (it doesn't look like a plain number).
year_columns = [c for c in df.columns if str(c).strip().isdigit()]
print("Detected year columns:", year_columns)

long_df = df.melt(
    id_vars=["la_code", "local_authority"],
    value_vars=year_columns,
    var_name="year",
    value_name="ratio",
)

long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce")
long_df["ratio"] = pd.to_numeric(long_df["ratio"], errors="coerce")

# ---------------------------------------------------------------
# 5. REMOVE NON-LOCAL-AUTHORITY AGGREGATE ROWS (safety check)
# ---------------------------------------------------------------
# Confirmed: sheet 5c is local-authority-level only (no "England"/
# "Wales" summary rows mixed in - those live in sheet 1c instead).
# This filter is kept as a safety net in case anything unexpected
# shows up.
aggregate_rows = ["England", "Wales", "England and Wales", "United Kingdom"]
local_authority_level = long_df[~long_df["local_authority"].isin(aggregate_rows)].copy()

# ---------------------------------------------------------------
# 6. FLAG ENGLAND VS WALES
# ---------------------------------------------------------------
# Confirmed via the real file: 296 England local authorities (code
# prefix "E"), 22 Wales local authorities (code prefix "W")
local_authority_level["country"] = local_authority_level["la_code"].astype(str).str[0].map({
    "E": "England",
    "W": "Wales",
})

print(local_authority_level["country"].value_counts())

# ---------------------------------------------------------------
# 7. CHECK FOR MISSING VALUES / DUPLICATES
# ---------------------------------------------------------------
print(local_authority_level.isnull().sum())
print("Duplicates:", local_authority_level.duplicated(subset=["la_code", "year"]).sum())

local_authority_level = local_authority_level.dropna(subset=["ratio", "country"])
local_authority_level = local_authority_level.drop_duplicates(subset=["la_code", "year"])

# ---------------------------------------------------------------
# 8. SAVE CLEANED FILE
# ---------------------------------------------------------------
local_authority_level = local_authority_level.sort_values(["country", "local_authority", "year"])
local_authority_level.to_csv("cleaned_affordability.csv", index=False)

print("\nDone. Rows:", len(local_authority_level))
print("Local authorities:", local_authority_level["local_authority"].nunique())
print("Years:", local_authority_level["year"].min(), "to", local_authority_level["year"].max())
print("\nSaved to cleaned_affordability.csv - import this directly into SAS.")
