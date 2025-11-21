# Python Generators – Database Seeding and Row Streaming

This project introduces **Python generators**, **MySQL database creation**, and **dataset population using CSV files**.  
You will build a script (`seed.py`) that sets up a MySQL database, creates a table, inserts CSV data, and later implements a generator to stream database rows **one at a time**.

---

## Project Overview

The goal of this project is to:

- Connect to a MySQL server  
- Create a database named **`ALX_prodev`**  
- Create a table named **`user_data`**  
- Populate the table using `user_data.csv`  
- Stream rows using a Python generator (later tasks)

You are provided with `0-main.py`, which calls your functions in `seed.py`.

---

## Project Structure

python-generators-0x00/
├── seed.py
├── 0-main.py
├── user_data.csv
└── README.md


---

## Database Requirements

**Database:** `ALX_prodev`  

**Table:** `user_data`

| Field    | Type          | Attributes        |
|----------|---------------|-----------------|
| user_id  | CHAR(36)      | PRIMARY KEY, UUID |
| name     | VARCHAR(255)  | NOT NULL         |
| email    | VARCHAR(255)  | NOT NULL         |
| age      | DECIMAL(10,2) | NOT NULL         |

> The table is created only if it does not exist.

---

## Functions in `seed.py`

### `connect_db()`
Connects to the MySQL server (without selecting a database).

### `create_database(connection)`
Creates the `ALX_prodev` database if it does not already exist.

### `connect_to_prodev()`
Connects directly to the `ALX_prodev` database.

### `create_table(connection)`
Creates the `user_data` table with the required fields.

### `insert_data(connection, csv_file)`
Inserts records from `user_data.csv` using:

- `csv.DictReader`
- `INSERT IGNORE` to avoid duplicates

---

## CSV File

The CSV file is usually provided via an S3 link. If your browser displays the data instead of downloading:

1. **Right-click → Save As…** and name it `user_data.csv`, OR  
2. Copy/paste the content into a new file named `user_data.csv`, OR  
3. Use the terminal:

```bash
curl -o user_data.csv https://example-s3-link/user_data.csv
