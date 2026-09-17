CREATE DATABASE IF NOT EXISTS international_debt;

USE international_debt;



#step 2 create table

USE international_debt;

CREATE TABLE IF NOT EXISTS countries (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(150) NOT NULL,
    country_code VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS indicators (
    indicator_id INT AUTO_INCREMENT PRIMARY KEY,
    series_code VARCHAR(100) NOT NULL UNIQUE,
    indicator_name VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS debt_data (
    debt_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    indicator_id INT NOT NULL,
    counterpart_area_name VARCHAR(150),
    counterpart_area_code VARCHAR(10),
    year INT NOT NULL,
    debt_value DECIMAL(30,2),

    CONSTRAINT fk_debt_country
        FOREIGN KEY (country_id)
        REFERENCES countries(country_id),

    CONSTRAINT fk_debt_indicator
        FOREIGN KEY (indicator_id)
        REFERENCES indicators(indicator_id)
);


#verify table

SHOW TABLES;


USE international_debt;

SELECT COUNT(*) AS total_countries
FROM countries;

SELECT COUNT(*) AS total_indicators
FROM indicators;



#SQL Analysis — Question 1

USE international_debt;

SELECT DISTINCT country_name
FROM countries
ORDER BY country_name;

#Q2 — Count total number of countries
SELECT COUNT(*) AS total_countries
FROM countries;

#Question2: Count the total number of countries.

USE international_debt;

#Question3: Find the total number of indicators

USE international_debt;

SELECT COUNT(*) AS total_indicators
FROM indicators;

#Question4: Display the first 10 records

USE international_debt;

SELECT *
FROM debt_data
LIMIT 10;

SELECT COUNT(*) AS total_countries
FROM countries;

#Question: Calculate total global debt.

SELECT SUM(dd.debt_value) AS total_global_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%';

#Question: List all unique indicator names.

SELECT DISTINCT indicator_name
FROM indicators
ORDER BY indicator_name;

#Question: Find the number of records for each country
SELECT 
    c.country_name,
    COUNT(dd.debt_id) AS record_count
FROM countries c
JOIN debt_data dd
    ON c.country_id = dd.country_id
GROUP BY c.country_id, c.country_name
ORDER BY record_count DESC;

#Question8: Display records where debt is greater than 1 billion USD

SELECT
    c.country_name,
    i.indicator_name,
    dd.year,
    dd.debt_value
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
  AND dd.debt_value > 1000000000
ORDER BY dd.debt_value DESC;

#Question9: Find the minimum, maximum, and average debt values.

SELECT
    MIN(dd.debt_value) AS minimum_debt,
    MAX(dd.debt_value) AS maximum_debt,
    AVG(dd.debt_value) AS average_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%';

#Question10: Count the total number of records

SELECT COUNT(*) AS total_records
FROM debt_data;

#Question: Find the total debt for each country.

SELECT
    c.country_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC;

# Question 12-Top 10 countries with the highest total debt.
SELECT
    c.country_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

#Question 13-Find the average debt per country

SELECT
    c.country_name,
    AVG(dd.debt_value) AS average_debt
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY c.country_id, c.country_name
ORDER BY average_debt DESC;

#Question 14-Find the total debt for each indicator.

SELECT
    i.indicator_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY i.indicator_id, i.indicator_name
ORDER BY total_debt DESC;

#Question 15-Find the indicator contributing the highest total debt
SELECT
    i.indicator_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY i.indicator_id, i.indicator_name
ORDER BY total_debt DESC
LIMIT 1;

#Q16 — Country with the lowest total debt

SELECT
    c.country_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY c.country_id, c.country_name
ORDER BY total_debt ASC
LIMIT 1;

#Q17 — Total debt for each country + indicator combination

SELECT
    c.country_name,
    i.indicator_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY
    c.country_id,
    c.country_name,
    i.indicator_id,
    i.indicator_name
LIMIT 100;

#Q18 — Number of indicators each country has

SELECT
    c.country_name,
    COUNT(DISTINCT i.indicator_id) AS indicator_count
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY c.country_id, c.country_name
ORDER BY indicator_count DESC;

#Q19 — Countries whose total debt is above the global average

       #Step 1 — Find the average country debt
SELECT AVG(total_debt) AS average_country_debt
FROM country_debt_totals;
        #Step 2
SELECT
    c.country_name,
    t.total_debt
FROM country_debt_totals t
JOIN countries c
    ON t.country_id = c.country_id
WHERE t.total_debt > 598907282714.804403
ORDER BY t.total_debt DESC;	

#Q20 — Rank countries based on total debt
SELECT
    c.country_name,
    t.total_debt,
    RANK() OVER (ORDER BY t.total_debt DESC) AS debt_rank
FROM country_debt_totals t
JOIN countries c
    ON t.country_id = c.country_id
ORDER BY debt_rank;
        
#Q21 — Top 5 indicators contributing most to global debt     
SELECT
    i.indicator_name,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY i.indicator_id, i.indicator_name
ORDER BY total_debt DESC
LIMIT 5;

#Q22 — Percentage contribution of each country to total global debt

SELECT SUM(total_debt) AS global_total_debt
FROM country_debt_totals;

#Q22 — Step 2: Percentage contribution of each country

SELECT
    c.country_name,
    t.total_debt,
    (t.total_debt / 8025357588378386.25) * 100 AS percentage_contribution
FROM country_debt_totals t
JOIN countries c
    ON t.country_id = c.country_id
ORDER BY percentage_contribution DESC;

#Q23 — Top 3 countries for each indicator
#step 1

USE international_debt;

SHOW INDEX FROM debt_data;

SHOW INDEX FROM indicators;

SELECT COUNT(*) AS debt_rows
FROM debt_data;

SELECT COUNT(*) AS dt_indicators
FROM indicators
WHERE series_code LIKE 'DT.%';

SELECT
    dd.country_id,
    dd.indicator_id,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY
    dd.country_id,
    dd.indicator_id;
    
CREATE TEMPORARY TABLE debt_summary AS
SELECT
    dd.country_id,
    dd.indicator_id,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY
    dd.country_id,
    dd.indicator_id;    

CREATE TEMPORARY TABLE debt_summary AS
SELECT
    dd.country_id,
    dd.indicator_id,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
JOIN indicators i
    ON dd.indicator_id = i.indicator_id
WHERE i.series_code LIKE 'DT.%'
GROUP BY
    dd.country_id,
    dd.indicator_id;
    
CREATE INDEX idx_summary_indicator_debt
ON debt_summary (indicator_id, total_debt);    

SELECT
    c.country_name,
    i.indicator_name,
    ds.total_debt,
    RANK() OVER (
        PARTITION BY ds.indicator_id
        ORDER BY ds.total_debt DESC
    ) AS indicator_rank
FROM debt_summary ds
JOIN countries c
    ON ds.country_id = c.country_id
JOIN indicators i
    ON ds.indicator_id = i.indicator_id;
    
 
SELECT
    indicator_name,
    country_name,
    total_debt,
    indicator_rank
FROM (
    SELECT
        c.country_name,
        i.indicator_name,
        ds.total_debt,
        RANK() OVER (
            PARTITION BY ds.indicator_id
            ORDER BY ds.total_debt DESC
        ) AS indicator_rank
    FROM debt_summary ds
    JOIN countries c
        ON ds.country_id = c.country_id
    JOIN indicators i
        ON ds.indicator_id = i.indicator_id
) ranked
WHERE indicator_rank <= 5
ORDER BY indicator_name, indicator_rank; 

SELECT *
FROM countries
LIMIT 10;

SELECT
    country_id,
    country_name,
    country_code
FROM countries
WHERE country_name LIKE '%income%'
   OR country_name LIKE '%IDA%'
   OR country_name LIKE '%region%'
   OR country_name LIKE '%world%'
ORDER BY country_name;

SELECT
    indicator_name,
    country_name,
    total_debt,
    indicator_rank
FROM (
    SELECT
        c.country_name,
        c.country_code,
        i.indicator_name,
        ds.total_debt,
        RANK() OVER (
            PARTITION BY ds.indicator_id
            ORDER BY ds.total_debt DESC
        ) AS indicator_rank
    FROM debt_summary ds
    JOIN countries c
        ON ds.country_id = c.country_id
    JOIN indicators i
        ON ds.indicator_id = i.indicator_id
    WHERE c.country_code NOT IN (
        'EAP','ECA','IDX','IDA','LAC','LMY',
        'LIC','LMC','MNA','MIC','SSA','UMC'
    )
) ranked
WHERE indicator_rank <= 5
ORDER BY indicator_name, indicator_rank;

SELECT
    c.country_name,
    SUM(ds.total_debt) AS overall_debt
FROM debt_summary ds
JOIN countries c
    ON ds.country_id = c.country_id
WHERE c.country_code NOT IN (
    'EAP','ECA','IDX','IDA','LAC','LMY',
    'LIC','LMC','MNA','MIC','SSA','UMC'
)
GROUP BY
    c.country_id,
    c.country_name
ORDER BY overall_debt DESC
LIMIT 10;

SELECT
    c.country_name,
    SUM(ds.total_debt) AS overall_debt
FROM debt_summary ds
JOIN countries c
    ON ds.country_id = c.country_id
WHERE TRIM(c.country_code) NOT IN (
    'EAP','ECA','IDX','IDA','LAC','LMY',
    'LIC','LMC','MNA','MIC','SSA','UMC'
)
GROUP BY
    c.country_id,
    c.country_name
ORDER BY overall_debt DESC
LIMIT 10;

SELECT
    dd.debt_year,
    SUM(dd.debt_value) AS total_debt
FROM debt_data dd
GROUP BY dd.debt_year
ORDER BY dd.debt_year;

DESCRIBE debt_data;

SELECT
    year,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY year;

SELECT
    i.indicator_name,
    SUM(ds.total_debt) AS indicator_total_debt
FROM debt_summary ds
JOIN indicators i
    ON ds.indicator_id = i.indicator_id
GROUP BY
    i.indicator_id,
    i.indicator_name
ORDER BY indicator_total_debt DESC
LIMIT 10;


#Q23 — Identify the top 3 countries for each indicator based on debt

SELECT
    indicator_name,
    country_name,
    total_debt,
    indicator_rank
FROM (
    SELECT
        c.country_name,
        i.indicator_name,
        ds.total_debt,
        RANK() OVER (
            PARTITION BY ds.indicator_id
            ORDER BY ds.total_debt DESC
        ) AS indicator_rank
    FROM debt_summary ds
    JOIN countries c
        ON ds.country_id = c.country_id
    JOIN indicators i
        ON ds.indicator_id = i.indicator_id
    WHERE TRIM(c.country_code) NOT IN (
        'EAP','ECA','IDX','IDA','LAC','LMY',
        'LIC','LMC','MNA','MIC','SSA','UMC'
    )
) ranked
WHERE indicator_rank <= 3
ORDER BY indicator_name, indicator_rank;

#Q24 — Difference between maximum and minimum debt for each country

SELECT
    c.country_name,
    MAX(dd.debt_value) AS max_debt,
    MIN(dd.debt_value) AS min_debt,
    MAX(dd.debt_value) - MIN(dd.debt_value) AS debt_difference
FROM debt_data dd
JOIN countries c
    ON dd.country_id = c.country_id
GROUP BY
    c.country_id,
    c.country_name
ORDER BY debt_difference DESC;

#Q25 — Create a View for Top 10 Countries by Total Debt
USE international_debt;

CREATE VIEW top_10_debt_countries AS
SELECT
    country_name,
    SUM(debt) AS total_debt
FROM international_debt
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;

SHOW TABLES;

DESCRIBE debt_data;

CREATE VIEW top_10_debt_countries AS
SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT *
FROM top_10_debt_countries;

SELECT
    country_id,
    country_name,
    country_code
FROM countries
WHERE country_name IN (
    'Low & middle income',
    'Middle income',
    'Upper middle income',
    'China',
    'IDA total'
);

SELECT
    country_id,
    country_name,
    country_code
FROM countries
WHERE country_name LIKE '%income%'
   OR country_name LIKE '%total%'
   OR country_name LIKE '%excluding%'
   OR country_name LIKE '%World%'
   OR country_name LIKE '%region%'
   OR country_name LIKE '%IBRD%'
   OR country_name LIKE '%IDA%';
   
   
DROP VIEW IF EXISTS top_10_debt_countries;

CREATE VIEW top_10_debt_countries AS
SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
WHERE c.country_code NOT IN
('EAP','ECA','IDX','IDA','LAC','LMY','LIC','LMC','MNA','MIC','SSA','UMC')
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT * FROM top_10_debt_countries;

SHOW CREATE VIEW top_10_debt_countries;


SELECT VIEW_DEFINITION
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'international_debt'
  AND TABLE_NAME = 'top_10_debt_countries';
  
  SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
WHERE c.country_code NOT IN
('EAP','ECA','IDX','IDA','LAC','LMY','LIC','LMC','MNA','MIC','SSA','UMC')
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries AS c
JOIN debt_data AS d
    ON c.country_id = d.country_id
WHERE c.country_code NOT IN
('EAP','ECA','IDX','IDA','LAC','LMY','LIC','LMC','MNA','MIC','SSA','UMC')
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

DROP VIEW IF EXISTS top_10_debt_countries;

CREATE VIEW top_10_debt_countries AS
SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
WHERE c.country_code NOT IN
('EAP','ECA','IDX','IDA','LAC','LMY','LIC','LMC','MNA','MIC','SSA','UMC')
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

CREATE OR REPLACE VIEW top_10_debt_countries AS
SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt
FROM countries c
JOIN debt_data d
    ON c.country_id = d.country_id
WHERE c.country_code NOT IN
('EAP','ECA','IDX','IDA','LAC','LMY','LIC','LMC','MNA','MIC','SSA','UMC')
GROUP BY c.country_id, c.country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT * FROM top_10_debt_countries;


#Q26 Categorize countries into High Debt, Medium Debt, Low Debt based on thresholds.

WITH country_debt AS (
    SELECT
        c.country_id,
        c.country_name,
        SUM(d.debt_value) AS total_debt
    FROM countries c
    JOIN debt_data d
        ON c.country_id = d.country_id
    WHERE c.country_code NOT IN
        ('EAP','ECA','IDX','IDA','LAC','LMY',
         'LIC','LMC','MNA','MIC','SSA','UMC')
    GROUP BY c.country_id, c.country_name
),
avg_debt AS (
    SELECT AVG(total_debt) AS average_debt
    FROM country_debt
)
SELECT
    cd.country_name,
    cd.total_debt,
    CASE
        WHEN cd.total_debt > 2 * ad.average_debt
            THEN 'High Debt'
        WHEN cd.total_debt >= ad.average_debt
            THEN 'Medium Debt'
        ELSE 'Low Debt'
    END AS debt_category
FROM country_debt cd
CROSS JOIN avg_debt ad
ORDER BY cd.total_debt DESC;

#Q27  Use window functions to calculate cumulative debt per country

SELECT
    country_name,
    year,
    debt_amount,
    SUM(debt_amount) OVER (
        PARTITION BY country_name
        ORDER BY year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_debt
FROM international_debt
ORDER BY country_name, year;

SHOW TABLES;
DESCRIBE debt_data;
DESCRIBE countries;

#Q27 — Cumulative Debt per Country using Window Function

SELECT
    c.country_name,
    d.year,
    SUM(d.debt_value) AS yearly_debt,
    SUM(SUM(d.debt_value)) OVER (
        PARTITION BY d.country_id
        ORDER BY d.year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_debt
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
GROUP BY
    d.country_id,
    c.country_name,
    d.year
ORDER BY
    c.country_name,
    d.year;
    
#Q28 — Find indicators where average debt is higher than overall average debt 

DESCRIBE indicators; 

SELECT
    i.indicator_name,
    AVG(d.debt_value) AS average_indicator_debt
FROM debt_data d
JOIN indicators i
    ON d.indicator_id = i.indicator_id
GROUP BY
    d.indicator_id,
    i.indicator_name
HAVING
    AVG(d.debt_value) > (
        SELECT AVG(debt_value)
        FROM debt_data
    )
ORDER BY
    average_indicator_debt DESC;  
    
WITH indicator_stats AS (
    SELECT
        indicator_id,
        AVG(debt_value) AS average_indicator_debt,
        SUM(SUM(debt_value)) OVER () /
        SUM(COUNT(debt_value)) OVER () AS overall_average_debt
    FROM debt_data
    GROUP BY indicator_id
)
SELECT
    i.indicator_name,
    s.average_indicator_debt,
    s.overall_average_debt
FROM indicator_stats s
JOIN indicators i
    ON s.indicator_id = i.indicator_id
WHERE s.average_indicator_debt > s.overall_average_debt
ORDER BY s.average_indicator_debt DESC;    

#Q29 — Identify countries contributing more than 5% of global debt

SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt,
    ROUND(
        SUM(d.debt_value) * 100.0 /
        (SELECT SUM(debt_value) FROM debt_data),
        2
    ) AS debt_percentage
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
GROUP BY
    d.country_id,
    c.country_name
HAVING
    SUM(d.debt_value) * 100.0 /
    (SELECT SUM(debt_value) FROM debt_data) > 5
ORDER BY
    debt_percentage DESC;
    
WITH country_totals AS (
    SELECT
        country_id,
        SUM(debt_value) AS total_debt
    FROM debt_data
    GROUP BY country_id
),
country_with_percentage AS (
    SELECT
        country_id,
        total_debt,
        SUM(total_debt) OVER () AS global_debt
    FROM country_totals
)
SELECT
    c.country_name,
    cp.total_debt,
    ROUND(
        cp.total_debt * 100.0 / cp.global_debt,
        2
    ) AS debt_percentage
FROM country_with_percentage cp
JOIN countries c
    ON cp.country_id = c.country_id
WHERE cp.total_debt * 100.0 / cp.global_debt > 5
ORDER BY debt_percentage DESC;  

CREATE TEMPORARY TABLE country_totals_q29 AS
SELECT
    country_id,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_id;  

SELECT COUNT(*) AS total_records

SELECT
    country_id,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_id
LIMIT 10;
FROM debt_data;

SHOW INDEX FROM debt_data;

SELECT
    country_id,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_id
LIMIT 10;

SELECT
    indicator_id,
    series_code,
    indicator_name
FROM indicators
WHERE series_code LIKE 'DT.%'
ORDER BY indicator_id;

WITH country_totals AS (
    SELECT
        country_id,
        SUM(debt_value) AS total_debt
    FROM debt_data
    WHERE indicator_id BETWEEN 10 AND 576
    GROUP BY country_id
),
global_total AS (
    SELECT SUM(total_debt) AS global_debt
    FROM country_totals
)
SELECT
    c.country_name,
    ct.total_debt,
    ROUND(
        ct.total_debt * 100.0 / gt.global_debt,
        2
    ) AS debt_percentage
FROM country_totals ct
JOIN countries c
    ON ct.country_id = c.country_id
CROSS JOIN global_total gt
WHERE ct.total_debt > gt.global_debt * 0.05
ORDER BY ct.total_debt DESC;

SELECT
    country_id,
    country_name,
    country_code
FROM countries
WHERE country_name IN (
    'Low & middle income',
    'Middle income',
    'Upper middle income',
    'East Asia & Pacific (excluding high income)',
    'Lower middle income'
);

WITH country_totals AS (
    SELECT
        country_id,
        SUM(debt_value) AS total_debt
    FROM debt_data
    WHERE indicator_id BETWEEN 10 AND 576
      AND country_id NOT IN (33, 72, 74, 83, 128)
    GROUP BY country_id
),
global_total AS (
    SELECT SUM(total_debt) AS global_debt
    FROM country_totals
)
SELECT
    c.country_name,
    ct.total_debt,
    ROUND(
        ct.total_debt * 100.0 / gt.global_debt,
        2
    ) AS debt_percentage
FROM country_totals ct
JOIN countries c
    ON ct.country_id = c.country_id
CROSS JOIN global_total gt
WHERE ct.total_debt > gt.global_debt * 0.05
ORDER BY ct.total_debt DESC;

SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt,
    ROUND(
        SUM(d.debt_value) * 100.0 /
        (
            SELECT SUM(d2.debt_value)
            FROM debt_data d2
            WHERE d2.country_id IN (
                SELECT country_id
                FROM countries
                WHERE country_code REGEXP '^[A-Z]{3}$'
            )
        ),
        2
    ) AS debt_percentage
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
WHERE d.indicator_id BETWEEN 10 AND 576
  AND c.country_code REGEXP '^[A-Z]{3}$'
GROUP BY c.country_id, c.country_name
HAVING debt_percentage > 5
ORDER BY debt_percentage DESC;


SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt,
    ROUND(
        SUM(d.debt_value) * 100.0 /
        (
            SELECT SUM(d2.debt_value)
            FROM debt_data d2
            WHERE d2.indicator_id BETWEEN 10 AND 576
        ),
        2
    ) AS debt_percentage
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
WHERE d.indicator_id BETWEEN 10 AND 576
  AND c.country_name NOT IN (
      'East Asia & Pacific (excluding high income)',
      'Low & middle income',
      'Lower middle income',
      'Middle income',
      'Upper middle income',
      'Latin America & Caribbean (excluding high income)',
      'IDA total',
      'Europe & Central Asia (excluding high income)',
      'Sub-Saharan Africa (excluding high income)',
      'South Asia'
  )
GROUP BY
    c.country_id,
    c.country_name
HAVING
    SUM(d.debt_value) * 100.0 /
    (
        SELECT SUM(d2.debt_value)
        FROM debt_data d2
        WHERE d2.indicator_id BETWEEN 10 AND 576
    ) > 5
ORDER BY
    debt_percentage DESC;
    
SET @global_debt = (
    SELECT SUM(debt_value)
    FROM debt_data
    WHERE indicator_id BETWEEN 10 AND 576
      AND country_id NOT IN (33, 72, 74, 83, 128)
);    

SELECT
    c.country_name,
    SUM(d.debt_value) AS total_debt,
    ROUND(
        SUM(d.debt_value) * 100.0 / @global_debt,
        2
    ) AS debt_percentage
FROM debt_data d
JOIN countries c
    ON d.country_id = c.country_id
WHERE d.indicator_id BETWEEN 10 AND 576
  AND d.country_id NOT IN (33, 72, 74, 83, 128)
GROUP BY d.country_id, c.country_name
HAVING SUM(d.debt_value) > @global_debt * 0.05
ORDER BY debt_percentage DESC;

WITH country_totals AS (
    SELECT
        d.country_id,
        SUM(d.debt_value) AS total_debt
    FROM debt_data d
    JOIN countries c
        ON d.country_id = c.country_id
    WHERE d.indicator_id BETWEEN 10 AND 576
      AND c.country_name NOT LIKE '%income%'
      AND c.country_name NOT LIKE '%excluding%'
      AND c.country_name NOT LIKE '%IDA%'
      AND c.country_name NOT LIKE '%South Asia%'
      AND c.country_name NOT LIKE '%World%'
      AND c.country_name NOT LIKE '%Total%'
    GROUP BY d.country_id
),
country_percentages AS (
    SELECT
        country_id,
        total_debt,
        total_debt * 100.0 / SUM(total_debt) OVER () AS debt_percentage
    FROM country_totals
)
SELECT
    c.country_name,
    cp.total_debt,
    ROUND(cp.debt_percentage, 2) AS debt_percentage
FROM country_percentages cp
JOIN countries c
    ON cp.country_id = c.country_id
WHERE cp.debt_percentage > 5
ORDER BY cp.debt_percentage DESC;


#Q30 — Find the most dominant indicator (highest contribution) for each country

WITH indicator_totals AS (
    SELECT
        country_id,
        indicator_id,
        SUM(debt_value) AS total_debt
    FROM debt_data
    GROUP BY
        country_id,
        indicator_id
),
ranked_indicators AS (
    SELECT
        country_id,
        indicator_id,
        total_debt,
        ROW_NUMBER() OVER (
            PARTITION BY country_id
            ORDER BY total_debt DESC
        ) AS rank_no
    FROM indicator_totals
)
SELECT
    c.country_name,
    i.indicator_name,
    r.total_debt
FROM ranked_indicators r
JOIN countries c
    ON r.country_id = c.country_id
JOIN indicators i
    ON r.indicator_id = i.indicator_id
WHERE r.rank_no = 1
ORDER BY r.total_debt DESC;