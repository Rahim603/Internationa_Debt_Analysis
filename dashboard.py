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
# SQL ANALYTICAL QUESTIONS
# ============================================================

st.sidebar.markdown("---")
st.sidebar.header("🧮 SQL Analytical Questions")

sql_questions = {
    "🔹 Basic Queries": [
        "Q1. Retrieve all distinct country names from the dataset.",
        "Q2. Count the total number of countries available.",
        "Q3. Find the total number of indicators present.",
        "Q4. Display the first 10 records of the dataset.",
        "Q5. Calculate the total global debt.",
        "Q6. List all unique indicator names.",
        "Q7. Find the number of records for each country.",
        "Q8. Display all records where debt is greater than 1 billion USD.",
        "Q9. Find the minimum, maximum, and average debt values.",
        "Q10. Count total number of records in the dataset."
    ],

    "🔹 Intermediate Level": [
        "Q11. Find the total debt for each country.",
        "Q12. Display the top 10 countries with the highest total debt.",
        "Q13. Find the average debt per country.",
        "Q14. Calculate total debt for each indicator.",
        "Q15. Identify the indicator contributing the highest total debt.",
        "Q16. Find the country with the lowest total debt.",
        "Q17. Calculate total debt for each country and indicator combination.",
        "Q18. Count how many indicators each country has.",
        "Q19. Display countries whose total debt is above the global average.",
        "Q20. Rank countries based on total debt (highest to lowest)."
    ],

    "🔹 Advanced Level": [
        "Q21. Find the top 5 indicators contributing most to global debt.",
        "Q22. Calculate percentage contribution of each country to total global debt.",
        "Q23. Identify the top 3 countries for each indicator based on debt.",
        "Q24. Find the difference between maximum and minimum debt for each country.",
        "Q25. Create a view for the top 10 countries with highest debt.",
        "Q26. Categorize countries into: High Debt, Medium Debt, Low Debt (based on thresholds).",
        "Q27. Use window functions to calculate cumulative debt per country.",
        "Q28. Find indicators where average debt is higher than overall average debt.",
        "Q29. Identify countries contributing more than 5% of global debt.",
        "Q30. Find the most dominant indicator (highest contribution) for each country."
    ]
}

selected_level = st.sidebar.selectbox(
    "Select Question Level",
    list(sql_questions.keys())
)

selected_sql_question = st.sidebar.selectbox(
    "Select SQL Question",
    sql_questions[selected_level]
)

st.header("🧮 SQL Analytical Questions")
st.write(f"**{selected_sql_question}**")


