#dock_view.py
import sqlite3
import json

def update_dock(id, dock_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Dock
                SET
                    location = ?,
                    capacity = ?
            WHERE id = ?
            """,
            (dock_data['location'], dock_data['capacity'], id)
        )

    return True if db_cursor.rowcount > 0 else False

def delete_dock(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Dock WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_docks():
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.location,
            d.capacity
        FROM Dock d
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        docks=[]
        for row in query_results:
            docks.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_docks = json.dumps(docks)

    return serialized_docks

def retrieve_dock(pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.location,
            d.capacity
        FROM Dock d
        WHERE d.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_dock = json.dumps(dict(query_results))

    return serialized_dock

# Defines create_dock which is a function that takes dock_data
# dock_data is a dictionary containing dock's information
def create_dock(dock_data):
    
    # Opens a connection to the shipping.db SQLite database
    with sqlite3.connect("./shipping.db") as conn:

        # Allows us to execute SQL statements
        db_cursor = conn.cursor()

        # Executes an INSERT INTO SQL statement to insert a new record
        # into the Dock table
        # The ? are placeholders that will be replaced with values from 
        # dock_data
        db_cursor.execute(
             """
            INSERT INTO Dock (location, capacity)
            VALUES (?, ?)
             """,
             (dock_data['location'], dock_data['capacity'])
        )
        
        # Retrieves the ID of the last row that was inserted into the table
        id = db_cursor.lastrowid

        # Returns the ID of the newly created dock as a JSON object
        return json.dumps({"id": id})
