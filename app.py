import tkinter as tk
from tkinter import ttk, messagebox
import store


BG_COLOR = "#d9f2d9"
CARD_COLOR = "white"
PRIMARY_COLOR = "#2F6B5E"
TEXT_COLOR = "#1E2A28"
WARNING_COLOR = "#B33A3A"
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")

def is_valid_phone(phone):
    phone = phone.strip()
    return phone.isdigit() and 10 <= len(phone) <= 15


window = tk.Tk()
window.title("VetClinic")
window.geometry("1000x700")
window.minsize(800, 600)
window.config(bg=BG_COLOR)
icon_image = tk.PhotoImage(file="images/vetclinic_icon.png")
window.iconphoto(True, icon_image)


active_visit_id = None


# =========================================================
# FRAME 0: LOGIN
# =========================================================
login_frame = tk.Frame(window, bg=PRIMARY_COLOR)

login_card = tk.Frame(login_frame, bg=PRIMARY_COLOR)
login_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(login_card, text="🐾 VetClinic ERP", bg=PRIMARY_COLOR, fg="white",
         font=("Segoe UI", 22, "bold")).pack(pady=(0, 40))

tk.Label(login_card, text="Username", bg=PRIMARY_COLOR, fg="white",
         font=FONT_NORMAL).pack()
login_username_entry = tk.Entry(login_card, width=30, font=FONT_NORMAL, justify="center")
login_username_entry.pack(pady=(5, 20))

tk.Label(login_card, text="Password", bg=PRIMARY_COLOR, fg="white",
         font=FONT_NORMAL).pack()
login_password_entry = tk.Entry(login_card, width=30, font=FONT_NORMAL, justify="center", show="*")
login_password_entry.pack(pady=(5, 30))


def login_clicked():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning("Missing info", "Please enter both username and password.")
        return

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful!", "Welcome to VetClinic ERP!")
        load_dashboard()
        show_frame(dashboard_frame)
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


tk.Button(login_card, text="Login", command=login_clicked,
          bg="white", fg=PRIMARY_COLOR, font=FONT_BOLD, padx=30, pady=8, bd=0
          ).pack()


# =========================================================
# FRAME 1: RECEPTION
# =========================================================
reception_frame = tk.Frame(window, bg=BG_COLOR)

