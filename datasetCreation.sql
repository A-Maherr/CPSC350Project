CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE COLLATE NOCASE
);
 
CREATE TABLE IF NOT EXISTS Income(
    user_id INTEGER,
    monthly_income DECIMAL,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Expense_type(
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each expense type
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Expenses(
    user_id INT,
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each expense
    type_id INTEGER,
    amount DECIMAL,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES Users(id),
    FOREIGN KEY(type_id) REFERENCES Expense_type(id)
);

CREATE TABLE IF NOT EXISTS Remainder( -- to track remaining income after expenses
    user_id INTEGER,
    amount DECIMAL,
    FOREIGN KEY(user_id) REFERENCES Users(id)
);

-- INSERTING THE CATEGROIES INTO THE EXPENSE_TYPE TABLE

INSERT INTO Expense_type VALUES(1, 'Housing');
INSERT INTO Expense_type VALUES(2, 'Transportation');
INSERT INTO Expense_type VALUES(3, 'Groceries');
INSERT INTO Expense_type VALUES(4, 'Utilities');
INSERT INTO Expense_type VALUES(5, 'Clothing');
INSERT INTO Expense_type VALUES(6, 'Healthcare');
INSERT INTO Expense_type VALUES(7, 'Personal Care');
INSERT INTO Expense_type VALUES(8, 'Debt Payments');
INSERT INTO Expense_type VALUES(9, 'Miscellaneous');









