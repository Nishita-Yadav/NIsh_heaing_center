import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nishita179",
        database="Nish_healing_center"
    )
    return con

def show_patients():
    for item in tree_patient.get_children():
        tree_patient.delete(item)
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT c.customer_id, c.name, c.age, c.gender, c.phone, c.days, h.name FROM Customer c LEFT JOIN Healer h ON c.healer_id = h.healer_id")
        rows = cur.fetchall()
        for r in rows:
            tree_patient.insert("", tk.END, values=r)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def check_bill():
    selected = tree_patient.focus()
    if selected == "":
        messagebox.showwarning("Warning", "Select a patient first!")
        return

    values = tree_patient.item(selected, "values")
    pid = values[0]

    try:
        con = connect_db()
        cur = con.cursor()
        query = """
            SELECT c.customer_id, c.name, c.age, c.gender, c.phone, c.days,
                   h.name, h.specialty, h.fee,
                   p.name, p.dosage, p.price,
                   a.test_name, a.cost,
                   s.meal_name, s.price
            FROM Customer c
            JOIN Healer h ON c.healer_id = h.healer_id
            JOIN Potion p ON c.potion_id = p.potion_id
            JOIN Analysis a ON c.analysis_id = a.analysis_id
            JOIN Supper s ON c.supper_id = s.supper_id
            WHERE c.customer_id = %s
        """
        cur.execute(query, (pid,))
        row = cur.fetchone()
        con.close()

        room_charge = row[5] * 500
        food_charge = row[15] * row[5]
        total = room_charge + row[8] + row[11] + row[13] + food_charge

        bill = "------------------------------------------\n"
        bill += "          NISH HEALING CENTER\n"
        bill += "------------------------------------------\n"
        bill += "Patient ID   : " + str(row[0]) + "\n"
        bill += "Name         : " + row[1] + "\n"
        bill += "Age / Gender : " + str(row[2]) + " / " + row[3] + "\n"
        bill += "Phone        : " + row[4] + "\n"
        bill += "Days Admitted: " + str(row[5]) + "\n"
        bill += "------------------------------------------\n"
        bill += "Room Charge  : Rs. " + str(room_charge) + "\n"
        bill += "Doctor       : " + row[6] + " (Rs. " + str(row[8]) + ")\n"
        bill += "Medicine     : " + row[9] + " (Rs. " + str(row[11]) + ")\n"
        bill += "Analysis     : " + row[12] + " (Rs. " + str(row[13]) + ")\n"
        bill += "Supper       : " + row[14] + " (Rs. " + str(food_charge) + ")\n"
        bill += "------------------------------------------\n"
        bill += "TOTAL BILL   : Rs. " + str(total) + "\n"
        bill += "------------------------------------------\n"

        bill_box.delete("1.0", tk.END)
        bill_box.insert(tk.END, bill)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fill_dropdowns():
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT healer_id, name FROM Healer")
        h_list = []
        for r in cur.fetchall():
            h_list.append(str(r[0]) + " - " + r[1])
        combo_healer["values"] = h_list

        cur.execute("SELECT potion_id, name FROM Potion")
        p_list = []
        for r in cur.fetchall():
            p_list.append(str(r[0]) + " - " + r[1])
        combo_potion["values"] = p_list

        cur.execute("SELECT analysis_id, test_name FROM Analysis")
        a_list = []
        for r in cur.fetchall():
            a_list.append(str(r[0]) + " - " + r[1])
        combo_analysis["values"] = a_list

        cur.execute("SELECT supper_id, meal_name FROM Supper")
        s_list = []
        for r in cur.fetchall():
            s_list.append(str(r[0]) + " - " + r[1])
        combo_supper["values"] = s_list

        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    phone = entry_phone.get()
    days = entry_days.get()
    h = combo_healer.get()
    p = combo_potion.get()
    a = combo_analysis.get()
    s = combo_supper.get()

    if name == "" or age == "" or gender == "" or phone == "" or days == "" or h == "" or p == "" or a == "" or s == "":
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    try:
        hid = int(h.split(" - ")[0])
        pid = int(p.split(" - ")[0])
        aid = int(a.split(" - ")[0])
        sid = int(s.split(" - ")[0])

        con = connect_db()
        cur = con.cursor()
        sql = "INSERT INTO Customer (name, age, gender, phone, days, healer_id, potion_id, analysis_id, supper_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (name, int(age), gender, phone, int(days), hid, pid, aid, sid))
        con.commit()
        con.close()

        messagebox.showinfo("Done", "New patient added!")
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_days.delete(0, tk.END)
        show_patients()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_other_lists():
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM Healer")
        for r in cur.fetchall():
            tree_doctor.insert("", tk.END, values=r)

        cur.execute("SELECT * FROM Analysis")
        for r in cur.fetchall():
            tree_analysis.insert("", tk.END, values=r)

        cur.execute("SELECT * FROM Potion")
        for r in cur.fetchall():
            tree_potion.insert("", tk.END, values=r)

        cur.execute("SELECT * FROM Supper")
        for r in cur.fetchall():
            tree_supper.insert("", tk.END, values=r)

        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