reception_card = tk.Frame(reception_frame, bg=CARD_COLOR, padx=40, pady=30)
reception_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(reception_card, text="🐾 VetClinic Reception", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

tk.Label(reception_card, text="Owner Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
owner_name_entry = tk.Entry(reception_card, width=35, font=FONT_NORMAL)
owner_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(reception_card, text="Owner Phone:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=10, sticky="w")
owner_phone_entry = tk.Entry(reception_card, width=35, font=FONT_NORMAL)
owner_phone_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(reception_card, text="Pet Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=3, column=0, padx=10, pady=10, sticky="w")
pet_name_entry = tk.Entry(reception_card, width=35, font=FONT_NORMAL)
pet_name_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(reception_card, text="Species:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=4, column=0, padx=10, pady=10, sticky="w")
species_entry = tk.Entry(reception_card, width=35, font=FONT_NORMAL)
species_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(reception_card, text="Breed:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=5, column=0, padx=10, pady=10, sticky="w")
breed_entry = tk.Entry(reception_card, width=35, font=FONT_NORMAL)
breed_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(reception_card, text="Assigned Vet:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=6, column=0, padx=10, pady=10, sticky="w")
vet_var = tk.StringVar()
vet_combo = ttk.Combobox(reception_card, textvariable=vet_var, width=32, state="readonly")
vet_combo.grid(row=6, column=1, padx=10, pady=10)

vet_lookup = {}


def load_vets_into_dropdown():
    global vet_lookup
    vets = store.get_all_vets()
    vet_lookup = {f"{v['name']} ({v['specialty']})": v["id"] for v in vets}
    vet_combo["values"] = list(vet_lookup.keys())
    if vet_lookup and not vet_var.get():
        vet_combo.current(0)


load_vets_into_dropdown()


def clear_reception_form():
    owner_name_entry.delete(0, tk.END)
    owner_phone_entry.delete(0, tk.END)
    pet_name_entry.delete(0, tk.END)
    species_entry.delete(0, tk.END)
    breed_entry.delete(0, tk.END)
    load_vets_into_dropdown()
    if vet_lookup:
        vet_combo.current(0)


def save_clicked():
    global active_visit_id

    owner_name = owner_name_entry.get()
    owner_phone = owner_phone_entry.get()
    pet_name = pet_name_entry.get()
    species = species_entry.get()
    breed = breed_entry.get()
    selected_vet_text = vet_var.get()

    if owner_name == "" or owner_phone == "" or pet_name == "":
        messagebox.showwarning("Missing info", "Please fill in all fields.")
        return

    if not is_valid_phone(owner_phone):
        messagebox.showwarning(
            "Invalid phone number",
            "Phone number must be digits only, between 10 and 15 digits long."
        )
        return

    vet_id = vet_lookup.get(selected_vet_text)
    if not vet_id:
        messagebox.showwarning("Missing info", "Please select a vet.")
        return

    owner_id = store.add_owner(owner_name, owner_phone, "")
    pet_id = store.add_pet(owner_id, pet_name, species, breed)
    visit_id = store.create_visit(pet_id, vet_id, "Checkup")

    active_visit_id = visit_id
    messagebox.showinfo("Saved", f"Visit #{store.get_visit_count()} created!")
    show_frame(consultation_frame)


def reception_cancel_clicked():
    if messagebox.askyesno("Cancel", "Discard this new visit and return to the dashboard?"):
        clear_reception_form()
        load_dashboard()
        show_frame(dashboard_frame)


reception_button_row = tk.Frame(reception_card, bg=CARD_COLOR)
reception_button_row.grid(row=7, column=0, columnspan=2, pady=(25, 0))

tk.Button(reception_button_row, text="Cancel", command=reception_cancel_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(reception_button_row, text="Save & Continue", command=save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 2: CONSULTATION
# =========================================================
consultation_frame = tk.Frame(window, bg=BG_COLOR)

consultation_card = tk.Frame(consultation_frame, bg=CARD_COLOR, padx=40, pady=30)
consultation_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(consultation_card, text="🩺 Consultation", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

tk.Label(consultation_card, text="Symptoms:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
symptoms_entry = tk.Entry(consultation_card, width=35, font=FONT_NORMAL)
symptoms_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(consultation_card, text="Diagnosis:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=10, sticky="w")
diagnosis_entry = tk.Entry(consultation_card, width=35, font=FONT_NORMAL)
diagnosis_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(consultation_card, text="Weight (kg):", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=3, column=0, padx=10, pady=10, sticky="w")
weight_entry = tk.Entry(consultation_card, width=35, font=FONT_NORMAL)
weight_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(consultation_card, text="Temperature (°C):", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=4, column=0, padx=10, pady=10, sticky="w")
temperature_entry = tk.Entry(consultation_card, width=35, font=FONT_NORMAL)
temperature_entry.grid(row=4, column=1, padx=10, pady=10)


def consultation_save_clicked():
    symptoms = symptoms_entry.get()
    diagnosis = diagnosis_entry.get()
    weight_text = weight_entry.get()
    temperature_text = temperature_entry.get()

    try:
        weight = float(weight_text) if weight_text else None
        temperature = float(temperature_text) if temperature_text else None
    except ValueError:
        messagebox.showwarning("Invalid input", "Weight and temperature must be numbers.")
        return

    store.update_consultation(active_visit_id, symptoms, diagnosis, weight, temperature)
    messagebox.showinfo("Saved", "Consultation saved!")
    show_frame(diagnostics_frame)


def visit_cancel_clicked():
    """Shared cancel handler for any stage after a visit already exists."""
    if messagebox.askyesno("Cancel Visit", "Cancel this visit and return to the dashboard?"):
        store.cancel_visit(active_visit_id)
        load_dashboard()
        show_frame(dashboard_frame)


consultation_button_row = tk.Frame(consultation_card, bg=CARD_COLOR)
consultation_button_row.grid(row=5, column=0, columnspan=2, pady=(25, 0))

tk.Button(consultation_button_row, text="◀ Back", command=lambda: show_frame(reception_frame),
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(consultation_button_row, text="Cancel", command=visit_cancel_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(consultation_button_row, text="Save", command=consultation_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 3: DIAGNOSTICS
# =========================================================
diagnostics_frame = tk.Frame(window, bg=BG_COLOR)

diagnostics_card = tk.Frame(diagnostics_frame, bg=CARD_COLOR, padx=40, pady=30)
diagnostics_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(diagnostics_card, text="🔬 Diagnostics", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

tk.Label(diagnostics_card, text="Tests Ordered:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
tests_ordered_entry = tk.Entry(diagnostics_card, width=35, font=FONT_NORMAL)
tests_ordered_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(diagnostics_card, text="Test Results:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=10, sticky="w")
test_results_entry = tk.Entry(diagnostics_card, width=35, font=FONT_NORMAL)
test_results_entry.grid(row=2, column=1, padx=10, pady=10)


def diagnostics_save_clicked():
    tests_ordered = tests_ordered_entry.get()
    test_results = test_results_entry.get()

    store.update_diagnostics(active_visit_id, tests_ordered, test_results)
    messagebox.showinfo("Saved", "Diagnostics saved!")
    load_medicines_into_dropdown()
    show_frame(treatment_frame)


diagnostics_button_row = tk.Frame(diagnostics_card, bg=CARD_COLOR)
diagnostics_button_row.grid(row=3, column=0, columnspan=2, pady=(25, 0))

tk.Button(diagnostics_button_row, text="◀ Back", command=lambda: show_frame(consultation_frame),
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(diagnostics_button_row, text="Cancel", command=visit_cancel_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(diagnostics_button_row, text="Save", command=diagnostics_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 4: TREATMENT
# =========================================================
treatment_frame = tk.Frame(window, bg=BG_COLOR)

treatment_card = tk.Frame(treatment_frame, bg=CARD_COLOR, padx=40, pady=30)
treatment_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(treatment_card, text="💊 Treatment", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

tk.Label(treatment_card, text="Medicine:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
medicine_var = tk.StringVar()
medicine_combo = ttk.Combobox(treatment_card, textvariable=medicine_var, width=32, state="readonly")
medicine_combo.grid(row=1, column=1, padx=10, pady=10)

tk.Label(treatment_card, text="Quantity:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=10, sticky="w")
quantity_entry = tk.Entry(treatment_card, width=35, font=FONT_NORMAL)
quantity_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(treatment_card, text="Notes:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=3, column=0, padx=10, pady=10, sticky="w")
treatment_notes_entry = tk.Entry(treatment_card, width=35, font=FONT_NORMAL)
treatment_notes_entry.grid(row=3, column=1, padx=10, pady=10)

# Low-stock warning label, shown above the buttons when relevant
treatment_low_stock_label = tk.Label(treatment_card, text="", bg=CARD_COLOR,
                                      fg=WARNING_COLOR, font=FONT_BOLD, wraplength=380,
                                      justify="left")
treatment_low_stock_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="w")

medicine_lookup = {}


def load_medicines_into_dropdown():
    global medicine_lookup
    medicines = store.get_all_medicines()
    medicine_lookup = {}
    for m in medicines:
        label = f"{m['name']} (stock: {m['stock_qty']})"
        if m["stock_qty"] <= store.LOW_STOCK_THRESHOLD:
            label += "  ⚠️ LOW STOCK"
        medicine_lookup[label] = m["id"]
    medicine_combo["values"] = list(medicine_lookup.keys())

    low_stock = store.get_low_stock_medicines()
    if low_stock:
        names = ", ".join(m["name"] for m in low_stock)
        treatment_low_stock_label.config(text=f"⚠️ Low stock: {names}")
    else:
        treatment_low_stock_label.config(text="")


def treatment_save_clicked():
    selected_text = medicine_var.get()
    medicine_id = medicine_lookup.get(selected_text)
    quantity_text = quantity_entry.get()
    notes = treatment_notes_entry.get()

    if not medicine_id:
        messagebox.showwarning("Missing info", "Please select a medicine.")
        return

    try:
        quantity = int(quantity_text) if quantity_text else 0
    except ValueError:
        messagebox.showwarning("Invalid input", "Quantity must be a whole number.")
        return

    medicine = store.get_medicine(medicine_id)
    if quantity > medicine["stock_qty"]:
        messagebox.showwarning(
            "Insufficient stock",
            f"Only {medicine['stock_qty']} units of {medicine['name']} available."
        )
        return

    cost = store.update_treatment(active_visit_id, medicine_id, quantity, notes)
    messagebox.showinfo("Saved", f"Treatment saved! Medicine cost: {store.format_currency(cost)}")
    show_frame(billing_frame)
    load_billing_screen()


treatment_button_row = tk.Frame(treatment_card, bg=CARD_COLOR)
treatment_button_row.grid(row=5, column=0, columnspan=2, pady=(20, 0))

tk.Button(treatment_button_row, text="◀ Back", command=lambda: show_frame(diagnostics_frame),
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(treatment_button_row, text="Cancel", command=visit_cancel_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(treatment_button_row, text="Save & Continue", command=treatment_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 5: BILLING
# =========================================================
billing_frame = tk.Frame(window, bg=BG_COLOR)

billing_card = tk.Frame(billing_frame, bg=CARD_COLOR, padx=40, pady=30)
billing_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(billing_card, text="🧾 Billing", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

tk.Label(billing_card, text="Consultation Fee:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
fee_entry = tk.Entry(billing_card, width=35, font=FONT_NORMAL)
fee_entry.insert(0, "500.00")
fee_entry.grid(row=1, column=1, padx=10, pady=10)

medicine_cost_label = tk.Label(billing_card, text=f"Medicine cost: {store.format_currency(0)}",
                                bg=CARD_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL)
medicine_cost_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

total_label = tk.Label(billing_card, text=f"Total: {store.format_currency(0)}", bg=CARD_COLOR,
                        fg=PRIMARY_COLOR, font=("Segoe UI", 16, "bold"))
total_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

tk.Label(billing_card, text="Payment Status:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=4, column=0, padx=10, pady=10, sticky="w")
payment_var = tk.StringVar(value="Paid")
tk.Radiobutton(billing_card, text="Paid", variable=payment_var, value="Paid", bg=CARD_COLOR
               ).grid(row=4, column=1, sticky="w")
tk.Radiobutton(billing_card, text="Unpaid", variable=payment_var, value="Unpaid", bg=CARD_COLOR
               ).grid(row=5, column=1, sticky="w")

current_medicine_cost = 0.0


def load_billing_screen():
    global current_medicine_cost
    visit = store.get_visit(active_visit_id)
    current_medicine_cost = visit["medicine_cost"] or 0.0
    medicine_cost_label.config(text=f"Medicine cost: {store.format_currency(current_medicine_cost)}")
    recalculate_total()


def recalculate_total(*args):
    try:
        fee = float(fee_entry.get())
    except ValueError:
        fee = 0.0
    total = fee + current_medicine_cost
    total_label.config(text=f"Total: {store.format_currency(total)}")


fee_entry.bind("<KeyRelease>", recalculate_total)


def billing_finalize_clicked():
    try:
        fee = float(fee_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid input", "Consultation fee must be a number.")
        return

    total = store.finalize_billing(active_visit_id, fee, payment_var.get(), next_checkup_in_days=30)
    messagebox.showinfo("Discharged", f"Visit complete! Total billed: {store.format_currency(total)}")
    load_dashboard()
    show_frame(dashboard_frame)


billing_button_row = tk.Frame(billing_card, bg=CARD_COLOR)
billing_button_row.grid(row=6, column=0, columnspan=2, pady=(25, 0))

tk.Button(billing_button_row, text="◀ Back", command=lambda: show_frame(treatment_frame),
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(billing_button_row, text="Cancel", command=visit_cancel_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(billing_button_row, text="Finalize & Discharge", command=billing_finalize_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 6: DASHBOARD
# =========================================================
dashboard_frame = tk.Frame(window, bg=BG_COLOR)

dashboard_card = tk.Frame(dashboard_frame, bg=CARD_COLOR, padx=30, pady=25)
dashboard_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(dashboard_card, text="📊 Dashboard", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 5))

# Low-stock banner, refreshed every time the dashboard loads
dashboard_low_stock_label = tk.Label(dashboard_card, text="", bg=CARD_COLOR,
                                      fg=WARNING_COLOR, font=FONT_BOLD, wraplength=500,
                                      justify="left")
dashboard_low_stock_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w")

tk.Label(dashboard_card, text="Search (pet / owner / stage):", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
search_entry = tk.Entry(dashboard_card, width=30, font=FONT_NORMAL)
search_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="w")
search_entry.bind("<KeyRelease>", lambda e: load_dashboard())

columns = ("no", "pet", "owner", "vet", "stage", "total", "payment")
visits_table = ttk.Treeview(dashboard_card, columns=columns, show="headings", height=15)

visits_table.heading("no", text="Visit No.")
visits_table.heading("pet", text="Pet")
visits_table.heading("owner", text="Owner")
visits_table.heading("vet", text="Vet")
visits_table.heading("stage", text="Stage")
visits_table.heading("total", text="Total")
visits_table.heading("payment", text="Payment")

visits_table.column("no", width=70, anchor="center")
visits_table.column("pet", width=110)
visits_table.column("owner", width=130)
visits_table.column("vet", width=130)
visits_table.column("stage", width=100)
visits_table.column("total", width=100, anchor="center")
visits_table.column("payment", width=80, anchor="center")

visits_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def load_dashboard():
    for row in visits_table.get_children():
        visits_table.delete(row)

    query = search_entry.get().lower()
    visits = store.get_all_visits()  # newest first from the database

    # Visit No. is just "position among visits that still exist," oldest = 1.
    # This stays clean and contiguous even after deletions, unlike the raw
    # database id (which is never reused once assigned).
    visits_oldest_first = list(reversed(visits))
    visit_number_by_id = {
        v["id"]: position
        for position, v in enumerate(visits_oldest_first, start=1)
    }

    for v in visits_oldest_first:
        # Search now matches pet name, owner name, OR current stage (e.g. "unpaid"/"billing")
        matches_pet = query in v["pet_name"].lower()
        matches_owner = query in v["owner_name"].lower()
        matches_stage = query in v["current_stage"].lower()
        matches_payment = query in (v["payment_status"] or "").lower()

        if query and not (matches_pet or matches_owner or matches_stage or matches_payment):
            continue

        total_display = store.format_currency(v["total_cost"]) if v["total_cost"] else "-"
        visits_table.insert("", "end", iid=str(v["id"]), values=(
            visit_number_by_id[v["id"]], v["pet_name"], v["owner_name"], v["vet_name"] or "-",
            v["current_stage"], total_display, v["payment_status"]
        ))

    # Refresh the low-stock banner every time the dashboard is loaded
    low_stock = store.get_low_stock_medicines()
    if low_stock:
        names = ", ".join(f"{m['name']} ({m['stock_qty']} left)" for m in low_stock)
        dashboard_low_stock_label.config(text=f"⚠️ Low stock alert: {names}")
    else:
        dashboard_low_stock_label.config(text="")


def edit_visit_clicked():
    selected = visits_table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a visit in the table to edit.")
        return
    visit_id = int(selected[0])
    load_edit_visit(visit_id)
    show_frame(edit_visit_frame)


def delete_visit_clicked():
    selected = visits_table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a visit in the table to delete.")
        return

    visit_id = int(selected[0])
    visit = store.get_visit(visit_id)
    label = f"{visit['pet_name']} ({visit['owner_name']})" if visit else f"visit #{visit_id}"

    if messagebox.askyesno(
        "Delete Visit",
        f"Permanently delete the visit record for {label}? This cannot be undone."
    ):
        store.delete_visit(visit_id)
        load_dashboard()


dashboard_button_row = tk.Frame(dashboard_card, bg=CARD_COLOR)
dashboard_button_row.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky="we")

tk.Button(dashboard_button_row, text="🔄 Refresh", command=load_dashboard,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(dashboard_button_row, text="✏️ Edit Visit", command=edit_visit_clicked,
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(dashboard_button_row, text="🗑️ Delete Visit", command=delete_visit_clicked,
          bg=WARNING_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(dashboard_button_row, text="💊 Manage Medicines",
          command=lambda: [load_medicines_management(), show_frame(medicines_frame)],
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(dashboard_button_row, text="🩺 Manage Vets",
          command=lambda: [load_vets_management(), show_frame(vets_frame)],
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(dashboard_button_row, text="+ New Visit", command=lambda: show_frame(reception_frame),
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=6, bd=0
          ).pack(side="right")


# =========================================================
# FRAME 7: EDIT VISIT
# =========================================================
edit_visit_frame = tk.Frame(window, bg=BG_COLOR)

edit_visit_card = tk.Frame(edit_visit_frame, bg=CARD_COLOR, padx=40, pady=25)
edit_visit_card.place(relx=0.5, rely=0.5, anchor="center")

edit_visit_id = None  # which visit is currently loaded in this form

tk.Label(edit_visit_card, text="✏️ Edit Visit", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

edit_fields = {}


def add_edit_field(row, label_text, key, width=35):
    tk.Label(edit_visit_card, text=label_text, bg=CARD_COLOR, fg=TEXT_COLOR,
             font=FONT_NORMAL).grid(row=row, column=0, padx=10, pady=6, sticky="w")
    entry = tk.Entry(edit_visit_card, width=width, font=FONT_NORMAL)
    entry.grid(row=row, column=1, padx=10, pady=6)
    edit_fields[key] = entry


add_edit_field(1, "Owner Name:", "owner_name")
add_edit_field(2, "Owner Phone:", "owner_phone")
add_edit_field(3, "Pet Name:", "pet_name")
add_edit_field(4, "Species:", "species")
add_edit_field(5, "Breed:", "breed")

tk.Label(edit_visit_card, text="Assigned Vet:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=6, column=0, padx=10, pady=6, sticky="w")
edit_vet_var = tk.StringVar()
edit_vet_combo = ttk.Combobox(edit_visit_card, textvariable=edit_vet_var, width=32, state="readonly")
edit_vet_combo.grid(row=6, column=1, padx=10, pady=6)
edit_vet_lookup = {}

add_edit_field(7, "Symptoms:", "symptoms")
add_edit_field(8, "Diagnosis:", "diagnosis")
add_edit_field(9, "Weight (kg):", "weight")
add_edit_field(10, "Temperature (°C):", "temperature")
add_edit_field(11, "Tests Ordered:", "tests_ordered")
add_edit_field(12, "Test Results:", "test_results")
add_edit_field(13, "Consultation Fee:", "consultation_fee")

tk.Label(edit_visit_card, text="Payment Status:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=14, column=0, padx=10, pady=6, sticky="w")
edit_payment_var = tk.StringVar(value="Unpaid")
edit_payment_row = tk.Frame(edit_visit_card, bg=CARD_COLOR)
edit_payment_row.grid(row=14, column=1, sticky="w")
tk.Radiobutton(edit_payment_row, text="Paid", variable=edit_payment_var, value="Paid",
               bg=CARD_COLOR).pack(side="left")
tk.Radiobutton(edit_payment_row, text="Unpaid", variable=edit_payment_var, value="Unpaid",
               bg=CARD_COLOR).pack(side="left")


def _set_entry(key, value):
    edit_fields[key].delete(0, tk.END)
    if value is not None:
        edit_fields[key].insert(0, str(value))


def load_edit_visit(visit_id):
    global edit_visit_id, edit_vet_lookup
    edit_visit_id = visit_id
    visit = store.get_visit(visit_id)

    vets = store.get_all_vets()
    edit_vet_lookup = {f"{v['name']} ({v['specialty']})": v["id"] for v in vets}
    edit_vet_combo["values"] = list(edit_vet_lookup.keys())
    current_vet_label = next(
        (label for label, vid in edit_vet_lookup.items() if vid == visit["vet_id"]), ""
    )
    edit_vet_var.set(current_vet_label)

    _set_entry("owner_name", visit["owner_name"])
    _set_entry("owner_phone", visit["owner_phone"])
    _set_entry("pet_name", visit["pet_name"])
    _set_entry("species", visit["species"])
    _set_entry("breed", visit["pet_breed"])
    _set_entry("symptoms", visit["symptoms"])
    _set_entry("diagnosis", visit["diagnosis"])
    _set_entry("weight", visit["weight_kg"])
    _set_entry("temperature", visit["temperature_c"])
    _set_entry("tests_ordered", visit["tests_ordered"])
    _set_entry("test_results", visit["test_results"])
    _set_entry("consultation_fee", visit["consultation_fee"] if visit["consultation_fee"] else 500.00)
    edit_payment_var.set(visit["payment_status"] or "Unpaid")


def edit_visit_save_clicked():
    owner_name = edit_fields["owner_name"].get()
    owner_phone = edit_fields["owner_phone"].get()
    pet_name = edit_fields["pet_name"].get()
    species = edit_fields["species"].get()
    breed = edit_fields["breed"].get()

    if owner_name == "" or owner_phone == "" or pet_name == "":
        messagebox.showwarning("Missing info", "Owner name, phone, and pet name are required.")
        return

    if not is_valid_phone(owner_phone):
        messagebox.showwarning(
            "Invalid phone number",
            "Phone number must be digits only, between 10 and 15 digits long."
        )
        return

    vet_id = edit_vet_lookup.get(edit_vet_var.get())
    if not vet_id:
        messagebox.showwarning("Missing info", "Please select a vet.")
        return

    try:
        weight = float(edit_fields["weight"].get()) if edit_fields["weight"].get() else None
        temperature = float(edit_fields["temperature"].get()) if edit_fields["temperature"].get() else None
        consultation_fee = float(edit_fields["consultation_fee"].get()) if edit_fields["consultation_fee"].get() else 0.0
    except ValueError:
        messagebox.showwarning("Invalid input", "Weight, temperature, and fee must be numbers.")
        return

    visit = store.get_visit(edit_visit_id)
    store.update_owner(visit["owner_id"], owner_name, owner_phone, "")
    store.update_pet(visit["pet_id"], pet_name, species, breed)
    store.update_visit_details(
        edit_visit_id,
        vet_id,
        edit_fields["symptoms"].get(),
        edit_fields["diagnosis"].get(),
        weight,
        temperature,
        edit_fields["tests_ordered"].get(),
        edit_fields["test_results"].get(),
        consultation_fee,
        edit_payment_var.get()
    )

    messagebox.showinfo("Updated", "Visit updated successfully!")
    load_dashboard()
    show_frame(dashboard_frame)


edit_visit_button_row = tk.Frame(edit_visit_card, bg=CARD_COLOR)
edit_visit_button_row.grid(row=15, column=0, columnspan=2, pady=(20, 0))

tk.Button(edit_visit_button_row, text="◀ Back to Dashboard",
          command=lambda: [load_dashboard(), show_frame(dashboard_frame)],
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(edit_visit_button_row, text="Save Changes", command=edit_visit_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 8: MANAGE MEDICINES
# =========================================================
medicines_frame = tk.Frame(window, bg=BG_COLOR)

medicines_card = tk.Frame(medicines_frame, bg=CARD_COLOR, padx=30, pady=25)
medicines_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(medicines_card, text="💊 Manage Medicines", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

medicine_columns = ("name", "stock", "price")
medicines_table = ttk.Treeview(medicines_card, columns=medicine_columns, show="headings", height=10)
medicines_table.heading("name", text="Medicine")
medicines_table.heading("stock", text="Stock Qty")
medicines_table.heading("price", text="Price")
medicines_table.column("name", width=220)
medicines_table.column("stock", width=100, anchor="center")
medicines_table.column("price", width=120, anchor="center")
medicines_table.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

tk.Label(medicines_card, text="New Stock Qty:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=8, sticky="w")
medicine_stock_entry = tk.Entry(medicines_card, width=20, font=FONT_NORMAL)
medicine_stock_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")

tk.Label(medicines_card, text="New Price:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=3, column=0, padx=10, pady=8, sticky="w")
medicine_price_entry = tk.Entry(medicines_card, width=20, font=FONT_NORMAL)
medicine_price_entry.grid(row=3, column=1, padx=10, pady=8, sticky="w")


def load_medicines_management():
    for row in medicines_table.get_children():
        medicines_table.delete(row)
    for m in store.get_all_medicines():
        medicines_table.insert("", "end", iid=str(m["id"]), values=(
            m["name"], m["stock_qty"], store.format_currency(m["price"])
        ))
    medicine_stock_entry.delete(0, tk.END)
    medicine_price_entry.delete(0, tk.END)


def medicine_selected(event=None):
    selected = medicines_table.selection()
    if not selected:
        return
    medicine = store.get_medicine(int(selected[0]))
    medicine_stock_entry.delete(0, tk.END)
    medicine_stock_entry.insert(0, str(medicine["stock_qty"]))
    medicine_price_entry.delete(0, tk.END)
    medicine_price_entry.insert(0, str(medicine["price"]))


medicines_table.bind("<<TreeviewSelect>>", medicine_selected)


def medicine_save_clicked():
    selected = medicines_table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a medicine to update.")
        return

    try:
        stock_qty = int(medicine_stock_entry.get())
        price = float(medicine_price_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid input", "Stock qty must be a whole number and price a number.")
        return

    if stock_qty < 0 or price < 0:
        messagebox.showwarning("Invalid input", "Stock qty and price cannot be negative.")
        return

    store.update_medicine(int(selected[0]), stock_qty, price)
    messagebox.showinfo("Updated", "Medicine updated successfully!")
    load_medicines_management()


medicines_button_row = tk.Frame(medicines_card, bg=CARD_COLOR)
medicines_button_row.grid(row=4, column=0, columnspan=2, pady=(20, 0))

tk.Button(medicines_button_row, text="◀ Back to Dashboard",
          command=lambda: [load_dashboard(), show_frame(dashboard_frame)],
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(medicines_button_row, text="Save Changes", command=medicine_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME 9: MANAGE VETS
# =========================================================
vets_frame = tk.Frame(window, bg=BG_COLOR)

vets_card = tk.Frame(vets_frame, bg=CARD_COLOR, padx=30, pady=25)
vets_card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(vets_card, text="🩺 Manage Vets", bg=CARD_COLOR,
         fg=PRIMARY_COLOR, font=("Segoe UI", 20, "bold")
         ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

vets_columns = ("name", "specialty")
vets_table = ttk.Treeview(vets_card, columns=vets_columns, show="headings", height=10)
vets_table.heading("name", text="Name")
vets_table.heading("specialty", text="Specialty")
vets_table.column("name", width=220)
vets_table.column("specialty", width=200)
vets_table.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

tk.Label(vets_card, text="Name:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=2, column=0, padx=10, pady=8, sticky="w")
vet_name_entry = tk.Entry(vets_card, width=30, font=FONT_NORMAL)
vet_name_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")

tk.Label(vets_card, text="Specialty:", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=FONT_NORMAL).grid(row=3, column=0, padx=10, pady=8, sticky="w")
vet_specialty_entry = tk.Entry(vets_card, width=30, font=FONT_NORMAL)
vet_specialty_entry.grid(row=3, column=1, padx=10, pady=8, sticky="w")


def load_vets_management():
    for row in vets_table.get_children():
        vets_table.delete(row)
    for v in store.get_all_vets():
        vets_table.insert("", "end", iid=str(v["id"]), values=(v["name"], v["specialty"]))
    vet_name_entry.delete(0, tk.END)
    vet_specialty_entry.delete(0, tk.END)


def vet_row_selected(event=None):
    selected = vets_table.selection()
    if not selected:
        return
    vet = store.get_vet(int(selected[0]))
    vet_name_entry.delete(0, tk.END)
    vet_name_entry.insert(0, vet["name"])
    vet_specialty_entry.delete(0, tk.END)
    vet_specialty_entry.insert(0, vet["specialty"] or "")


vets_table.bind("<<TreeviewSelect>>", vet_row_selected)


def vet_save_clicked():
    selected = vets_table.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a vet to update.")
        return

    name = vet_name_entry.get().strip()
    specialty = vet_specialty_entry.get().strip()

    if name == "":
        messagebox.showwarning("Missing info", "Name cannot be empty.")
        return

    store.update_vet(int(selected[0]), name, specialty)
    messagebox.showinfo("Updated", "Vet updated successfully!")
    load_vets_management()
    # Refresh the vet dropdowns elsewhere so the new name shows up immediately
    load_vets_into_dropdown()


vets_button_row = tk.Frame(vets_card, bg=CARD_COLOR)
vets_button_row.grid(row=4, column=0, columnspan=2, pady=(20, 0))

tk.Button(vets_button_row, text="◀ Back to Dashboard",
          command=lambda: [load_dashboard(), show_frame(dashboard_frame)],
          bg=TEXT_COLOR, fg="white", font=FONT_BOLD, padx=15, pady=10, bd=0
          ).pack(side="left", padx=(0, 10))

tk.Button(vets_button_row, text="Save Changes", command=vet_save_clicked,
          bg=PRIMARY_COLOR, fg="white", font=FONT_BOLD, padx=20, pady=10, bd=0
          ).pack(side="left")


# =========================================================
# FRAME SWITCHING
# =========================================================
def show_frame(frame):
    frame.tkraise()


login_frame.place(x=0, y=0, relwidth=1, relheight=1)
reception_frame.place(x=0, y=0, relwidth=1, relheight=1)
consultation_frame.place(x=0, y=0, relwidth=1, relheight=1)
diagnostics_frame.place(x=0, y=0, relwidth=1, relheight=1)
treatment_frame.place(x=0, y=0, relwidth=1, relheight=1)
billing_frame.place(x=0, y=0, relwidth=1, relheight=1)
dashboard_frame.place(x=0, y=0, relwidth=1, relheight=1)
edit_visit_frame.place(x=0, y=0, relwidth=1, relheight=1)
medicines_frame.place(x=0, y=0, relwidth=1, relheight=1)
vets_frame.place(x=0, y=0, relwidth=1, relheight=1)

show_frame(login_frame)

window.mainloop()