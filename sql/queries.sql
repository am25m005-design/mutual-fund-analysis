SELECT
    scheme_name,
    fund_house,
    aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav),2) AS average_nav
FROM nav_history
GROUP BY month
ORDER BY month;

SELECT
    strftime('%Y', transaction_date) AS year,
    COUNT(*) AS sip_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM investor_transactions
WHERE transaction_type='SIP'
GROUP BY year;

SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS investment
FROM investor_transactions
GROUP BY state
ORDER BY investment DESC;

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

SELECT
    scheme_name,
    return_5yr_pct
FROM scheme_performance
ORDER BY return_5yr_pct DESC
LIMIT 5;

SELECT
    transaction_type,
    ROUND(AVG(amount_inr),2) AS average_amount
FROM investor_transactions
GROUP BY transaction_type;

SELECT
    category,
    COUNT(*) AS total_funds
FROM fund_master
GROUP BY category
ORDER BY total_funds DESC;

SELECT
    category,
    ROUND(AVG(expense_ratio_pct),2) AS avg_expense_ratio
FROM scheme_performance
GROUP BY category
ORDER BY avg_expense_ratio;

SELECT
    amfi_code,
    MAX(nav) AS highest_nav
FROM nav_history
GROUP BY amfi_code
ORDER BY highest_nav DESC
LIMIT 10;