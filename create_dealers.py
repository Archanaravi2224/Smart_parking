import sqlite3

DATABASE = "gps_data.db"

def get_db_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows dictionary-style row access
    return conn

def initialize_database():
    """Creates tables and populates initial data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Dealers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dealers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            total_slots INTEGER DEFAULT 10
        )
    """)

    # Create Slots Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dealer_id INTEGER NOT NULL,
            status TEXT DEFAULT 'available',
            FOREIGN KEY (dealer_id) REFERENCES dealers(id)
        )
    """)

    # Insert Dealers
    cursor.execute("""
        INSERT OR IGNORE INTO dealers (id, name, password, total_slots)
        SELECT id, name, CAST(id AS TEXT) || 'abc', 10 FROM parking_areas;
    """)

    # Insert 10 slots per dealer
    cursor.execute("""
        INSERT INTO slots (dealer_id, status)
        SELECT dealers.id, 'available'
        FROM dealers, 
        (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 
         UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10);
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# **Add the missing functions:**

def get_dealer_by_id(dealer_id):
    """Fetch dealer details by ID."""
    conn = get_db_connection()
    dealer = conn.execute("SELECT * FROM dealers WHERE id = ?", (dealer_id,)).fetchone()
    conn.close()
    return dealer

def get_slots_by_dealer(dealer_id):
    """Fetch slot details for a specific dealer."""
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM slots WHERE dealer_id = ?", (dealer_id,)).fetchall()
    conn.close()
    return slots

def get_available_slots(parking_id):
    """Fetch only available slots for booking."""
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM slots WHERE dealer_id = ? AND status = 'available'", (parking_id,)).fetchall()
    conn.close()
    return slots
def get_all_slots(parking_id):
    """Fetch all slots (available & booked) for a given parking area."""
    conn = get_db_connection()
    
    # Fetch slot_id and status
    slots = conn.execute("SELECT id, status FROM slots WHERE dealer_id = ?", (parking_id,)).fetchall()
    
    conn.close()
    
    # Convert to list of dictionaries
    slot_list = [{"slot_id": slot[0], "status": slot[1]} for slot in slots]

    # Debugging: Print to ensure slot data is fetched
    print(f"🚀 Fetching Slots for Parking ID {parking_id}: {slot_list}")

    return slot_list


def update_slot_status(slot_id, status):
    """Update slot status (available/booked)."""
    conn = get_db_connection()
    conn.execute("UPDATE slots SET status = ? WHERE id = ?", (status, slot_id))
    conn.commit()
    conn.close()

def update_total_slots(dealer_id, new_slot_count):
    """Update the total slot count for a dealer and adjust the slots table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update dealer's total_slots
    cursor.execute("UPDATE dealers SET total_slots = ? WHERE id = ?", (new_slot_count, dealer_id))

    # Adjust slots table
    current_slots = cursor.execute("SELECT COUNT(*) FROM slots WHERE dealer_id = ?", (dealer_id,)).fetchone()[0]

    if new_slot_count > current_slots:
        slots_to_add = new_slot_count - current_slots
        for _ in range(slots_to_add):
            cursor.execute("INSERT INTO slots (dealer_id, status) VALUES (?, 'available')", (dealer_id,))
    elif new_slot_count < current_slots:
        slots_to_remove = current_slots - new_slot_count
        cursor.execute("DELETE FROM slots WHERE id IN (SELECT id FROM slots WHERE dealer_id = ? LIMIT ?)", 
                       (dealer_id, slots_to_remove))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
