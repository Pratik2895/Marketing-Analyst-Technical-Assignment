"""
Quality check utility for the Marketing Analytics Dashboard.
Run this file to validate that source data and dashboard metrics are consistent.
"""

import sys
import pandas as pd
import numpy as np
from app import create_unified_data, load_data

EXPECTED_COLUMNS = {
    'Facebook': [
        'date', 'campaign_id', 'campaign_name', 'ad_set_id', 'ad_set_name',
        'impressions', 'clicks', 'spend', 'conversions', 'engagement_rate',
        'video_views', 'reach', 'frequency'
    ],
    'Google': [
        'date', 'campaign_id', 'campaign_name', 'ad_group_id', 'ad_group_name',
        'impressions', 'clicks', 'cost', 'conversions', 'conversion_value',
        'ctr', 'avg_cpc', 'quality_score', 'search_impression_share'
    ],
    'TikTok': [
        'date', 'campaign_id', 'campaign_name', 'adgroup_id', 'adgroup_name',
        'impressions', 'clicks', 'cost', 'conversions', 'video_views',
        'video_watch_25', 'video_watch_50', 'video_watch_75', 'video_watch_100',
        'likes', 'shares', 'comments'
    ]
}

UNIFIED_COLUMNS = [
    'date', 'platform', 'campaign_id', 'campaign_name', 'ad_group_id',
    'ad_group_name', 'impressions', 'clicks', 'cost', 'conversions', 'ctr',
    'conversion_value', 'video_views', 'reach', 'cpm', 'cpc', 'cpa', 'roas'
]


def validate_columns(df: pd.DataFrame, expected: list[str], name: str) -> bool:
    missing = [col for col in expected if col not in df.columns]
    extra = [col for col in df.columns if col not in expected]

    if missing:
        print(f"ERROR: {name} is missing expected columns: {missing}")
    if extra:
        print(f"WARNING: {name} has extra columns: {extra}")

    return len(missing) == 0


def validate_non_negative(df: pd.DataFrame, columns: list[str], name: str) -> bool:
    negative = {}
    for column in columns:
        if column in df.columns:
            invalid = df[df[column] < 0]
            if not invalid.empty:
                negative[column] = len(invalid)

    if negative:
        print(f"ERROR: {name} contains negative values:")
        for column, count in negative.items():
            print(f"  - {column}: {count} rows")
        return False
    return True


def validate_metric_formula(raw_dfs: dict[str, pd.DataFrame], unified_df: pd.DataFrame) -> bool:
    errors = []

    fb_df = raw_dfs['Facebook']
    google_df = raw_dfs['Google']
    tiktok_df = raw_dfs['TikTok']

    fb_expected = pd.DataFrame({
        'ctr': fb_df['engagement_rate'],
        'cpm': np.where(fb_df['impressions'] > 0, fb_df['spend'] / fb_df['impressions'] * 1000, 0),
        'cpc': np.where(fb_df['clicks'] > 0, fb_df['spend'] / fb_df['clicks'], 0),
        'cpa': np.where(fb_df['conversions'] > 0, fb_df['spend'] / fb_df['conversions'], 0),
        'roas': np.where(fb_df['spend'] > 0, (fb_df['conversions'] * 50) / fb_df['spend'], 0)
    })

    google_expected = pd.DataFrame({
        'ctr': google_df['ctr'],
        'cpm': np.where(google_df['impressions'] > 0, google_df['cost'] / google_df['impressions'] * 1000, 0),
        'cpc': np.where(google_df['clicks'] > 0, google_df['cost'] / google_df['clicks'], 0),
        'cpa': np.where(google_df['conversions'] > 0, google_df['cost'] / google_df['conversions'], 0),
        'roas': np.where(google_df['cost'] > 0, google_df['conversion_value'] / google_df['cost'], 0)
    })

    tiktok_expected = pd.DataFrame({
        'ctr': np.where(tiktok_df['impressions'] > 0, tiktok_df['clicks'] / tiktok_df['impressions'], 0),
        'cpm': np.where(tiktok_df['impressions'] > 0, tiktok_df['cost'] / tiktok_df['impressions'] * 1000, 0),
        'cpc': np.where(tiktok_df['clicks'] > 0, tiktok_df['cost'] / tiktok_df['clicks'], 0),
        'cpa': np.where(tiktok_df['conversions'] > 0, tiktok_df['cost'] / tiktok_df['conversions'], 0),
        'roas': np.where(tiktok_df['cost'] > 0, (tiktok_df['conversions'] * 40) / tiktok_df['cost'], 0)
    })

    expected = pd.concat([fb_expected, google_expected, tiktok_expected], ignore_index=True)
    expected = expected.reset_index(drop=True)
    actual = unified_df[['ctr', 'cpm', 'cpc', 'cpa', 'roas']].reset_index(drop=True)

    for metric in ['ctr', 'cpm', 'cpc', 'cpa', 'roas']:
        mismatch = actual[~np.isclose(actual[metric].fillna(0), expected[metric].fillna(0), atol=1e-6)]
        if not mismatch.empty:
            errors.append((metric, len(mismatch)))

    if errors:
        print("ERROR: Unified data metric formulas do not match expected values:")
        for metric, count in errors:
            print(f"  - {metric}: {count} mismatched rows")
        return False

    return True


