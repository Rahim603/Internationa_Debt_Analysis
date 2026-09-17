import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="International Debt Analysis",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("🌍 International Debt Analysis Dashboard")

st.markdown(
    "Interactive analysis of international debt data using "
    "Python, MySQL and Streamlit."
)


# ============================================================
# MYSQL CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mihar@5263",
    database="international_debt",
    connection_timeout=10
)

st.success("✅ Connected to MySQL successfully!")


# ============================================================
# DEBT INDICATOR CONDITION
# ============================================================

debt_condition = "i.series_code LIKE 'DT.%'"


# ============================================================
# EXCLUDE WORLD BANK AGGREGATE / INCOME GROUP ENTRIES
# ============================================================

aggregate_condition = """
AND LOWER(c.country_name) NOT LIKE '%income%'
AND LOWER(c.country_name) NOT LIKE '%ida%'
AND LOWER(c.country_name) NOT LIKE '%east asia%'
AND LOWER(c.country_name) NOT LIKE '%europe & central asia%'
AND LOWER(c.country_name) NOT LIKE '%latin america%'
AND LOWER(c.country_name) NOT LIKE '%south asia%'
AND LOWER(c.country_name) NOT LIKE '%sub-saharan africa%'
AND LOWER(c.country_name) NOT LIKE '%middle east%'
AND LOWER(c.country_name) NOT LIKE '%least developed%'
"""


# ============================================================
# KPI CALCULATIONS
# ============================================================

cursor = conn.cursor()


# Total Countries
cursor.execute("""
    SELECT COUNT(*)
    FROM countries
""")

total_countries = cursor.fetchone()[0]


# Total Debt Indicators
cursor.execute(f"""
    SELECT COUNT(*)
    FROM indicators i
    WHERE {debt_condition}
""")

total_debt_indicators = cursor.fetchone()[0]


# Total Debt Records
cursor.execute(f"""
    SELECT COUNT(*)
    FROM debt_data d
    JOIN indicators i
        ON d.indicator_id = i.indicator_id
    WHERE {debt_condition}
""")

total_debt_records = cursor.fetchone()[0]


# Total Debt Value
cursor.execute(f"""
    SELECT COALESCE(SUM(d.debt_value), 0)
    FROM debt_data d
    JOIN indicators i
        ON d.indicator_id = i.indicator_id
    WHERE {debt_condition}
""")

total_debt = cursor.fetchone()[0]


cursor.close()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "🌍 Total Countries",
    f"{total_countries:,}"
)


col2.metric(
    "📊 Debt Indicators",
    f"{total_debt_indicators:,}"
)


col3.metric(
    "🗂️ Debt Records",
    f"{total_debt_records:,}"
)


col4.metric(
    "💰 Total Debt Value",
    f"${total_debt:,.0f}"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


# ------------------------------------------------------------
# Country Filter
# ------------------------------------------------------------

country_filter_query = f"""
SELECT DISTINCT c.country_name
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {debt_condition}
{aggregate_condition}
ORDER BY c.country_name
"""

country_filter_df = pd.read_sql(
    country_filter_query,
    conn
)


country_options = (
    ["All Countries"]
    + country_filter_df["country_name"].tolist()
)


selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    country_options
)


# ------------------------------------------------------------
# Indicator Filter
# ------------------------------------------------------------

indicator_filter_query = f"""
SELECT DISTINCT i.indicator_name
FROM indicators i
WHERE {debt_condition}
ORDER BY i.indicator_name
"""

indicator_filter_df = pd.read_sql(
    indicator_filter_query,
    conn
)


indicator_options = (
    ["All Debt Indicators"]
    + indicator_filter_df["indicator_name"].tolist()
)


selected_indicator = st.sidebar.selectbox(
    "📊 Select Debt Indicator",
    indicator_options
)


# ============================================================
# CURRENT FILTER SELECTION
# ============================================================

st.subheader("📌 Current Selection")


selection_col1, selection_col2 = st.columns(2)


selection_col1.info(
    f"🌍 Country: {selected_country}"
)


selection_col2.info(
    f"📊 Indicator: {selected_indicator}"
)


# ============================================================
# TOP 10 COUNTRIES BY DEBT VALUE
# ============================================================

