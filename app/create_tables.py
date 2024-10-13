from sqlalchemy import create_engine, text

# Define your database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Adjust this for your database

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define your SQL query for creating the products table
create_table_query = """
CREATE TABLE IF NOT EXISTS products (
   id INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   description TEXT,
   price REAL
);
"""

# Execute the SQL command to create the table
with engine.connect() as connection:
    connection.execute(text(create_table_query))  # Use text() for raw SQL
    print("Table 'products' created successfully.")
