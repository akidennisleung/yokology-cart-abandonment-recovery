#!/usr/bin/env python3
"""Parse GA4 User Explorer CSV with column-shift correction.

Usage:
    python parse_ga4_csv.py <ga4_csv_path> <output_csv_path>

GA4 Exploration CSV has a known column-shift bug:
  - The User ID occupies the first unnamed column (index position)
  - All subsequent column headers are shifted left by one position
  - This script corrects the mapping and outputs a clean Parquet file

Correct mapping (data position -> actual meaning):
  Col 0 (unnamed/index) = user_id
  Col 1 (header: Effective user ID) = stream_name
  Col 2 (header: Stream name) = namespace_id
  Col 3 (header: Namespace ID) = event_count
  Col 4 (header: Event count) = sessions
  Col 5 (header: Sessions) = avg_session_duration
  Col 6 (header: Avg session duration) = purchase_revenue
  Col 7 (header: Purchase revenue) = transactions
  Col 8 (header: Transactions) = active_users
  Col 9 (header: Active users) = key_events
"""
import sys
import csv
import pandas as pd
import re


CORRECT_HEADERS = [
    'user_id', 'stream_name', 'namespace_id', 'event_count', 'sessions',
    'avg_session_duration', 'purchase_revenue', 'transactions',
    'active_users', 'key_events', 'label'
]

NUMERIC_COLS = [
    'event_count', 'sessions', 'avg_session_duration',
    'purchase_revenue', 'transactions', 'active_users', 'key_events'
]


def parse_ga4_csv(csv_path: str) -> pd.DataFrame:
    """Parse GA4 User Explorer CSV with column-shift correction."""
    rows = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        skip_header = True
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            if skip_header:
                skip_header = False
                continue
            rows.append(row)

    df = pd.DataFrame(rows, columns=CORRECT_HEADERS[:len(rows[0])])

    # Convert numeric columns
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Clean user_id
    df['user_id'] = df['user_id'].astype(str).str.strip()

    # Filter: valid 24-char hex Shopline IDs only
    df['is_shopline_id'] = df['user_id'].str.match(r'^[0-9a-f]{24}$', na=False)
    shopline_df = df[df['is_shopline_id']].copy()

    # Filter: ysrecipes stream only
    shopline_df = shopline_df[shopline_df['stream_name'].str.contains('ysrecipes', na=False)].copy()

    # Remove grand total / summary rows
    shopline_df = shopline_df[~shopline_df['user_id'].str.contains('total', case=False, na=False)]

    print(f"[parse_ga4_csv] Raw rows: {len(rows)}")
    print(f"[parse_ga4_csv] Valid Shopline IDs (ysrecipes): {len(shopline_df)}")
    return shopline_df


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <ga4_csv_path> <output_parquet_path>")
        sys.exit(1)
    result = parse_ga4_csv(sys.argv[1])
    result.to_csv(sys.argv[2], index=False)
    print(f"[parse_ga4_csv] Saved {len(result)} rows to {sys.argv[2]}")