def load_raw_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fb_df = pd.read_csv('01_facebook_ads.csv')
    google_df = pd.read_csv('02_google_ads.csv')
    tiktok_df = pd.read_csv('03_tiktok_ads.csv')
    return fb_df, google_df, tiktok_df


def validate_aggregates(raw_dfs: dict[str, pd.DataFrame], unified_df: pd.DataFrame) -> bool:
    errors = []

    raw_totals = {
        'cost': sum(df['cost'].sum() if 'cost' in df.columns else df['spend'].sum() for df in raw_dfs.values()),
        'impressions': sum(df['impressions'].sum() for df in raw_dfs.values()),
        'clicks': sum(df['clicks'].sum() for df in raw_dfs.values()),
        'conversions': sum(df['conversions'].sum() for df in raw_dfs.values())
    }

    unified_totals = {
        'cost': unified_df['cost'].sum(),
        'impressions': unified_df['impressions'].sum(),
        'clicks': unified_df['clicks'].sum(),
        'conversions': unified_df['conversions'].sum()
    }

    for metric, raw_value in raw_totals.items():
        unified_value = unified_totals[metric]
        if not np.isclose(raw_value, unified_value, atol=1e-6):
            errors.append((metric, raw_value, unified_value))

    if errors:
        print("ERROR: Aggregated totals do not match between source data and unified data:")
        for metric, raw_value, unified_value in errors:
            print(f"  - {metric}: raw={raw_value}, unified={unified_value}")
        return False

    return True


def validate_dashboard_metrics(unified_df: pd.DataFrame) -> bool:
    totals = {
        'total_spend': unified_df['cost'].sum(),
        'total_impressions': unified_df['impressions'].sum(),
        'total_clicks': unified_df['clicks'].sum(),
        'total_conversions': unified_df['conversions'].sum(),
        'total_revenue': unified_df['conversion_value'].sum()
    }

    if any(value < 0 for value in totals.values()):
        print("ERROR: Dashboard totals contain negative values.")
        return False

    return True


def run_qc() -> bool:
    print("Running data quality checks...\n")
    fb_raw, google_raw, tiktok_raw = load_raw_data()
    fb_df, google_df, tiktok_df = load_data()
    unified_df = create_unified_data(fb_df, google_df, tiktok_df)

    results = []
    results.append(validate_columns(fb_raw, EXPECTED_COLUMNS['Facebook'], 'Facebook source'))
    results.append(validate_columns(google_raw, EXPECTED_COLUMNS['Google'], 'Google source'))
    results.append(validate_columns(tiktok_raw, EXPECTED_COLUMNS['TikTok'], 'TikTok source'))
    results.append(validate_columns(unified_df, UNIFIED_COLUMNS, 'Unified dataset'))

    results.append(validate_non_negative(fb_raw, ['impressions', 'clicks', 'conversions', 'spend'], 'Facebook source'))
    results.append(validate_non_negative(google_raw, ['impressions', 'clicks', 'conversions', 'cost'], 'Google source'))
    results.append(validate_non_negative(tiktok_raw, ['impressions', 'clicks', 'conversions', 'cost'], 'TikTok source'))
    results.append(validate_non_negative(unified_df, ['impressions', 'clicks', 'conversions', 'cost', 'conversion_value'], 'Unified dataset'))

    results.append(validate_metric_formula({'Facebook': fb_raw, 'Google': google_raw, 'TikTok': tiktok_raw}, unified_df))
    results.append(validate_aggregates({'Facebook': fb_raw, 'Google': google_raw, 'TikTok': tiktok_raw}, unified_df))
    results.append(validate_dashboard_metrics(unified_df))

    print("\nData quality check complete.")
    if all(results):
        print("STATUS: PASS")
        return True
    else:
        print("STATUS: FAIL")
        return False


if __name__ == '__main__':
    ok = run_qc()
    sys.exit(0 if ok else 1)
