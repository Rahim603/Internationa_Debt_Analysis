International Debt Analysis System Using Python, SQL, and Visualization Tools
📌 Project Overview

The **International Debt Analysis System** is an end-to-end data analytics project focused on analyzing international debt data using **Python, MySQL, SQL, and interactive visualization tools**.

Global financial institutions such as the World Bank generate large volumes of international debt data containing country-wise borrowings, repayments, interest payments, and other financial indicators. These datasets are often available in raw and complex formats, making it difficult to directly analyze and interpret them.

This project transforms the raw international debt data into a structured and usable format through data cleaning, preprocessing, exploratory data analysis, SQL-based analysis, and interactive dashboard development.

The project follows a complete data analytics lifecycle:

**Data Collection → Data Cleaning → EDA → SQL Database → SQL Analysis → Visualization → Dashboard → Insights**

---

🎯 Project Objectives

The main objective is to design and implement an **International Debt Analytics System** that enables:

- Cleaning and preprocessing international debt data using Python
- Handling missing values and duplicate records
- Performing Exploratory Data Analysis (EDA)
- Understanding country-wise and indicator-wise debt
- Storing processed data in a structured MySQL database
- Performing analytical queries using SQL
- Creating visualizations to identify trends and patterns
- Developing an interactive dashboard using Streamlit
- Generating meaningful insights from international debt data

---

🏦 Domain

**Finance Analytics & Global Economic Data Analysis**

---

🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| MySQL | Relational database storage |
| SQL | Analytical queries |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive visualization |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Data analysis and EDA |
| VS Code | Development environment |

---

📂 Project Workflow

1. Data Collection

- Import international debt datasets in CSV format
- Load datasets into Python using Pandas
- Understand the structure, columns, and data types
- Review country, indicator, and debt-related information

2. Data Preprocessing

The raw data is prepared for analysis through:

- Missing-value handling
- Duplicate-record removal
- Data type conversion
- Relevant-column selection
- Data standardization
- Data transformation and preparation for SQL storage

3. Exploratory Data Analysis (EDA)

EDA is performed to understand the structure and characteristics of international debt data.

Key analysis areas include:

- Country-wise debt distribution
- Countries with the highest and lowest debt
- Debt indicator analysis
- Trends and patterns
- Statistical summaries
- Comparisons between countries and indicators

4. Database Design & SQL Integration

A relational MySQL database is designed to store the processed data.

Main entities include:

- **Countries**
- **Indicators**
- **Debt Data**

The database uses:

- Primary Keys
- Foreign Keys
- Relational table design
- Joins
- Aggregations
- SQL analytical queries

Processed data is integrated from Python into MySQL.

5. SQL Analysis

The project includes **30 SQL analytical questions** divided into three levels:

Basic Queries

1. Retrieve all distinct country names
2. Count the total number of countries
3. Find the total number of indicators
4. Display the first 10 records
5. Calculate total global debt
6. List unique indicator names
7. Find the number of records for each country
8. Display records where debt is greater than 1 billion USD
9. Find minimum, maximum, and average debt values
10. Count total records

Intermediate Queries

1. Find total debt for each country
2. Display the top 10 countries with the highest total debt
3. Find average debt per country
4. Calculate total debt for each indicator
5. Identify the indicator contributing the highest total debt
6. Find the country with the lowest total debt
7. Calculate debt for each country and indicator combination
8. Count the number of indicators for each country
9. Display countries above the global average
10. Rank countries based on total debt

Advanced Queries

1. Find the top 5 indicators contributing most to global debt
2. Calculate each country's percentage contribution to global debt
3. Identify the top 3 countries for each indicator
4. Find the difference between maximum and minimum debt for each country
5. Create a view for the top 10 countries with highest debt
6. Categorize countries into High, Medium, and Low Debt based on thresholds
7. Use window functions to calculate cumulative debt per country
8. Find indicators whose average debt is higher than the overall average
9. Identify countries contributing more than 5% of global debt
10. Find the most dominant indicator for each country

---

📊 Dashboard

An interactive dashboard is developed using **Streamlit** with visualization libraries such as Plotly, Matplotlib, and Seaborn.

The dashboard is designed to provide visual insights into:

- Country-wise debt
- Indicator-wise debt
- Top countries by debt
- Debt trends
- Comparative analysis
- Key analytical findings

Users can interact with the dashboard to explore the international debt data more easily.

---

🔍 Key Analysis Areas

The project focuses on identifying:

- Countries with high and low debt levels
- Major debt indicators
- Country-wise debt distribution
- Indicator-wise debt contribution
- International debt trends
- Countries contributing significantly to global debt
- Relationships between countries and debt indicators

