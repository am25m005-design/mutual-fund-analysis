-- 1. Top 5 funds by AUM

SELECT
    scheme_name,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. Average NAV by Month

SELECT
    strftime('%Y-%m', nav_date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;


-- 3. Transactions by State

SELECT
    state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- 4. Transaction Type Distribution

SELECT
    transaction_type,
    COUNT(*) AS total
FROM fact_transactions
GROUP BY transaction_type;


-- 5. Funds with Expense Ratio < 1%

SELECT
    scheme_name,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


-- 6. Average 3-Year Return

SELECT
    ROUND(AVG(return_3yr_pct),2) AS average_return
FROM fact_performance;


-- 7. Highest Sharpe Ratio Funds

SELECT
    scheme_name,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;


-- 8. Risk Grade Distribution

SELECT
    risk_grade,
    COUNT(*) AS total_funds
FROM fact_performance
GROUP BY risk_grade;


-- 9. Total Transaction Amount by State

SELECT
    state,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;


-- 10. Top Fund Houses by Number of Schemes

SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;