st.header("🌍 Top 10 Countries by Debt Value")


country_query = f"""
SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {debt_condition}
{aggregate_condition}
GROUP BY c.country_name
ORDER BY total_debt DESC
LIMIT 10
"""


country_df = pd.read_sql(
    country_query,
    conn
)


fig_country = px.bar(
    country_df,
    x="total_debt",
    y="country_name",
    orientation="h",
    title="Top 10 Countries by Debt Value",
    labels={
        "total_debt": "Debt Value (USD)",
        "country_name": "Country"
    }
)


fig_country.update_layout(
    yaxis={"categoryorder": "total ascending"}
)


st.plotly_chart(
    fig_country,
    use_container_width=True
)


# ============================================================
# TOP 10 DEBT INDICATORS
# ============================================================

st.header("📊 Top 10 Debt Indicators")


indicator_query = f"""
SELECT
    i.indicator_name,
    SUM(d.debt_value) AS total_value
FROM debt_data d
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {debt_condition}
GROUP BY i.indicator_name
ORDER BY total_value DESC
LIMIT 10
"""


indicator_df = pd.read_sql(
    indicator_query,
    conn
)


fig_indicator = px.bar(
    indicator_df,
    x="total_value",
    y="indicator_name",
    orientation="h",
    title="Top 10 Debt Indicators by Total Value",
    labels={
        "total_value": "Total Value (USD)",
        "indicator_name": "Indicator"
    }
)


fig_indicator.update_layout(
    yaxis={"categoryorder": "total ascending"}
)


st.plotly_chart(
    fig_indicator,
    use_container_width=True
)


# ============================================================
# OVERALL YEAR-WISE DEBT TREND
# ============================================================

st.header("📈 Year-wise Debt Trend")


year_query = f"""
SELECT
    d.year,
    SUM(d.debt_value) AS total_debt
FROM debt_data d
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {debt_condition}
GROUP BY d.year
ORDER BY d.year
"""


year_df = pd.read_sql(
    year_query,
    conn
)


fig_year = px.line(
    year_df,
    x="year",
    y="total_debt",
    markers=True,
    title="International Debt Trend by Year",
    labels={
        "year": "Year",
        "total_debt": "Debt Value (USD)"
    }
)


st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ============================================================
# FILTERED DEBT ANALYSIS
# ============================================================

st.header("🔍 Filtered Debt Analysis")


filter_conditions = [debt_condition]
filter_params = []


# Country condition
if selected_country != "All Countries":
    filter_conditions.append(
        "c.country_name = %s"
    )
    filter_params.append(selected_country)


# Indicator condition
if selected_indicator != "All Debt Indicators":
    filter_conditions.append(
        "i.indicator_name = %s"
    )
    filter_params.append(selected_indicator)


where_clause = " AND ".join(filter_conditions)


# ============================================================
# FILTERED TOTAL DEBT
# ============================================================

filtered_total_query = f"""
SELECT
    COALESCE(SUM(d.debt_value), 0)
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {where_clause}
"""


filtered_total_df = pd.read_sql(
    filtered_total_query,
    conn,
    params=filter_params
)


filtered_total = filtered_total_df.iloc[0, 0]


st.metric(
    "💰 Selected Debt Value",
    f"${filtered_total:,.0f}"
)


# ============================================================
# FILTERED YEAR-WISE TREND
# ============================================================

filtered_year_query = f"""
SELECT
    d.year,
    SUM(d.debt_value) AS total_debt
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
JOIN indicators i
    ON d.indicator_id = i.indicator_id
WHERE {where_clause}
GROUP BY d.year
ORDER BY d.year
"""


filtered_year_df = pd.read_sql(
    filtered_year_query,
    conn,
    params=filter_params
)


if not filtered_year_df.empty:

    fig_filtered = px.line(
        filtered_year_df,
        x="year",
        y="total_debt",
        markers=True,
        title="Filtered Debt Trend by Year",
        labels={
            "year": "Year",
            "total_debt": "Debt Value (USD)"
        }
    )

    st.plotly_chart(
        fig_filtered,
        use_container_width=True
    )

else:

    st.warning(
        "No data available for the selected filters."
    )


# ============================================================
# CLOSE MYSQL CONNECTION
# ============================================================

conn.close()