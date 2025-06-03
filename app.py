import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from datetime import datetime, timedelta
import argparse

def process_data(pr_dir: str, ghi_dir: str, output_file: str) -> pd.DataFrame:
    print(f"Looking for PR data in: {os.path.abspath(pr_dir)}")
    print(f"Looking for GHI data in: {os.path.abspath(ghi_dir)}")

    pr_data = []
    ghi_data = []

    # Helper to find all csv files recursively
    def find_csv_files(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    yield os.path.join(root, file)

    # Read GHI files
    ghi_dict = {}
    for file_path in find_csv_files(ghi_dir):
        file_name = os.path.basename(file_path)
        date_str = file_name.replace('.csv', '')
        try:
            expected_date = pd.to_datetime(date_str, format='%Y-%m-%d')
        except Exception:
            continue
        df = pd.read_csv(file_path)
        df.columns = [col.strip().capitalize() for col in df.columns]
        if 'Date' not in df.columns or 'Ghi' not in df.columns:
            continue
        df = df.rename(columns={'Ghi': 'GHI'})
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        row = df[df['Date'] == expected_date]
        if not row.empty:
            ghi_dict[expected_date] = row[['Date', 'GHI']].iloc[0]

    # Read PR files
    pr_dict = {}
    for file_path in find_csv_files(pr_dir):
        file_name = os.path.basename(file_path)
        date_str = file_name.replace('.csv', '')
        try:
            expected_date = pd.to_datetime(date_str, format='%Y-%m-%d')
        except Exception:
            continue
        df = pd.read_csv(file_path)
        df.columns = [col.strip().capitalize() for col in df.columns]
        if 'Date' not in df.columns or 'Pr' not in df.columns:
            continue
        df = df.rename(columns={'Pr': 'PR'})
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        row = df[df['Date'] == expected_date]
        if not row.empty:
            pr_dict[expected_date] = row[['Date', 'PR']].iloc[0]

    # Merge by date
    merged_rows = []
    for date in sorted(set(ghi_dict.keys()) & set(pr_dict.keys())):
        ghi_row = ghi_dict[date]
        pr_row = pr_dict[date]
        merged_rows.append({'Date': date, 'GHI': ghi_row['GHI'], 'PR': pr_row['PR']})

    combined_df = pd.DataFrame(merged_rows)
    combined_df = combined_df.sort_values('Date').reset_index(drop=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to {output_file} with {len(combined_df)} rows.")
    return combined_df


def plot_pr_evolution(df: pd.DataFrame, start_date: str = '2019-07-01', 
                     end_date: str = '2022-03-24', output_file: str = 'output/pr_evolution.png'):
    df = df[(df['Date'] >= pd.to_datetime(start_date)) & 
            (df['Date'] <= pd.to_datetime(end_date))].copy()

    if df.empty:
        raise ValueError("No data available in the specified date range.")

    df['PR_MA30'] = df['PR'].rolling(window=30, min_periods=1).mean()

    df['Budget_PR'] = 73.9
    for year in range(2019, 2023):
        start = f'{year}-07-01'
        end = f'{year+1}-06-30'
        mask = (df['Date'] >= pd.to_datetime(start)) & (df['Date'] <= pd.to_datetime(end))
        df.loc[mask, 'Budget_PR'] = 73.9 * (0.992 ** (year - 2019))

    def get_color(ghi):
        if ghi < 2:
            return 'navy'
        elif 2 <= ghi < 4:
            return 'lightblue'
        elif 4 <= ghi < 6:
            return 'orange'
        else:
            return 'brown'

    df['Color'] = df['GHI'].apply(get_color)

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='Date', y='PR', hue='Color', palette=list(df['Color'].unique()),
                    legend=False, size=30, sizes=(30, 30))
    plt.plot(df['Date'], df['PR_MA30'], color='red', label='30-day Moving Average')
    plt.plot(df['Date'], df['Budget_PR'], color='darkgreen', label='Budget PR')

    last_date = df['Date'].max()
    periods = [7, 30, 60]
    text = []
    for period in periods:
        recent_data = df[df['Date'] > (last_date - timedelta(days=period))]
        avg_pr = recent_data['PR'].mean() if not recent_data.empty else 0
        text.append(f'Avg PR (last {period} days): {avg_pr:.2f}')

    plt.text(0.98, 0.02, '\n'.join(text), transform=plt.gca().transAxes, 
             verticalalignment='bottom', horizontalalignment='right', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.title('Performance Ratio Evolution')
    plt.xlabel('Date')
    plt.ylabel('Performance Ratio (%)')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Process and visualize PR and GHI data.')
    parser.add_argument('--pr_dir', default='PR', help='Path to PR data directory')
    parser.add_argument('--ghi_dir', default='GHI', help='Path to GHI data directory')
    parser.add_argument('--output_csv', default='output/combined_data.csv', help='Output CSV file path')
    parser.add_argument('--output_plot', default='output/pr_evolution.png', help='Output plot file path')
    parser.add_argument('--start_date', default='2019-07-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', default='2022-03-24', help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)

    df = process_data(args.pr_dir, args.ghi_dir, args.output_csv)

    plot_pr_evolution(df, args.start_date, args.end_date, args.output_plot)

if __name__ == '__main__':
    main()