win = tk.Tk()
win.title("Nish Healing Center")
win.geometry("1000x580")
win.configure(bg="#e0f2f1")

top_label = tk.Label(win, text="NISH HEALING CENTER - HOSPITAL BILL SYSTEM", bg="#00695c", fg="white", font=("Arial", 15, "bold"), pady=12)
top_label.pack(fill=tk.X)

tabs = ttk.Notebook(win)
tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tab1 = tk.Frame(tabs, bg="#f0f9f8")
tab2 = tk.Frame(tabs, bg="#f0f9f8")
tab3 = tk.Frame(tabs, bg="#f0f9f8")
tab4 = tk.Frame(tabs, bg="#f0f9f8")

tabs.add(tab1, text="Patients & Bill")
tabs.add(tab2, text="Add Patient")
tabs.add(tab3, text="Doctors List")
tabs.add(tab4, text="Analysis & Others")

# Tab 1
f_left = tk.Frame(tab1, bg="#f0f9f8")
f_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(f_left, text="Existing Patients List", bg="#f0f9f8", font=("Arial", 11, "bold")).pack(anchor="w")

tree_patient = ttk.Treeview(f_left, columns=("ID", "Name", "Age", "Gender", "Phone", "Days", "Doctor"), show="headings", height=15)
tree_patient.heading("ID", text="ID")
tree_patient.heading("Name", text="Name")
tree_patient.heading("Age", text="Age")
tree_patient.heading("Gender", text="Gender")
tree_patient.heading("Phone", text="Phone")
tree_patient.heading("Days", text="Days")
tree_patient.heading("Doctor", text="Doctor")

tree_patient.column("ID", width=40)
tree_patient.column("Name", width=110)
tree_patient.column("Age", width=40)
tree_patient.column("Gender", width=65)
tree_patient.column("Phone", width=95)
tree_patient.column("Days", width=45)
tree_patient.column("Doctor", width=120)
tree_patient.pack(fill=tk.BOTH, expand=True, pady=5)

tk.Button(f_left, text="Generate Bill", command=check_bill, bg="#00796b", fg="white", font=("Arial", 10, "bold"), padx=12, pady=5).pack(side=tk.LEFT, pady=5)
tk.Button(f_left, text="Refresh", command=show_patients, bg="#b2dfdb", font=("Arial", 10), padx=12, pady=5).pack(side=tk.LEFT, padx=8, pady=5)

f_right = tk.Frame(tab1, bg="#f0f9f8")
f_right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

tk.Label(f_right, text="Patient Bill", bg="#f0f9f8", font=("Arial", 11, "bold")).pack(anchor="w")
bill_box = tk.Text(f_right, width=44, height=22, font=("Courier", 10))
bill_box.pack(pady=5)

