from db_handler import connect_to_db
from cleanup import register_cleanup, cleanup
from services.data_generation import populate_all_tables

conn, cur = connect_to_db()


# Main application logic
if __name__ == "__main__":
    try:
        print("Application is running...")
        # Simulate some work
        populate_all_tables() #Popola tabelle
    finally:
        #cleanup() #Svuota tabelle
        # Functions registered with atexit will be called automatically
        pass
