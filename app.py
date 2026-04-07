"""
Marketing Analytics Dashboard
Senior Marketing Analyst Assignment

This dashboard unifies and visualizes advertising data from Facebook, Google, and TikTok platforms.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load and unify all advertising data from CSV files."""
    data_dir = Path(__file__).parent

    # Load Facebook Ads data
    fb_df = pd.read_csv(data_dir / "01_facebook_ads.csv")
    fb_df['platform'] = 'Facebook'
    fb_df = fb_df.rename(columns={
        'spend': 'cost',
        'ad_set_id': 'ad_group_id',
        'ad_set_name': 'ad_group_name'
    })

    # Load Google Ads data
    google_df = pd.read_csv(data_dir / "02_google_ads.csv")
    google_df['platform'] = 'Google'

    # Load TikTok Ads data
    tiktok_df = pd.read_csv(data_dir / "03_tiktok_ads.csv")
    tiktok_df['platform'] = 'TikTok'
    # Rename columns for consistency
    tiktok_df = tiktok_df.rename(columns={
        'adgroup_id': 'ad_group_id',
        'adgroup_name': 'ad_group_name'
    })

    return fb_df, google_df, tiktok_df

def create_unified_data(fb_df, google_df, tiktok_df):
    """Create a unified dataset with standardized columns."""

    # Standardize Facebook data
    fb_unified = pd.DataFrame({
        'date': pd.to_datetime(fb_df['date']),
        'platform': 'Facebook',
        'campaign_id': fb_df['campaign_id'],
        'campaign_name': fb_df['campaign_name'],
        'ad_group_id': fb_df['ad_group_id'],
        'ad_group_name': fb_df['ad_group_name'],
        'impressions': fb_df['impressions'],
        'clicks': fb_df['clicks'],
        'cost': fb_df['cost'],
        'conversions': fb_df['conversions'],
        'ctr': fb_df['engagement_rate'],  # Using engagement_rate as CTR equivalent
        'conversion_value': fb_df['conversions'] * 50,  # Estimated conversion value
        'video_views': fb_df['video_views'],
        'reach': fb_df['reach'],
    })

    # Standardize Google data
    google_unified = pd.DataFrame({
        'date': pd.to_datetime(google_df['date']),
        'platform': 'Google',
        'campaign_id': google_df['campaign_id'],
        'campaign_name': google_df['campaign_name'],
        'ad_group_id': google_df['ad_group_id'],
        'ad_group_name': google_df['ad_group_name'],
        'impressions': google_df['impressions'],
        'clicks': google_df['clicks'],
        'cost': google_df['cost'],
        'conversions': google_df['conversions'],
        'ctr': google_df['ctr'],
        'conversion_value': google_df['conversion_value'],
        'video_views': 0,  # Google doesn't have video views in this dataset
        'reach': google_df['impressions'] * 0.8,  # Estimated reach
    })

    # Standardize TikTok data
    tiktok_unified = pd.DataFrame({
        'date': pd.to_datetime(tiktok_df['date']),
        'platform': 'TikTok',
        'campaign_id': tiktok_df['campaign_id'],
        'campaign_name': tiktok_df['campaign_name'],
        'ad_group_id': tiktok_df['ad_group_id'],
        'ad_group_name': tiktok_df['ad_group_name'],
        'impressions': tiktok_df['impressions'],
        'clicks': tiktok_df['clicks'],
        'cost': tiktok_df['cost'],
        'conversions': tiktok_df['conversions'],
        'ctr': tiktok_df['clicks'] / tiktok_df['impressions'],  # Calculate CTR
        'conversion_value': tiktok_df['conversions'] * 40,  # Estimated conversion value
        'video_views': tiktok_df['video_views'],
        'reach': tiktok_df['impressions'] * 0.75,  # Estimated reach
    })

    # Combine all platforms
    unified_df = pd.concat([fb_unified, google_unified, tiktok_unified], ignore_index=True)

    # Calculate additional metrics
    unified_df['cpm'] = (unified_df['cost'] / unified_df['impressions']) * 1000
    unified_df['cpc'] = unified_df['cost'] / unified_df['clicks']
    unified_df['cpa'] = unified_df['cost'] / unified_df['conversions']
    unified_df['roas'] = unified_df['conversion_value'] / unified_df['cost']

    # Fill NaN values
    unified_df = unified_df.fillna(0)

    return unified_df

