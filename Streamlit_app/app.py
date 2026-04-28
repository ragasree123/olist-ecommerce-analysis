import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="Olist E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv(
        'Streamlit_app/data/orders_delivered.csv',
        parse_dates=[
            'order_purchase_timestamp',
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]
    )
    reviews = pd.read_csv(
        'Streamlit_app/data/reviews_with_delay.csv'
    )
    states = pd.read_csv(
        'Streamlit_app/data/state_revenue.csv'
    )
    return orders, reviews, states

# ── Sidebar ───────────────────────────────────────────
st.sidebar.title("🔍 Filters")

selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(orders['customer_state'].dropna().unique()),
    default=[]
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(
        orders['product_category_name_english'].dropna().unique()
    ),
    default=[]
)

# Apply filters
filtered = orders.copy()
if selected_states:
    filtered = filtered[
        filtered['customer_state'].isin(selected_states)
    ]
if selected_categories:
    filtered = filtered[
        filtered['product_category_name_english'].isin(
            selected_categories
        )
    ]

# ── Title ─────────────────────────────────────────────
st.title("🛒 Olist E-commerce Analysis Dashboard")
st.markdown(
    "Analysing **100,000+ real orders** from Brazil's "
    "largest marketplace (2016–2018)"
)
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_orders_all = len(orders)
total_rev_all = orders['price'].sum()
avg_delay_all = orders['delivery_delay_days'].mean()
late_pct_all = (orders['delivery_delay_days'] > 0).mean() * 100

with col1:
    delta_orders = len(filtered) - total_orders_all
    st.metric(
        label="Total Orders",
        value=f"{len(filtered):,}",
        delta=f"{delta_orders:,} vs full dataset"
        if selected_states or selected_categories else None
    )
with col2:
    total_rev = filtered['price'].sum()
    delta_rev = total_rev - total_rev_all
    st.metric(
        label="Total Revenue",
        value=f"R${total_rev/1e6:.2f}M",
        delta=f"R${delta_rev/1e6:.2f}M vs full dataset"
        if selected_states or selected_categories else None
    )
with col3:
    avg_delay = filtered['delivery_delay_days'].mean()
    delta_delay = avg_delay - avg_delay_all
    st.metric(
        label="Avg Delay (days)",
        value=f"{avg_delay:.1f}",
        delta=f"{delta_delay:.1f} vs full dataset"
        if selected_states or selected_categories else None
    )
with col4:
    late_pct = (
        filtered['delivery_delay_days'] > 0
    ).mean() * 100
    delta_late = late_pct - late_pct_all
    st.metric(
        label="Late Order %",
        value=f"{late_pct:.1f}%",
        delta=f"{delta_late:.1f}% vs full dataset"
        if selected_states or selected_categories else None
    )

st.markdown("---")

# ── Charts Row 1 ──────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Categories by Revenue")
    cat_data = filtered.groupby(
        'product_category_name_english'
    )['price'].sum().reset_index()
    cat_data.columns = ['category', 'revenue']
    cat_data = cat_data.nlargest(10, 'revenue')
    cat_data = cat_data.sort_values('revenue')

    fig1 = px.bar(
        cat_data,
        x='revenue',
        y='category',
        orientation='h',
        color='revenue',
        color_continuous_scale=['#E24B4A', '#EF9F27', '#1D9E75'],
        labels={'revenue': 'Revenue (R$)', 'category': ''},
        title='Top 10 Categories by Revenue'
    )
    fig1.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Monthly Revenue Trend")
    monthly_filtered = filtered.copy()
    monthly_filtered['year_month'] = pd.to_datetime(
        monthly_filtered['order_purchase_timestamp']
    ).dt.to_period('M').dt.to_timestamp()

    monthly_data = monthly_filtered.groupby(
        'year_month'
    )['price'].sum().reset_index()
    monthly_data.columns = ['month', 'revenue']

    fig2 = px.area(
        monthly_data,
        x='month',
        y='revenue',
        labels={'month': 'Month', 'revenue': 'Revenue (R$)'},
        title='Monthly Revenue Trend 2016-2018',
        color_discrete_sequence=['#1D9E75']
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Charts Row 2 ──────────────────────────────────────
col3a, col3b = st.columns(2)

with col3a:
    st.subheader("Late Order % by Category")
    late_data = filtered.copy()
    late_data['is_late'] = (
        late_data['delivery_delay_days'] > 0
    ).astype(int)

    late_by_cat = late_data.groupby(
        'product_category_name_english'
    ).agg(
        total=('order_id', 'count'),
        late=('is_late', 'sum')
    ).reset_index()

    late_by_cat = late_by_cat[late_by_cat['total'] >= 100]
    late_by_cat['late_pct'] = (
        late_by_cat['late'] / late_by_cat['total'] * 100
    ).round(1)
    late_by_cat = late_by_cat.nlargest(
        10, 'late_pct'
    ).sort_values('late_pct')

    fig3 = px.bar(
        late_by_cat,
        x='late_pct',
        y='product_category_name_english',
        orientation='h',
        color='late_pct',
        color_continuous_scale=['#EF9F27', '#E24B4A'],
        labels={
            'late_pct': 'Late order rate (%)',
            'product_category_name_english': ''
        },
        title='Top 10 Categories — Highest Late Rate'
    )
    fig3.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

with col3b:
    st.subheader("Review Score Distribution")
    rev_data = filtered.merge(
        reviews[['order_id', 'review_score']],
        on='order_id',
        how='left'
    ).dropna(subset=['review_score'])

    score_counts = rev_data['review_score'].value_counts(
    ).sort_index().reset_index()
    score_counts.columns = ['score', 'count']

    colour_map = {
        1: '#E24B4A',
        2: '#E24B4A',
        3: '#EF9F27',
        4: '#378ADD',
        5: '#1D9E75'
    }
    score_counts['color'] = score_counts['score'].map(
        colour_map
    )

    fig4 = px.bar(
        score_counts,
        x='score',
        y='count',
        color='score',
        color_discrete_map={
            1: '#E24B4A',
            2: '#E24B4A',
            3: '#EF9F27',
            4: '#378ADD',
            5: '#1D9E75'
        },
        labels={
            'score': 'Review Score (1-5)',
            'count': 'Number of orders'
        },
        title='Review Score Distribution'
    )
    fig4.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Data Table + Download ──────────────────────────────
st.subheader("📋 Raw Data")

show_data = st.checkbox(
    "Show filtered data table", value=False
)

if show_data:
    display_cols = [
        'order_id',
        'product_category_name_english',
        'customer_state',
        'price',
        'freight_value',
        'delivery_delay_days',
        'order_status'
    ]
    st.dataframe(
        filtered[display_cols].head(500),
        use_container_width=True
    )

# Download button
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download filtered data as CSV",
    data=csv,
    file_name='olist_filtered_data.csv',
    mime='text/csv'
)

st.markdown("---")
st.caption(
    "Data source: Olist Brazilian E-commerce Dataset "
    "(Kaggle) · Built by Ragasree"
)