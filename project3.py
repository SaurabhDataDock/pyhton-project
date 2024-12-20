import tkinter as tk
from tkinter import Label, Entry, Button, Canvas, messagebox, ttk
from datetime import datetime, timedelta
import mysql.connector

# Connect to database (replace with your actual database credentials)
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="healthcare_db"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")


# Function to generate time slots
def generate_time_slots():
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    slots = []
    while start_time < end_time:
        slots.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=20)
    return slots


# Generate a list of dates for the dropdown (next 30 days)
def generate_dates():
    today = datetime.today()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]


# Function to get available slots for a specific date
def get_available_slots(selected_date):
    all_slots = generate_time_slots()
    cursor.execute("SELECT appointment_time FROM appointments WHERE appointment_date = %s", (selected_date,))

    # Convert each fetched time to a string and format as "HH:MM"
    booked_slots = [str(time[0])[:5] for time in cursor.fetchall()]  # Strip seconds by slicing
    return {"available": [slot for slot in all_slots if slot not in booked_slots],
            "booked": booked_slots}


# Function to display time slots in calendar format with selection
def display_slots():
    selected_date = date_var.get()
    slots = get_available_slots(selected_date)

    canvas.delete("all")  # Clear previous slots

    x, y = 10, 10
    for i, slot in enumerate(generate_time_slots()):
        color = "yellow" if slot in slots["available"] else "green"
        rect = canvas.create_rectangle(x, y, x + 60, y + 30, fill=color, tags="slot")
        text = canvas.create_text(x + 30, y + 15, text=slot, fill="black")

        # If the slot is available, make it clickable
        if slot in slots["available"]:
            canvas.tag_bind(rect, "<Button-1>", lambda e, s=slot: select_slot(s))
            canvas.tag_bind(text, "<Button-1>", lambda e, s=slot: select_slot(s))

        y += 40
        if (i + 1) % 4 == 0:
            x += 80
            y = 10


# Function to handle slot selection
def select_slot(slot):
    selected_slot.set(slot)
    messagebox.showinfo("Slot Selected", f"You have selected {slot}.")


# Function to book the appointment
def book_appointment():
    name = entry_name.get()
    phone = entry_phone.get()
    date = date_var.get()
    time = selected_slot.get()

    if not name or not phone or not date or not time:
        messagebox.showwarning("Incomplete Data", "Please fill in all fields and select a time slot.")
        return

    try:
        cursor.execute(
            "INSERT INTO appointments (patient_name, patient_phone, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)",
            (name, phone, date, time))
        conn.commit()
        messagebox.showinfo("Success", f"Appointment successfully booked for {name} on {date} at {time}.")
        display_slots()  # Refresh slots
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error booking appointment: {err}")


# Set up the Tkinter GUI
root = tk.Tk()
root.geometry("600x500")
root.title("Doctor Appointment Booking")

# User details section
Label(root, text="Name:").pack(pady=5)
entry_name = Entry(root)
entry_name.pack(pady=5)

Label(root, text="Phone Number:").pack(pady=5)
entry_phone = Entry(root)
entry_phone.pack(pady=5)

# Date selection
Label(root, text="Select Appointment Date").pack(pady=5)
date_var = tk.StringVar(value=generate_dates()[0])
date_dropdown = ttk.Combobox(root, textvariable=date_var, values=generate_dates())
date_dropdown.pack(pady=5)

# Button to load and display available/booked slots
Button(root, text="Show Available Slots", command=display_slots).pack(pady=10)

# Canvas to display colored slots
canvas = Canvas(root, width=400, height=300, bg="lightgrey")
canvas.pack()

# Selected slot
selected_slot = tk.StringVar()
Label(root, text="Selected Slot:").pack(pady=5)
entry_slot = Entry(root, textvariable=selected_slot, state="readonly")
entry_slot.pack(pady=5)

# Button to confirm and book appointment
Button(root, text="Book Appointment", command=book_appointment).pack(pady=10)

# Close the database connection when the application exits
root.protocol("WM_DELETE_WINDOW", lambda: [conn.close(), root.destroy()])

root.mainloop()