---

📈 Expected Project Outcomes

The project produces:

- A clean and structured international debt dataset
- A relational MySQL database
- SQL analytical queries and insights
- Python-based data processing
- Exploratory data analysis
- Interactive visualizations
- A Streamlit dashboard
- Country-wise and indicator-wise debt insights
- An end-to-end data analytics pipeline

---
📁 Suggested GitHub Repository Structure

```text
International-Debt-Analysis/
│
├── README.md
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   └── international_debt_analysis.ipynb
│
├── python/
│   └── data_processing.py
│
├── sql/
│   ├── database_schema.sql
│   └── analytical_queries.sql
│
├── dashboard/
│   └── dashboard.py
│
├── visualizations/
│
├── reports/
│   └── EDA_Report.pdf
│
└── requirements.txt
```

> Update the filenames above according to the actual files included in the repository.

---

⚙️ Installation & Setup

1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd International-Debt-Analysis
```

2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

3. Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit mysql-connector-python jupyter
```

Or, if a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

---
🗄️ MySQL Database Setup

1. Install and start MySQL.
2. Create the project database.
3. Execute the database schema SQL file.
4. Create the required relational tables.
5. Insert the cleaned data into the database.
6. Execute the analytical SQL queries.

Example:

```sql
CREATE DATABASE international_debt;
USE international_debt;
```

> Update the database connection settings in the Python/dashboard files according to your local MySQL configuration.

---

▶️ Running the Dashboard

After completing the database setup:

```bash
streamlit run dashboard/dashboard.py
```

The dashboard will open in the browser.

---

🧹 Data Quality & Preprocessing

Data quality is an important part of this project.

The preprocessing stage addresses:

- Missing values
- Duplicate records
- Incorrect data types
- Irrelevant fields
- Data standardization
- Structured transformation for analysis

The cleaned dataset is then used for EDA, SQL integration, and visualization.

---

📊 Visualizations

The project uses visualizations to communicate analytical findings clearly.

Examples include:

- Country-wise debt comparison
- Indicator-wise debt distribution
- Top countries by total debt
- Debt trends over time
- Statistical comparisons
- Interactive Plotly charts

---

💡 Insights

The analysis is designed to generate insights related to:

- Country-wise international debt distribution
- Countries with relatively high or low debt
- Major debt indicators
- Global debt contribution
- Debt trends and patterns
- Indicator-level differences
- Country and indicator relationships

---

📦 Project Deliverables

The project deliverables include:

- Raw CSV dataset
- Cleaned and preprocessed dataset
- MySQL database schema
- Data insertion into SQL tables
- 30 SQL analytical queries
- Python data-processing and integration scripts
- Data visualizations
- Interactive Streamlit dashboard
- EDA report with insights
- Final project documentation

---

🎓 Skills Demonstrated

This project demonstrates practical skills in:

- Python programming
- Pandas data processing
- CSV-to-DataFrame conversion
- Data cleaning
- Data preprocessing
- Exploratory Data Analysis
- Financial data analysis
- MySQL
- SQL
- Relational database design
- Primary and foreign key relationships
- SQL joins and aggregations
- Window functions
- Data integration from Python to MySQL
- Plotly / Seaborn / Matplotlib
- Streamlit dashboard development
- Insight generation
- End-to-end data analytics

---

📌 Project Evaluation Areas

The project covers the following evaluation areas:

- Data preprocessing and quality
- CSV-to-DataFrame conversion
- Exploratory Data Analysis
- Database design and normalization
- Primary and foreign key relationships
- SQL query optimization
- Joins and aggregations
- Python-to-MySQL integration
- Visualization quality
- Dashboard functionality
- Clean and structured Python code
- Insight generation and interpretation
- Project documentation

---

🔗 Dataset

**International Debt Statistics Dataset**

The project problem statement references the International Debt Statistics dataset. The original dataset/source link should be added here when publishing the repository.

---

👨‍💻 Author

**[ABDUL RAHIM s]**

Data Analytics / Data Science Project

---
📜 Project Context

This project was completed as part of a guided data analytics project focused on applying Python, SQL, database concepts, visualization, and dashboard development to an international finance dataset.

---

⭐ Conclusion

The **International Debt Analysis System** demonstrates a complete data analytics workflow, starting from raw CSV data and progressing through data cleaning, EDA, MySQL database integration, SQL analysis, visualization, and interactive dashboard development.

The project provides a structured approach to understanding international debt data and extracting meaningful country-wise and indicator-wise insights.
