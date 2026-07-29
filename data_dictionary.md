# Mutual Fund Analytics - Data Dictionary

## 1. dim_fund

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | TEXT | Unique AMFI scheme code |
| scheme_name | TEXT | Mutual fund scheme name |
| fund_house | TEXT | Asset Management Company |
| category | TEXT | Scheme category |
| plan | TEXT | Direct or Regular plan |

---

## 2. fact_nav

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | TEXT | AMFI scheme code |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value |
| daily_return | REAL | Daily percentage return |

---

## 3. fact_transactions

| Column | Data Type | Description |
|---------|-----------|-------------|
| investor_id | TEXT | Investor identifier |
| transaction_date | DATE | Transaction date |
| amfi_code | TEXT | AMFI scheme code |
| transaction_type | TEXT | SIP, Lumpsum or Redemption |
| amount_inr | REAL | Transaction amount |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| city_tier | TEXT | City classification |
| age_group | TEXT | Investor age group |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income (₹ lakh) |
| payment_mode | TEXT | Mode of payment |
| kyc_status | TEXT | KYC verification status |

---

## 4. fact_performance

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | TEXT | AMFI scheme code |
| return_1yr_pct | REAL | 1-Year return (%) |
| return_3yr_pct | REAL | 3-Year return (%) |
| return_5yr_pct | REAL | 5-Year return (%) |
| benchmark_3yr_pct | REAL | Benchmark 3-Year return (%) |
| alpha | REAL | Alpha value |
| beta | REAL | Beta value |
| sharpe_ratio | REAL | Sharpe ratio |
| sortino_ratio | REAL | Sortino ratio |
| std_dev_ann_pct | REAL | Annualized standard deviation (%) |
| max_drawdown_pct | REAL | Maximum drawdown (%) |
| aum_crore | REAL | Assets Under Management (₹ crore) |
| expense_ratio_pct | REAL | Expense ratio (%) |
| morningstar_rating | INTEGER | Morningstar rating (1–5) |
| risk_grade | TEXT | Risk category |
| negative_sharpe | BOOLEAN | Indicates negative Sharpe ratio |
| invalid_expense_ratio | BOOLEAN | Indicates expense ratio outside expected range |

---

## Data Sources

- AMFI (Association of Mutual Funds in India)
- MFAPI
- Internship datasets provided by Bluestock Fintech

---

## Database

**Database Name**

```
bluestock_mf.db
```

**Tables**

- dim_fund
- fact_nav
- fact_transactions
- fact_performance