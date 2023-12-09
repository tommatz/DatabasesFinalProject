CREATE TABLE IF NOT EXISTS ORDER_HISTORY(
    uuid NOT NULL, 
    ticker NOT NULL, 
    date NOT NULL, 
    order_type NOT NULL, 
    cash_amount, 
    execution_time, 
    FOREIGN KEY(uuid) REFERENCES CUSTOMER(uuid), 
    PRIMARY KEY (uuid, date, ticker)
);