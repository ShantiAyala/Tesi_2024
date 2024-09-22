import atexit
import os
from db_handler import truncate_tables, close_db_connection, connect_to_db


def cleanup():
    """Cleanup function to truncate tables on program exit."""
    conn, cur = connect_to_db()
    truncate_tables(cur)
    close_db_connection(conn, cur)
    print("Cleanup complete: connection closed and tables truncated.")

def register_cleanup(cur, conn):
    """Register the truncation and cleanup functions to run on exit."""
    atexit.register(truncate_tables, cur)  # Register the table truncation
    atexit.register(cleanup)  # Register the cleanup of the database connection