
import sqlite3

DB_FILE = "vetclinic.db"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT,
    dob DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id) ON DELETE CASCADE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT DEFAULT 'General Practice'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 0,
    price REAL NOT NULL DEFAULT 0.00,
    expiry_date DATE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    vet_id INTEGER,
    visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    current_stage TEXT NOT NULL DEFAULT 'Reception',

    symptoms TEXT,
    diagnosis TEXT,
    weight_kg REAL,
    temperature_c REAL,

    tests_ordered TEXT,
    test_results TEXT,

    medicine_id INTEGER,
    medicine_qty INTEGER DEFAULT 0,
    treatment_notes TEXT,

    consultation_fee REAL DEFAULT 500.00,
    medicine_cost REAL DEFAULT 0.00,
    total_cost REAL DEFAULT 0.00,
    payment_status TEXT DEFAULT 'Unpaid',

    discharge_time TIMESTAMP,
    next_checkup_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    FOREIGN KEY (vet_id) REFERENCES vets(id) ON DELETE SET NULL,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE SET NULL
)
""")

# Seed some starting data so the app isn't empty on first run
cursor.execute("SELECT COUNT(*) FROM vets")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO vets (name, specialty) VALUES (?, ?)",
        [
            ("Dr. Amara Silva", "General Practice"),
            ("Dr. Ravi Perera", "Surgery"),
            ("Dr. Nadia Fernando", "Dermatology"),
        ]
    )

cursor.execute("SELECT COUNT(*) FROM medicines")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO medicines (name, stock_qty, price, expiry_date) VALUES (?, ?, ?, ?)",
        [
            ("Amoxicillin 250mg", 100, 15.00, "2027-06-01"),
            ("Rabies Vaccine", 50, 45.00, "2027-01-15"),
            ("Deworming Tablet", 200, 8.50, "2027-09-01"),
            ("Pain Relief Injection", 60, 22.00, "2026-12-01"),
            ("Antiseptic Spray", 80, 12.00, "2027-03-10"),
        ]
    )

connection.commit()
connection.close()
print("All 5 tables created and seed data added!")