# Tab 2
form = tk.Frame(tab2, bg="white", padx=25, pady=20, bd=1, relief="solid")
form.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(form, text="Add New Patient", bg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(form, text="Patient Name:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=4)
entry_name = tk.Entry(form, width=30)
entry_name.grid(row=1, column=1, pady=4)

tk.Label(form, text="Age:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=4)
entry_age = tk.Entry(form, width=30)
entry_age.grid(row=2, column=1, pady=4)

tk.Label(form, text="Gender:", bg="white", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=4)
combo_gender = ttk.Combobox(form, values=["Male", "Female", "Other"], state="readonly", width=27)
combo_gender.grid(row=3, column=1, pady=4)

tk.Label(form, text="Phone:", bg="white", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=4)
entry_phone = tk.Entry(form, width=30)
entry_phone.grid(row=4, column=1, pady=4)

tk.Label(form, text="Days Admitted:", bg="white", font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=4)
entry_days = tk.Entry(form, width=30)
entry_days.grid(row=5, column=1, pady=4)

tk.Label(form, text="Select Healer:", bg="white", font=("Arial", 10)).grid(row=6, column=0, sticky="w", pady=4)
combo_healer = ttk.Combobox(form, state="readonly", width=27)
combo_healer.grid(row=6, column=1, pady=4)

tk.Label(form, text="Select Potion:", bg="white", font=("Arial", 10)).grid(row=7, column=0, sticky="w", pady=4)
combo_potion = ttk.Combobox(form, state="readonly", width=27)
combo_potion.grid(row=7, column=1, pady=4)

tk.Label(form, text="Select Analysis:", bg="white", font=("Arial", 10)).grid(row=8, column=0, sticky="w", pady=4)
combo_analysis = ttk.Combobox(form, state="readonly", width=27)
combo_analysis.grid(row=8, column=1, pady=4)

tk.Label(form, text="Select Supper:", bg="white", font=("Arial", 10)).grid(row=9, column=0, sticky="w", pady=4)
combo_supper = ttk.Combobox(form, state="readonly", width=27)
combo_supper.grid(row=9, column=1, pady=4)

tk.Button(form, text="Save Patient", command=save_patient, bg="#00796b", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5).grid(row=10, column=0, columnspan=2, pady=12)

# Tab 3
tk.Label(tab3, text="Doctors (Healer) List", bg="#f0f9f8", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=8)
tree_doctor = ttk.Treeview(tab3, columns=("ID", "Name", "Specialty", "Fee"), show="headings", height=15)
tree_doctor.heading("ID", text="ID")
tree_doctor.heading("Name", text="Doctor Name")
tree_doctor.heading("Specialty", text="Specialty")
tree_doctor.heading("Fee", text="Fee (Rs)")
tree_doctor.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Tab 4
tk.Label(tab4, text="Analysis List", bg="#f0f9f8", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=4)
tree_analysis = ttk.Treeview(tab4, columns=("ID", "Test", "Details", "Cost"), show="headings", height=5)
tree_analysis.heading("ID", text="ID")
tree_analysis.heading("Test", text="Test Name")
tree_analysis.heading("Details", text="Details")
tree_analysis.heading("Cost", text="Cost (Rs)")
tree_analysis.pack(fill=tk.X, padx=15)

tk.Label(tab4, text="Potion (Medicine) List", bg="#f0f9f8", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=4)
tree_potion = ttk.Treeview(tab4, columns=("ID", "Name", "Dosage", "Price"), show="headings", height=4)
tree_potion.heading("ID", text="ID")
tree_potion.heading("Name", text="Medicine Name")
tree_potion.heading("Dosage", text="Dosage")
tree_potion.heading("Price", text="Price (Rs)")
tree_potion.pack(fill=tk.X, padx=15)

tk.Label(tab4, text="Supper (Food) List", bg="#f0f9f8", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=4)
tree_supper = ttk.Treeview(tab4, columns=("ID", "Meal", "Diet", "Price"), show="headings", height=4)
tree_supper.heading("ID", text="ID")
tree_supper.heading("Meal", text="Meal Name")
tree_supper.heading("Diet", text="Diet Type")
tree_supper.heading("Price", text="Price (Rs)")
tree_supper.pack(fill=tk.X, padx=15)

show_patients()
fill_dropdowns()
show_other_lists()

win.mainloop()