def create_database(unified_df):
    """Create SQLite database with unified data."""
    conn = sqlite3.connect('marketing_data.db')
    unified_df.to_sql('unified_ads', conn, if_exists='replace', index=False)
    conn.close()
    return True

# Load data
fb_df, google_df, tiktok_df = load_data()
unified_df = create_unified_data(fb_df, google_df, tiktok_df)

# Create database
create_database(unified_df)

# Dashboard Title
st.markdown('<p class="main-header">📊 Marketing Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown("**Cross-Channel Performance Analysis** | Facebook, Google & TikTok Ads")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(unified_df['date'].min().date(), unified_df['date'].max().date()),
    min_value=unified_df['date'].min().date(),
    max_value=unified_df['date'].max().date()
)

platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=['Facebook', 'Google', 'TikTok'],
    default=['Facebook', 'Google', 'TikTok']
)

campaigns = st.sidebar.multiselect(
    "Select Campaigns",
    options=sorted(unified_df['campaign_name'].unique()),
    default=sorted(unified_df['campaign_name'].unique())
)

# Filter data
if len(date_range) == 2:
    mask = (unified_df['date'].dt.date >= date_range[0]) & (unified_df['date'].dt.date <= date_range[1])
    filtered_df = unified_df[mask]
else:
    filtered_df = unified_df

filtered_df = filtered_df[
    (filtered_df['platform'].isin(platforms)) &
    (filtered_df['campaign_name'].isin(campaigns))
]

# Key Metrics Section
st.header("Key Performance Indicators", divider="blue")

col1, col2, col3, col4, col5 = st.columns(5)

total_spend = filtered_df['cost'].sum()
total_impressions = filtered_df['impressions'].sum()
total_clicks = filtered_df['clicks'].sum()
total_conversions = filtered_df['conversions'].sum()
total_revenue = filtered_df['conversion_value'].sum()

with col1:
    st.metric("Total Spend", f"${total_spend:,.2f}")

with col2:
    st.metric("Total Impressions", f"{total_impressions:,.0f}")

with col3:
    st.metric("Total Clicks", f"{total_clicks:,.0f}")

with col4:
    st.metric("Total Conversions", f"{total_conversions:,.0f}")

with col5:
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

# Secondary Metrics
col1, col2, col3, col4 = st.columns(4)

avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
avg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
avg_roas = (total_revenue / total_spend) if total_spend > 0 else 0

with col1:
    st.metric("Avg CTR", f"{avg_ctr:.2f}%")

with col2:
    st.metric("Avg CPC", f"${avg_cpc:.2f}")

with col3:
    st.metric("Avg CPA", f"${avg_cpa:.2f}")

with col4:
    st.metric("ROAS", f"{avg_roas:.2f}x")

st.divider()

# Platform Performance Comparison
st.header("Platform Performance Comparison", divider="blue")

platform_metrics = filtered_df.groupby('platform').agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'conversion_value': 'sum'
}).reset_index()

platform_metrics['CTR'] = (platform_metrics['clicks'] / platform_metrics['impressions'] * 100).round(2)
platform_metrics['CPA'] = (platform_metrics['cost'] / platform_metrics['conversions']).round(2)
platform_metrics['ROAS'] = (platform_metrics['conversion_value'] / platform_metrics['cost']).round(2)

col1, col2 = st.columns(2)

