import sqlite3
from datetime import date, timedelta


# Any medicine at or below this stock level is flagged as "low stock"
LOW_STOCK_THRESHOLD = 20


def get_connection():
    """Every function below calls this instead of repeating connect() + row_factory."""
    connection = sqlite3.connect("vetclinic.db")
    connection.row_factory = sqlite3.Row   # lets us access columns by name, e.g. row["name"]
    connection.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints (cascades, etc.)
    return connection


def format_currency(amount):
    """Single place to control how money is displayed across the whole app."""
    if amount is None:
        amount = 0.0
    return f"Rs. {amount:,.2f}"


# ============================================================
# OWNERS
# ============================================================

def add_owner(name, phone, address):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO owners (name,phone,address) VALUES (?,?,?)",
        (name, phone, address)
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def find_owner_by_phone(phone):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM owners WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def update_owner(owner_id, name, phone, address):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE owners SET name=?, phone=?, address=? WHERE id=?",
        (name, phone, address, owner_id)
    )
    connection.commit()
    connection.close()


# ============================================================
# PETS
# ============================================================

def add_pet(owner_id, name, species, breed):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO pets (owner_id, name, species, breed) VALUES (?, ?, ?, ?)",
        (owner_id, name, species, breed)
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_pets_by_owner(owner_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pets WHERE owner_id = ?", (owner_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    connection.close()
    return rows


def update_pet(pet_id, name, species, breed):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE pets SET name=?, species=?, breed=? WHERE id=?",
        (name, species, breed, pet_id)
    )
    connection.commit()
    connection.close()


# ============================================================
# VETS
# ============================================================

def get_all_vets():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vets ORDER BY name")
    rows = [dict(r) for r in cursor.fetchall()]
    connection.close()
    return rows


