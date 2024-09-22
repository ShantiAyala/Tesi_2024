import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd

# Define your database connection parameters
conn_params = {
    "host": "localhost",
    "dbname": "farm_db",
    "user": "postgres",
    "password": "pollo54",
    #"password": "postgres", #decommenta questa linea se la tua password è postgres
    "port": "5432" 
}

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True  
    cur = conn.cursor()
    return conn, cur

def close_db_connection(conn, cur):
    """Chiude il cursore e la connessione al database."""
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Database connection closed.")
    
def truncate_tables(cur):
    """Truncate all tables in the 'public' schema."""
    cur.execute("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cur.fetchall()  

    for table in tables:
        cur.execute(sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(
            sql.Identifier(table[0])  
        ))
    print("All tables have been truncated.")

#----------------------------------


def get_connection():
    # Crea l'engine SQLAlchemy
    engine = create_engine('postgresql+psycopg2://postgres:pollo54@localhost/farm_db')
    #decommenta questa linea se la tua password è postgres
    #engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/farm_db')
    return engine

def fetch_data(query):
    # Ottieni il motore di connessione
    engine = get_connection()
    
    # Esegui la query e carica i dati in un DataFrame Pandas
    df = pd.read_sql(query, engine)
    
    return df

def fetch_2data(query, params):
    
    engine = get_connection()
    df = pd.read_sql(query, engine, params=params)
    
    return df