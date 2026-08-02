DROP TABLE IF EXISTS fund_master;
DROP TABLE IF EXISTS nav_history;
DROP TABLE IF EXISTS investor_transactions;
DROP TABLE IF EXISTS scheme_performance;
DROP TABLE IF EXISTS aum_history;

CREATE TABLE fund_master(

    amfi_code INTEGER PRIMARY KEY,

    fund_house TEXT,

    scheme_name TEXT,

    category TEXT,

    sub_category TEXT,

    plan TEXT,

    launch_date TEXT,

    benchmark TEXT,

    expense_ratio_pct REAL,

    exit_load_pct REAL,

    min_sip_amount REAL,

    min_lumpsum_amount REAL,

    fund_manager TEXT,

    risk_category TEXT,

    sebi_category_code TEXT
);

CREATE TABLE nav_history(

    amfi_code INTEGER,

    date TEXT,

    nav REAL
);

CREATE TABLE investor_transactions(

    investor_id TEXT,

    transaction_date TEXT,

    amfi_code INTEGER,

    transaction_type TEXT,

    amount_inr REAL,

    state TEXT,

    city TEXT,

    city_tier TEXT,

    age_group TEXT,

    gender TEXT,

    annual_income_lakh REAL,

    payment_mode TEXT,

    kyc_status TEXT
);

CREATE TABLE scheme_performance(

    amfi_code INTEGER,

    scheme_name TEXT,

    fund_house TEXT,

    category TEXT,

    plan TEXT,

    return_1yr_pct REAL,

    return_3yr_pct REAL,

    return_5yr_pct REAL,

    benchmark_3yr_pct REAL,

    alpha REAL,

    beta REAL,

    sharpe_ratio REAL,

    sortino_ratio REAL,

    std_dev_ann_pct REAL,

    max_drawdown_pct REAL,

    aum_crore REAL,

    expense_ratio_pct REAL,

    morningstar_rating INTEGER,

    risk_grade TEXT
);

CREATE TABLE aum_history(

    date TEXT,

    fund_house TEXT,

    aum_lakh_crore REAL,

    aum_crore REAL,

    num_schemes INTEGER
);