def get_vet(vet_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vets WHERE id = ?", (vet_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def update_vet(vet_id, name, specialty):
    """Used by the 'Manage Vets' screen to correct a vet's name or specialty."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE vets SET name=?, specialty=? WHERE id=?",
        (name, specialty, vet_id)
    )
    connection.commit()
    connection.close()


# ============================================================
# MEDICINES
# ============================================================

def get_all_medicines():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicines ORDER BY name")
    rows = [dict(r) for r in cursor.fetchall()]
    connection.close()
    return rows


def get_medicine(medicine_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def get_low_stock_medicines(threshold=LOW_STOCK_THRESHOLD):
    """Used to power the low-stock warning on the dashboard."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM medicines WHERE stock_qty <= ? ORDER BY stock_qty ASC",
        (threshold,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    connection.close()
    return rows


def update_medicine(medicine_id, stock_qty, price):
    """Used by the 'Manage Medicines' screen to restock or reprice a medicine."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE medicines SET stock_qty=?, price=? WHERE id=?",
        (stock_qty, price, medicine_id)
    )
    connection.commit()
    connection.close()


def reduce_medicine_stock(medicine_id, qty):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE medicines SET stock_qty = stock_qty - ? WHERE id = ?",
        (qty, medicine_id)
    )
    connection.commit()
    connection.close()


# ============================================================
# VISITS  (the 5-stage workflow)
# ============================================================

def create_visit(pet_id, vet_id, reason):
    """Stage 1: Reception."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO visits (pet_id, vet_id, reason, current_stage) VALUES (?, ?, ?, 'Reception')",
        (pet_id, vet_id, reason)
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_visit(visit_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT visits.*, pets.name AS pet_name, pets.species, pets.breed AS pet_breed,
               owners.id AS owner_id, owners.name AS owner_name,
               owners.phone AS owner_phone, owners.address AS owner_address,
               vets.name AS vet_name, medicines.name AS medicine_name
        FROM visits
        JOIN pets ON visits.pet_id = pets.id
        JOIN owners ON pets.owner_id = owners.id
        LEFT JOIN vets ON visits.vet_id = vets.id
        LEFT JOIN medicines ON visits.medicine_id = medicines.id
        WHERE visits.id = ?
    """, (visit_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None


def get_all_visits():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT visits.id, visits.current_stage, visits.visit_date,
               visits.total_cost, visits.payment_status,
               pets.name AS pet_name, owners.name AS owner_name,
               vets.name AS vet_name
        FROM visits
        JOIN pets ON visits.pet_id = pets.id
        JOIN owners ON pets.owner_id = owners.id
        LEFT JOIN vets ON visits.vet_id = vets.id
        ORDER BY visits.visit_date DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    connection.close()
    return rows


def get_visit_count():
    """
    Total number of visit rows currently in the table. Used for a purely
    cosmetic 'Visit No.' shown to staff, since the real id (AUTOINCREMENT)
    never gets reused after a delete and would otherwise show confusing gaps.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM visits")
    count = cursor.fetchone()[0]
    connection.close()
    return count


def cancel_visit(visit_id):
    """Marks a visit as cancelled instead of deleting it, so there's still a record."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE visits SET current_stage = 'Cancelled' WHERE id = ?",
        (visit_id,)
    )
    connection.commit()
    connection.close()


def delete_visit(visit_id):
    """Permanently removes a visit record. Used by the dashboard's Delete button."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM visits WHERE id = ?", (visit_id,))
    connection.commit()
    connection.close()


def update_visit_details(visit_id, vet_id, symptoms, diagnosis, weight_kg, temperature_c,
                          tests_ordered, test_results, consultation_fee, payment_status):
    """
    Lets staff correct a mistake on a visit that's already been saved,
    without pushing it forward or backward through the workflow stages.
    Recalculates total_cost from the (possibly edited) fee + existing medicine cost.
    """
    visit = get_visit(visit_id)
    medicine_cost = visit["medicine_cost"] or 0.0
    total_cost = consultation_fee + medicine_cost

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE visits SET vet_id=?, symptoms=?, diagnosis=?, weight_kg=?, temperature_c=?,
               tests_ordered=?, test_results=?, consultation_fee=?,
               total_cost=?, payment_status=?
        WHERE id=?
    """, (vet_id, symptoms, diagnosis, weight_kg, temperature_c, tests_ordered, test_results,
          consultation_fee, total_cost, payment_status, visit_id))
    connection.commit()
    connection.close()


def update_consultation(visit_id, symptoms, diagnosis, weight_kg, temperature_c):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE visits SET symptoms=?, diagnosis=?, weight_kg=?, temperature_c=?,
               current_stage='Diagnostics'
        WHERE id=?
    """, (symptoms, diagnosis, weight_kg, temperature_c, visit_id))
    connection.commit()
    connection.close()


def update_diagnostics(visit_id, tests_ordered, test_results):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE visits SET tests_ordered=?, test_results=?, current_stage='Treatment'
        WHERE id=?
    """, (tests_ordered, test_results, visit_id))
    connection.commit()
    connection.close()


def update_treatment(visit_id, medicine_id, medicine_qty, treatment_notes):
    medicine_cost = 0.0
    if medicine_id and medicine_qty:
        medicine = get_medicine(medicine_id)
        medicine_cost = medicine["price"] * medicine_qty
        reduce_medicine_stock(medicine_id, medicine_qty)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE visits SET medicine_id=?, medicine_qty=?, treatment_notes=?,
               medicine_cost=?, current_stage='Billing'
        WHERE id=?
    """, (medicine_id, medicine_qty, treatment_notes, medicine_cost, visit_id))
    connection.commit()
    connection.close()
    return medicine_cost


def finalize_billing(visit_id, consultation_fee, payment_status, next_checkup_in_days=None):
    visit = get_visit(visit_id)
    total = consultation_fee + (visit["medicine_cost"] or 0)

    next_checkup = None
    if next_checkup_in_days:
        next_checkup = (date.today() + timedelta(days=next_checkup_in_days)).isoformat()

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE visits SET consultation_fee=?, total_cost=?, payment_status=?,
               current_stage='Discharged', discharge_time=datetime('now'),
               next_checkup_date=?
        WHERE id=?
    """, (consultation_fee, total, payment_status, next_checkup, visit_id))
    connection.commit()
    connection.close()
    return total

