import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import pywhatkit
import datetime
import time

# ---------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Preeti@25",  # change this if needed
        database="birthdaydb"
    )

# ---------- ADD NEW BIRTHDAY ----------
def add_birthday():
    name = name_entry.get()
    phone = phone_entry.get()
    birthdate = date_entry.get()

    if not (name and phone and birthdate):
        messagebox.showwarning("Warning", "All fields are required!")
        return

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO birthdays (name, phone, birthdate) VALUES (%s, %s, %s)", (name, phone, birthdate))
        db.commit()
        db.close()
        messagebox.showinfo("Success", f"Added {name}'s birthday!")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        show_birthdays()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- DISPLAY ALL BIRTHDAYS ----------
def show_birthdays():
    for row in tree.get_children():
        tree.delete(row)

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM birthdays")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    db.close()

# ---------- SEND WHATSAPP MESSAGE ----------
def send_wishes():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM birthdays WHERE DATE_FORMAT(birthdate, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d')")
    birthdays_today = cursor.fetchall()
    db.close()

    if not birthdays_today:
        messagebox.showinfo("No Birthdays", "No birthdays today!")
        return

    for person in birthdays_today:
        name = person['name']
        phone = person['phone']
        message = f"🎉 जन्मदिनस्य हार्दिकाः शुभकामनाः {name}! 🎂🎈\nWishing you a wonderful year ahead!"
        now = datetime.datetime.now()
        pywhatkit.sendwhatmsg(phone, message, now.hour, now.minute + 2)
        time.sleep(10)

    messagebox.showinfo("Done", "Birthday wishes sent successfully!")

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("🎂 WishMitram - Your Smart Birthday Wisher")
root.geometry("700x520")
root.resizable(False, False)

# Title Section
tk.Label(
    root,
    text="🤖 WishMitram",
    font=("Arial", 22, "bold"),
    fg="#0052cc"
).pack(pady=10)

tk.Label(
    root,
    text="Your Smart Birthday Wisher (स्मार्ट जन्मदिन शुभेच्छक मित्र)",
    font=("Arial", 11, "italic"),
    fg="#444"
).pack(pady=2)

# Input fields
frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Phone (+91...):").grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(frame, width=25)
phone_entry.grid(row=1, column=1)

tk.Label(frame, text="Birthdate (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame, width=25)
date_entry.grid(row=2, column=1)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Add Birthday", command=add_birthday, bg="#9ef59e").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="📋 Show All", command=show_birthdays, bg="#a4d8ff").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="📨 Send Wishes", command=send_wishes, bg="#ffd27f").grid(row=0, column=2, padx=10)

# Birthday List
columns = ("ID", "Name", "Phone", "Birthdate")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

show_birthdays()

# Footer
tk.Label(
    root,
    text="Developed with ❤️ by Preeti | WishMitram 2025",
    font=("Arial", 9, "italic"),
    fg="gray"
).pack(pady=5)

root.mainloop()