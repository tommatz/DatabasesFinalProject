CREATE TABLE IF NOT EXISTS STRATEGIES(
    uuid NOT NULL,
    strategy_type NOT NULL,
    ticker NOT NULL, 
    percent_cash_per_order NOT NULL, 
    FOREIGN KEY(uuid) REFERENCES CUSTOMER(uuid), 
    PRIMARY KEY (uuid, ticker)
);