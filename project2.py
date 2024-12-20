import tkinter as tk
from tkinter import Label, Entry, Button, Canvas, messagebox
from datetime import datetime, timedelta
import mysql.connector

# Connect to database (replace with your actual database credentials)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="healthcare_db"
)
cursor = conn.cursor()


# Function to generate time slots
def generate_time_slots():
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    slots = []
    while start_time < end_time:
        slots.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=20)
    return slots


# Function to get available slots for a specific date
def get_available_slots(selected_date):
    all_slots = generate_time_slots()
    cursor.execute("SELECT appointment_time FROM appointments WHERE appointment_date = %s", (selected_date,))

    # Convert each fetched time to a string and format as "HH:MM"
    booked_slots = [str(time[0])[:5] for time in cursor.fetchall()]  # Strip seconds by slicing
    return {"available": [slot for slot in all_slots if slot not in booked_slots],
            "booked": booked_slots}



# Function to display time slots in calendar format
def display_slots():
    date = entry_date.get()
    slots = get_available_slots(date)

    canvas.delete("all")  # Clear previous slots

    x, y = 10, 10
    for i, slot in enumerate(generate_time_slots()):
        color = "yellow" if slot in slots["available"] else "green"
        canvas.create_rectangle(x, y, x + 60, y + 30, fill=color, tags="slot")
        canvas.create_text(x + 30, y + 15, text=slot, fill="black")
        y += 40
        if (i + 1) % 4 == 0:
            x += 80
            y = 10


# Set up the Tkinter GUI
root = tk.Tk()
root.geometry("500x400")
root.title("Doctor Appointment Booking")

# Date entry and label
Label(root, text="Appointment Date (YYYY-MM-DD)").pack(pady=5)
entry_date = Entry(root)
entry_date.pack(pady=5)

# Button to load and display available/booked slots
Button(root, text="Show Available Slots", command=display_slots).pack(pady=10)

# Canvas to display colored slots
canvas = Canvas(root, width=400, height=300, bg="lightgrey")
canvas.pack()

root.mainloop()

# Close the database connection when done
conn.close()
