import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Loyalty Retention Dashboard", layout="wide")

# ---------- Load Data ----------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    path = os.path.join(BASE_DIR, "..", "data", "processed", "customer_segments_final.csv")
    df = pd.read_csv(path)
    return df

df = load_data()

# ---------- Friendly segment names ----------
segment_names = {
    'segment_0': 'Loyal Frequent Flyers',
    '1a_New_Member': 'New Members',
    '1b_Lapsed_Critical': 'Lapsed / Critical Risk',
    'segment_2': 'Engaged Redeemers',
    'segment_3': 'Point Hoarders'
}
df['Segment Name'] = df['final_segment'].map(segment_names)

# ---------- Risk label ----------
def risk_label(score):
    if score == -1:
        return "New Member - Not Yet Scorable"
    elif score >= 0.5:
        return "High Risk"
    elif score >= 0.25:
        return "Medium Risk"
    else:
        return "Low Risk"

df['Risk Label'] = df['churn_risk'].apply(risk_label)
df['Churn Risk %'] = df['churn_risk'].apply(lambda x: "N/A" if x == -1 else f"{x:.1%}")

# ---------- Header ----------
st.title("✈️ Airline Loyalty Retention Dashboard")
st.markdown("Identify at-risk customers and recommended retention actions at a glance.")

# ---------- Top-level metrics ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Members", f"{len(df):,}")
col2.metric("Critical Risk Members", f"{(df['priority']=='Critical').sum():,}")
col3.metric("Avg CLV", f"${df['CLV'].mean():,.0f}")
col4.metric("High Churn Risk (Model)", f"{(df['churn_risk']>=0.5).sum():,}")

st.divider()

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")
priority_filter = st.sidebar.multiselect(
    "Priority Level",
    options=df['priority'].unique(),
    default=df['priority'].unique()
)
segment_filter = st.sidebar.multiselect(
    "Segment",
    options=df['Segment Name'].unique(),
    default=df['Segment Name'].unique()
)
risk_filter = st.sidebar.multiselect(
    "Churn Risk Level (Model)",
    options=df['Risk Label'].unique(),
    default=df['Risk Label'].unique()
)

filtered_df = df[
    (df['priority'].isin(priority_filter)) &
    (df['Segment Name'].isin(segment_filter)) &
    (df['Risk Label'].isin(risk_filter))
]

# ---------- Overview Charts ----------
st.subheader("Segment Overview")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    seg_counts = filtered_df['Segment Name'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    fig1 = px.bar(seg_counts, x='Segment', y='Count', title="Customers per Segment", color='Segment')
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    risk_counts = filtered_df[filtered_df['churn_risk'] >= 0]['Risk Label'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']
    fig2 = px.pie(risk_counts, names='Risk Level', values='Count', title="Churn Risk Breakdown (Model)",
                   color='Risk Level',
                   color_discrete_map={'High Risk': '#D62728', 'Medium Risk': '#FF7F0E', 'Low Risk': '#2CA02C'})
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------- Action Plan Table ----------
st.subheader("Recommended Actions by Segment")
action_summary = df.groupby(['Segment Name', 'priority', 'recommended_action']).agg(
    Customer_Count=('Loyalty Number', 'count'),
    Avg_Churn_Risk=('churn_risk', lambda x: x[x >= 0].mean())
).reset_index()
action_summary['Avg_Churn_Risk'] = action_summary['Avg_Churn_Risk'].apply(
    lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
)
st.dataframe(action_summary, use_container_width=True)

st.divider()

# ---------- Highest Priority Customers Table ----------
st.subheader("⚠️ Top 20 Highest Churn Risk Customers (Action Needed)")
top_risk = df[df['churn_risk'] >= 0].sort_values('churn_risk', ascending=False).head(20)
st.dataframe(
    top_risk[['Loyalty Number', 'Segment Name', 'Churn Risk %', 'CLV', 'tenure_months', 'recommended_action']],
    use_container_width=True
)

st.divider()

# ---------- Customer-level lookup ----------
st.subheader("🔍 Customer Lookup")
search_id = st.text_input("Enter Loyalty Number to look up a customer:")

if search_id:
    try:
        customer = df[df['Loyalty Number'] == int(search_id)]
        if not customer.empty:
            c = customer.iloc[0]
            st.success(f"Customer {search_id} found")
            cc1, cc2, cc3, cc4 = st.columns(4)
            cc1.metric("Segment", c['Segment Name'])
            cc2.metric("CLV", f"${c['CLV']:,.0f}")
            cc3.metric("Priority", c['priority'])
            cc4.metric("Churn Risk", c['Churn Risk %'])
            st.info(f"**Recommended Action:** {c['recommended_action']}")
            st.write(f"Months since last flight (2017): {c['months_since_last_flight_2017']}")
            st.write(f"Tenure: {c['tenure_months']} months")
        else:
            st.warning("Loyalty Number not found.")
    except ValueError:
        st.error("Please enter a valid numeric Loyalty Number.")

st.divider()

# ---------- Full filtered table ----------
st.subheader("Full Customer List (filtered)")
display_cols = ['Loyalty Number', 'Segment Name', 'priority', 'Risk Label', 'Churn Risk %', 'CLV', 'tenure_months',
                 'months_since_last_flight_2017', 'recommended_action']
st.dataframe(
    filtered_df.sort_values('churn_risk', ascending=False)[display_cols],
    use_container_width=True
)