with col1:
    # Spend by Platform
    fig_spend = px.bar(
        platform_metrics,
        x='platform',
        y='cost',
        title='Total Spend by Platform',
        color='platform',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'},
        text='cost'
    )
    fig_spend.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig_spend.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_spend, use_container_width=True)

with col2:
    # Conversions by Platform
    fig_conv = px.bar(
        platform_metrics,
        x='platform',
        y='conversions',
        title='Total Conversions by Platform',
        color='platform',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'},
        text='conversions'
    )
    fig_conv.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig_conv.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_conv, use_container_width=True)

# Performance Metrics Table
st.subheader("Platform Metrics Summary")
st.dataframe(
    platform_metrics[['platform', 'cost', 'impressions', 'clicks', 'conversions', 'CTR', 'CPA', 'ROAS']].style.format({
        'cost': '${:,.2f}',
        'impressions': '{:,.0f}',
        'clicks': '{:,.0f}',
        'conversions': '{:,.0f}',
        'CTR': '{:.2f}%',
        'CPA': '${:.2f}',
        'ROAS': '{:.2f}x'
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# Time Series Analysis
st.header("Trend Analysis", divider="blue")

daily_metrics = filtered_df.groupby(['date', 'platform']).agg({
    'cost': 'sum',
    'conversions': 'sum',
    'clicks': 'sum',
    'impressions': 'sum'
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    # Daily Spend Trend
    fig_trend = px.line(
        daily_metrics,
        x='date',
        y='cost',
        color='platform',
        title='Daily Spend by Platform',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_trend.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    # Daily Conversions Trend
    fig_conv_trend = px.line(
        daily_metrics,
        x='date',
        y='conversions',
        color='platform',
        title='Daily Conversions by Platform',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_conv_trend.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_conv_trend, use_container_width=True)

st.divider()

# Campaign Performance Analysis
st.header("Campaign Performance Analysis", divider="blue")

campaign_metrics = filtered_df.groupby(['platform', 'campaign_name']).agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'conversion_value': 'sum'
}).reset_index()

campaign_metrics['CTR'] = (campaign_metrics['clicks'] / campaign_metrics['impressions'] * 100).round(2)
campaign_metrics['CPA'] = (campaign_metrics['cost'] / campaign_metrics['conversions']).round(2)
campaign_metrics['ROAS'] = (campaign_metrics['conversion_value'] / campaign_metrics['cost']).round(2)

# Top Campaigns by Conversions
col1, col2 = st.columns(2)

with col1:
    top_campaigns = campaign_metrics.nlargest(10, 'conversions')
    fig_top = px.bar(
        top_campaigns,
        x='conversions',
        y='campaign_name',
        color='platform',
        orientation='h',
        title='Top 10 Campaigns by Conversions',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_top.update_layout(height=500)
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    # ROAS by Campaign
    fig_roas = px.scatter(
        campaign_metrics,
        x='cost',
        y='ROAS',
        size='conversions',
        color='platform',
        hover_name='campaign_name',
        title='ROAS vs Spend (bubble size = conversions)',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_roas.update_layout(height=500)
    st.plotly_chart(fig_roas, use_container_width=True)

# Campaign Performance Table
st.subheader("All Campaigns Performance")
st.dataframe(
    campaign_metrics.sort_values('conversions', ascending=False).style.format({
        'cost': '${:,.2f}',
        'impressions': '{:,.0f}',
        'clicks': '{:,.0f}',
        'conversions': '{:,.0f}',
        'conversion_value': '${:,.2f}',
        'CTR': '{:.2f}%',
        'CPA': '${:.2f}',
        'ROAS': '{:.2f}x'
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# Cost Efficiency Analysis
st.header("Cost Efficiency Analysis", divider="blue")

col1, col2 = st.columns(2)

with col1:
    # CPM vs CPA scatter
    fig_eff = px.scatter(
        campaign_metrics,
        x='CPA',
        y='cost',
        color='platform',
        size='conversions',
        hover_name='campaign_name',
        title='CPA vs Total Spend',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_eff.update_layout(height=400)
    st.plotly_chart(fig_eff, use_container_width=True)

with col2:
    # Click Distribution
    click_dist = filtered_df.groupby('platform')['clicks'].sum().reset_index()
    fig_pie = px.pie(
        click_dist,
        values='clicks',
        names='platform',
        title='Click Distribution by Platform',
        color='platform',
        color_discrete_map={'Facebook': '#1877F2', 'Google': '#4285F4', 'TikTok': '#000000'}
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Key Insights Section
st.header("Key Insights & Recommendations", divider="blue")

# Calculate insights
best_platform_roas = platform_metrics.loc[platform_metrics['ROAS'].idxmax()]
best_platform_conv = platform_metrics.loc[platform_metrics['conversions'].idxmax()]
lowest_cpa_platform = platform_metrics.loc[platform_metrics['CPA'].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top Performers")
    st.write(f"**Best ROAS Platform:** {best_platform_roas['platform']} ({best_platform_roas['ROAS']:.2f}x)")
    st.write(f"**Most Conversions Platform:** {best_platform_conv['platform']} ({best_platform_conv['conversions']:,.0f} conversions)")
    st.write(f"**Lowest CPA Platform:** {lowest_cpa_platform['platform']} (${lowest_cpa_platform['CPA']:.2f})")

    # Top performing campaign
    top_campaign = campaign_metrics.loc[campaign_metrics['conversions'].idxmax()]
    st.write(f"**Top Campaign:** {top_campaign['campaign_name']} ({top_campaign['conversions']:,.0f} conversions)")

with col2:
    st.subheader("💡 Recommendations")

    # Generate recommendations based on data
    recommendations = []

    if best_platform_roas['ROAS'] > 2:
        recommendations.append(f"✅ Scale up spend on {best_platform_roas['platform']} - strong ROAS of {best_platform_roas['ROAS']:.2f}x")

    if lowest_cpa_platform['CPA'] < 20:
        recommendations.append(f"✅ {lowest_cpa_platform['platform']} has efficient CPA at ${lowest_cpa_platform['CPA']:.2f} - consider increasing budget")

    # Find underperforming campaigns
    low_roas_campaigns = campaign_metrics[campaign_metrics['ROAS'] < 1]
    if len(low_roas_campaigns) > 0:
        recommendations.append(f"⚠️ {len(low_roas_campaigns)} campaigns have ROAS < 1x - review targeting and creative")

    # Find high potential campaigns
    high_conv_low_cost = campaign_metrics[(campaign_metrics['conversions'] > campaign_metrics['conversions'].median()) &
                                           (campaign_metrics['cost'] < campaign_metrics['cost'].median())]
    if len(high_conv_low_cost) > 0:
        recommendations.append(f"🎯 {len(high_conv_low_cost)} campaigns show high efficiency - good scaling candidates")

    for rec in recommendations:
        st.write(rec)

st.divider()

# Data Export Section
st.header("Data Export", divider="blue")

col1, col2, col3 = st.columns(3)

with col1:
    csv = unified_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Unified Data (CSV)",
        data=csv,
        file_name='unified_marketing_data.csv',
        mime='text/csv'
    )

with col2:
    # Download platform comparison
    csv_platform = platform_metrics.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Platform Metrics (CSV)",
        data=csv_platform,
        file_name='platform_metrics.csv',
        mime='text/csv'
    )

with col3:
    # Download campaign metrics
    csv_campaign = campaign_metrics.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Campaign Metrics (CSV)",
        data=csv_campaign,
        file_name='campaign_metrics.csv',
        mime='text/csv'
    )

# Footer
st.divider()
st.markdown("""
**Marketing Analytics Dashboard** | Built with Streamlit
*Data Sources: Facebook Ads, Google Ads, TikTok Ads*
*Assignment: Senior Marketing Analyst Technical Assignment*
""")