


import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, StringVar, OptionMenu
import mysql.connector
from datetime import datetime, timedelta

# Establish database connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # replace with your MySQL username
        password="123456789",    # replace with your MySQL password
        database="healthcare_db"     # replace with your database name
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print("Error: ", err)
    exit(1)

# Function to generate 20-minute time slots with :00 seconds
def generate_time_slots():
    start_time = datetime.strptime("09:00:00", "%H:%M:%S")
    end_time = datetime.strptime("17:00:00", "%H:%M:%S")
    slots = []
    while start_time < end_time:
        slots.append(start_time.strftime("%H:%M:00"))  # Append ":00" to each time slot
        start_time += timedelta(minutes=20)
    return slots

# Function to check available slots for a specific date
def get_available_slots(selected_date):
    all_slots = generate_time_slots()
    cursor.execute("SELECT appointment_time FROM appointments WHERE appointment_date = %s", (selected_date,))
    booked_slots = [str(time[0]) if len(str(time[0])) == 8 else str(time[0]) + ":00" for time in cursor.fetchall()]
    return [slot for slot in all_slots if slot not in booked_slots]


# Function to submit appointment data
def submit_appointment():
    name = entry_name.get()
    date = entry_date.get()
    time = selected_time.get()

    if not name or not date or not time:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        # Ensure time has seconds in ":00" format
        if len(time) == 5:
            time += ":00"

        # Insert the appointment details into the database
        query = "INSERT INTO appointments (name, appointment_date, appointment_time) VALUES (%s, %s, %s)"
        values = (name, date, time)
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Appointment booked successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        entry_name.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        selected_time.set("")

# Function to update available slots when a date is selected
def update_slots():
    selected_date = entry_date.get()
    if selected_date:
        available_slots = get_available_slots(selected_date)
        selected_time.set("")
        time_menu['menu'].delete(0, 'end')
        for slot in available_slots:
            time_menu['menu'].add_command(label=slot, command=tk._setit(selected_time, slot))

# Set up the Tkinter GUI
root = tk.Tk()
root.geometry("400x400")
root.title("Doctor Appointment Booking")

# Labels and Entry widgets for name and date
Label(root, text="Patient Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
entry_name = Entry(root, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Appointment Date (YYYY-MM-DD)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
entry_date = Entry(root, font=("Arial", 12))
entry_date.grid(row=1, column=1, padx=10, pady=10)

# Dropdown for available time slots
Label(root, text="Available Time Slots", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
selected_time = StringVar(root)
time_menu = OptionMenu(root, selected_time, "")
time_menu.config(width=20)
time_menu.grid(row=2, column=1, padx=10, pady=10)

# Button to update available slots
Button(root, text="Check Available Slots", font=("Arial", 12), command=update_slots).grid(row=3, column=0, columnspan=2, pady=10)

# Submit button
Button(root, text="Book Appointment", font=("Arial", 12), command=submit_appointment).grid(row=4, column=0, columnspan=2, pady=20)

# Start Tkinter main loop
root.mainloop()

# Close database connection on exit
conn.close()
