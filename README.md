# Housing Affordability in England and Wales, 1997–2025

**Module:** MS4S08 Applied Statistics for Data Science
**Institution:** University of South Wales
**Assessment:** Group poster (Tasks A–C) + individual reflective diary (Task D)

---

## Research question

How has housing affordability in England and Wales changed between 2015 and 2025,
and how do the two countries compare at national and regional level?

---

## Data source

| Field | Value |
|---|---|
| Dataset | House price (existing dwellings) to workplace-based earnings ratio |
| Publisher | Office for National Statistics (ONS) |
| Licence | Open Government Licence v3.0 |
| Coverage | Local authority districts in England and Wales, 1997–2025 |
| Format | Excel workbook, one sheet per analysis type |
| Dataset page | https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/housepriceexistingdwellingstoworkplacebasedearningsratio |

The analysis uses **Table 5c** of the ONS release — median affordability ratio
at local authority district level.

---

## Repository structure

```
Raw Data/
    Raw Data.xlsx                          # Original ONS workbook (untouched)

Cleaned Data/
    clean_data.py                          # Python cleaning script
    cleaned_affordability.csv              # One row per authority-year

SAS analysis & visualization/
    England_2025_table.pdf                 # Descriptive table: England 2025
    wales_2025_tabl.pdf                    # Descriptive table: Wales 2025
    table1_summary.pdf                     # Summary statistics table
    check1_years.pdf                       # Year coverage check
    WORK.PAIRED.pdf                        # Paired 2015 vs 2025 output
    test1_signedrank.pdf                   # Wilcoxon signed-rank (paired)
    test2_kruskalwalli.pdf                 # Kruskal–Wallis (regional, 2025)
    test3_england_wales.pdf                # Wilcoxon two-sample (England vs Wales)
    figure1_hist_diff.pdf                  # Histogram of paired differences
    figure2_boxplot_year.pdf               # Boxplot by year
    figure3_region_bar.pdf                 # Regional bar chart, 2025
    figure4_movers.pdf                     # Biggest movers
    figure6_trends.pdf                     # Trend lines

Poster/
    affordability.pbix                     # Power BI interactive dashboard

.gitignore
README.md
```

| Folder | Contents |
|---|---|
| `Raw Data/` | Original ONS workbook, unmodified |
| `Cleaned Data/` | Cleaning script + tidy CSV (one row per authority-year) |
| `SAS analysis & visualization/` | SAS outputs: tables, test results, figures |
| `Poster/` | Power BI dashboard file (`.pbix`) |

---

## Data pipeline

### 1. Cleaning — Python

`Cleaned Data/clean_data.py` reads the ONS workbook, selects the "5c" sheet,
reshapes from wide to long format, drops suppressed values (`[x]`),
and writes `Cleaned Data/cleaned_affordability.csv`.

**Dependencies:**

```bash
pip install pandas openpyxl
```

**Run:**

```bash
python "Cleaned Data/clean_data.py"
```

**Output columns:**

| Column | Description |
|---|---|
| `la_code` | ONS local authority code |
| `local_authority` | Local authority name |
| `year` | Year, 1997–2025 |
| `ratio` | Median house price ÷ median workplace-based earnings |
| `region_code` | ONS region code |
| `region` | Region name |
| `country` | England or Wales |

### 2. Analysis — SAS

SAS code imports the cleaned CSV and runs three non-parametric tests.
Outputs are saved as PDFs in `SAS analysis & visualization/`.

| Test | Purpose | SAS procedure | Output file |
|---|---|---|---|
| Wilcoxon signed-rank | Paired 2015 vs 2025 comparison | `PROC UNIVARIATE` | `test1_signedrank.pdf` |
| Kruskal–Wallis | Regional comparison, 2025 | `PROC NPAR1WAY` | `test2_kruskalwalli.pdf` |
| Wilcoxon two-sample | England vs Wales, 2025 | `PROC NPAR1WAY` | `test3_england_wales.pdf` |

### 3. Visualisation — Power BI

`Poster/affordability.pbix` contains the interactive dashboard:

- KPI cards: median 2015 vs 2025, England vs Wales, region gap
- Region bar chart with red/amber/blue colour banding
- England and Wales line chart
- Change chart with red/green directional colouring
- Scatterplot linking price growth to ratio change
- Wales map
- Top-15 least affordable bar chart
- Country and year slicers

---

## Key results

| Result | Value |
|---|---|
| Median ratio 2015 | 7.55 |
| Median ratio 2025 | 7.84 |
| England median 2025 | 8.07 |
| Wales median 2025 | 5.87 |
| England–Wales gap | 37% |
| Highest region (London) | 12.22 |
| Lowest region (North East) | 4.67 |
| **Wilcoxon signed-rank** | S = 9593, p < 0.0001 |
| **Kruskal–Wallis** | χ²(9) = 222.04, p < 0.0001 |
| **England vs Wales** | Z = −4.76, p < 0.001 |

---

## Why non-parametric tests

Normality was rejected for both the paired differences and the England 2025 ratios:

- Kolmogorov–Smirnov on paired differences: D = 0.147, p < 0.010
- Anderson–Darling on paired differences: A² = 12.13, p < 0.005
- Shapiro–Wilk on England 2025: W = 0.942, p < 0.0001

The skew is driven by a small number of prime central London boroughs
with ratios above 20. Non-parametric tests do not assume normality
and are robust to this skew.

---

## Reproducing the analysis

1. Clone the repository.
2. Install Python dependencies:

   ```bash
   pip install pandas openpyxl
   ```

3. Run the cleaning script:

   ```bash
   python "Cleaned Data/clean_data.py"
   ```

4. Import `Cleaned Data/cleaned_affordability.csv` into SAS Studio.
5. Run the SAS analysis and confirm PDFs match those in
   `SAS analysis & visualization/`.
6. Open `Poster/affordability.pbix` and refresh the data source
   to point at your local copy of the CSV.

---

## Notes and limitations

- Analysis uses Table 5c only (median local-authority ratios).
  Lower-quartile, county-level, and region-level tables exist in
  the same workbook but were not used.
- Values marked `[x]` in the ONS data are suppressed due to small
  sample sizes. These rows are dropped. Early-year sample sizes
  (1997–2002) are slightly smaller than later years.
- Local authority boundary changes affect the series. Successor
  authorities such as Cornwall, Wiltshire, North Yorkshire, Cumberland,
  and Westmorland and Furness appear only from their creation year.
- The 2025 data is provisional and subject to revision.

---

## Licence

ONS data is © Crown copyright, reproduced under the Open Government
Licence v3.0. Analysis code in this repository is released under the
MIT Licence.

---

## Authors

Group project for MS4S08, University of South Wales, 2026–2027.
