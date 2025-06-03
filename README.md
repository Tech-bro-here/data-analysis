# PV Data Analysis and Visualization

## Overview
This project processes and visualizes PV plant data using daily PR (Performance Ratio) and GHI (Global Horizontal Irradiance) CSV files. It combines the data into a single CSV and generates a performance evolution plot as described in the assignment.

## Folder Structure
```
project-root/
│
├── PR/
│   ├── 2019-07/
│   │   ├── 2019-07-01.csv
│   │   ├── ...
│   └── ...
├── GHI/
│   ├── 2019-07/
│   │   ├── 2019-07-01.csv
│   │   ├── ...
│   └── ...
├── app.py
└── output/
    ├── combined_data.csv
    └── pr_evolution.png
```

- Each `.csv` file in PR and GHI folders is named as `YYYY-MM-DD.csv` and contains a `Date` column and either a `PR` or `GHI` column.

## Requirements
- Python 3.7+
- pandas
- matplotlib
- seaborn

Install dependencies with:
```sh
pip install pandas matplotlib seaborn
```

## How to Run

From the project root, run:
```sh
python app.py --pr_dir "PR" --ghi_dir "GHI" --output_csv "output/combined_data.csv" --output_plot "output/pr_evolution.png" --start_date "2019-07-01" --end_date "2022-03-24"
```

Or simply:
```sh
python app.py
```
if your folders are named `PR` and `GHI` and you want to use the default output and date range.

### Arguments
- `--pr_dir`: Path to PR data directory (default: `PR`)
- `--ghi_dir`: Path to GHI data directory (default: `GHI`)
- `--output_csv`: Output CSV file path (default: `output/combined_data.csv`)
- `--output_plot`: Output plot file path (default: `output/pr_evolution.png`)
- `--start_date`: Start date for the plot (default: `2019-07-01`)
- `--end_date`: End date for the plot (default: `2022-03-24`)

## Output
- `output/combined_data.csv`: Combined data with columns `Date`, `GHI`, `PR` (should have 982 rows if all data is present).
- `output/pr_evolution.png`: Performance Ratio evolution plot with moving average, budget line, and color-coded GHI points.

## Notes
- The script will print warnings if files or columns are missing or if dates do not match.
- The plot and CSV are generated according to the assignment requirements.

## Contact
For any issues, please contact the project maintainer. 