if selected_sql_question.startswith("Q1."):
    df = pd.read_sql("""
        SELECT DISTINCT c.country_name
        FROM countries c
        JOIN debt_data d ON c.country_id = d.country_id
        ORDER BY c.country_name
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q2."):
    df = pd.read_sql("""
        SELECT COUNT(*) AS total_countries
        FROM countries
    """, conn)
    st.metric("Total Countries", f"{df.iloc[0, 0]:,}")

elif selected_sql_question.startswith("Q3."):
    df = pd.read_sql(f"""
        SELECT COUNT(*) AS total_indicators
        FROM indicators i
        WHERE {debt_condition}
    """, conn)
    st.metric("Total Indicators", f"{df.iloc[0, 0]:,}")

elif selected_sql_question.startswith("Q4."):
    df = pd.read_sql("""
        SELECT *
        FROM debt_data
        LIMIT 10
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q5."):
    df = pd.read_sql(f"""
        SELECT COALESCE(SUM(d.debt_value), 0) AS total_global_debt
        FROM debt_data d
        JOIN indicators i ON d.indicator_id = i.indicator_id
        WHERE {debt_condition}
    """, conn)
    st.metric("Total Global Debt", f"${df.iloc[0, 0]:,.2f}")

elif selected_sql_question.startswith("Q6."):
    df = pd.read_sql(f"""
        SELECT DISTINCT i.indicator_name
        FROM indicators i
        WHERE {debt_condition}
        ORDER BY i.indicator_name
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q7."):
    df = pd.read_sql("""
        SELECT c.country_name, COUNT(*) AS record_count
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY record_count DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q8."):
    df = pd.read_sql(f"""
        SELECT d.*, c.country_name, i.indicator_name
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        JOIN indicators i ON d.indicator_id = i.indicator_id
        WHERE {debt_condition}
          AND d.debt_value > 1000000000
        ORDER BY d.debt_value DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q9."):
    df = pd.read_sql("""
        SELECT
            MIN(debt_value) AS minimum_debt,
            MAX(debt_value) AS maximum_debt,
            AVG(debt_value) AS average_debt
        FROM debt_data
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q10."):
    df = pd.read_sql("""
        SELECT COUNT(*) AS total_records
        FROM debt_data
    """, conn)
    st.metric("Total Records", f"{df.iloc[0, 0]:,}")

elif selected_sql_question.startswith("Q11."):
    df = pd.read_sql("""
        SELECT c.country_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY total_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q12."):
    df = pd.read_sql("""
        SELECT c.country_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY total_debt DESC
        LIMIT 10
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q13."):
    df = pd.read_sql("""
        SELECT c.country_name, AVG(d.debt_value) AS average_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY average_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q14."):
    df = pd.read_sql("""
        SELECT i.indicator_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN indicators i ON d.indicator_id = i.indicator_id
        GROUP BY i.indicator_name
        ORDER BY total_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q15."):
    df = pd.read_sql("""
        SELECT i.indicator_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN indicators i ON d.indicator_id = i.indicator_id
        GROUP BY i.indicator_name
        ORDER BY total_debt DESC
        LIMIT 1
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q16."):
    df = pd.read_sql("""
        SELECT c.country_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY total_debt ASC
        LIMIT 1
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q17."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            i.indicator_name,
            SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        JOIN indicators i ON d.indicator_id = i.indicator_id
        GROUP BY c.country_name, i.indicator_name
        ORDER BY total_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q18."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            COUNT(DISTINCT d.indicator_id) AS indicator_count
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY indicator_count DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q19."):
    df = pd.read_sql("""
        SELECT c.country_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        HAVING SUM(d.debt_value) > (
            SELECT AVG(country_total)
            FROM (
                SELECT SUM(debt_value) AS country_total
                FROM debt_data
                GROUP BY country_id
            ) AS country_totals
        )
        ORDER BY total_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q20."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            SUM(d.debt_value) AS total_debt,
            RANK() OVER (ORDER BY SUM(d.debt_value) DESC) AS debt_rank
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY debt_rank
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q21."):
    df = pd.read_sql("""
        SELECT i.indicator_name, SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN indicators i ON d.indicator_id = i.indicator_id
        GROUP BY i.indicator_name
        ORDER BY total_debt DESC
        LIMIT 5
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q22."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            SUM(d.debt_value) AS total_debt,
            ROUND(
                SUM(d.debt_value) * 100 /
                (SELECT SUM(debt_value) FROM debt_data), 2
            ) AS debt_share_percent
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY debt_share_percent DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q23."):
    df = pd.read_sql("""
        SELECT indicator_name, country_name, total_debt, country_rank
        FROM (
            SELECT
                i.indicator_name,
                c.country_name,
                SUM(d.debt_value) AS total_debt,
                ROW_NUMBER() OVER (
                    PARTITION BY d.indicator_id
                    ORDER BY SUM(d.debt_value) DESC
                ) AS country_rank
            FROM debt_data d
            JOIN countries c ON d.country_id = c.country_id
            JOIN indicators i ON d.indicator_id = i.indicator_id
            GROUP BY d.indicator_id, i.indicator_name, c.country_name
        ) ranked
        WHERE country_rank <= 3
        ORDER BY indicator_name, country_rank
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q24."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            MAX(d.debt_value) AS maximum_debt,
            MIN(d.debt_value) AS minimum_debt,
            MAX(d.debt_value) - MIN(d.debt_value) AS debt_difference
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY debt_difference DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q25."):
    cursor_q25 = conn.cursor()
    cursor_q25.execute("""
        CREATE OR REPLACE VIEW top_10_debt_countries AS
        SELECT
            c.country_name,
            SUM(d.debt_value) AS total_debt
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        ORDER BY total_debt DESC
        LIMIT 10
    """)
    cursor_q25.close()

    df = pd.read_sql("""
        SELECT *
        FROM top_10_debt_countries
        ORDER BY total_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q26."):
    st.info("Set the thresholds used to categorize countries.")

    col1, col2 = st.columns(2)

    medium_threshold = col1.number_input(
        "Medium Debt threshold (USD)",
        min_value=0.0,
        value=10000000000.0,
        step=1000000000.0
    )

    high_threshold = col2.number_input(
        "High Debt threshold (USD)",
        min_value=0.0,
        value=100000000000.0,
        step=1000000000.0
    )

    if high_threshold <= medium_threshold:
        st.warning("High Debt threshold must be greater than Medium Debt threshold.")
    else:
        df = pd.read_sql(f"""
            SELECT
                country_name,
                total_debt,
                CASE
                    WHEN total_debt >= {high_threshold} THEN 'High Debt'
                    WHEN total_debt >= {medium_threshold} THEN 'Medium Debt'
                    ELSE 'Low Debt'
                END AS debt_category
            FROM (
                SELECT
                    c.country_name,
                    SUM(d.debt_value) AS total_debt
                FROM debt_data d
                JOIN countries c ON d.country_id = c.country_id
                GROUP BY c.country_name
            ) AS country_totals
            ORDER BY total_debt DESC
        """, conn)
        st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q27."):
    df = pd.read_sql("""
        SELECT
            country_name,
            year,
            yearly_debt,
            SUM(yearly_debt) OVER (
                PARTITION BY country_name
                ORDER BY year
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_debt
        FROM (
            SELECT
                c.country_name,
                d.year,
                SUM(d.debt_value) AS yearly_debt
            FROM debt_data d
            JOIN countries c ON d.country_id = c.country_id
            GROUP BY c.country_name, d.year
        ) AS yearly_totals
        ORDER BY country_name, year
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q28."):
    df = pd.read_sql("""
        SELECT
            i.indicator_name,
            AVG(d.debt_value) AS average_debt
        FROM debt_data d
        JOIN indicators i ON d.indicator_id = i.indicator_id
        GROUP BY i.indicator_name
        HAVING AVG(d.debt_value) > (
            SELECT AVG(debt_value)
            FROM debt_data
        )
        ORDER BY average_debt DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q29."):
    df = pd.read_sql("""
        SELECT
            c.country_name,
            SUM(d.debt_value) AS total_debt,
            ROUND(
                SUM(d.debt_value) * 100 /
                (SELECT SUM(debt_value) FROM debt_data), 2
            ) AS debt_share_percent
        FROM debt_data d
        JOIN countries c ON d.country_id = c.country_id
        GROUP BY c.country_name
        HAVING SUM(d.debt_value) >
               (SELECT SUM(debt_value) * 0.05 FROM debt_data)
        ORDER BY debt_share_percent DESC
    """, conn)
    st.dataframe(df, use_container_width=True)

elif selected_sql_question.startswith("Q30."):
    df = pd.read_sql("""
        SELECT country_name, indicator_name, total_debt
        FROM (
            SELECT
                c.country_name,
                i.indicator_name,
                SUM(d.debt_value) AS total_debt,
                ROW_NUMBER() OVER (
                    PARTITION BY d.country_id
                    ORDER BY SUM(d.debt_value) DESC
                ) AS indicator_rank
            FROM debt_data d
            JOIN countries c ON d.country_id = c.country_id
            JOIN indicators i ON d.indicator_id = i.indicator_id
            GROUP BY
                d.country_id,
                c.country_name,
                d.indicator_id,
                i.indicator_name
        ) ranked
        WHERE indicator_rank = 1
        ORDER BY country_name
    """, conn)
    st.dataframe(df, use_container_width=True)


# ============================================================
# CLOSE MYSQL CONNECTION
# ============================================================

conn.close()