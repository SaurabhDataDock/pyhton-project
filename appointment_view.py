import tkinter as tk
from tkinter import Label, Entry, Button, Canvas, messagebox, ttk

class AppointmentView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.title("Doctor Appointment Booking")

        # User details
        Label(self.root, text="Name:").pack(pady=5)
        self.entry_name = Entry(self.root)
        self.entry_name.pack(pady=5)

        Label(self.root, text="Phone Number:").pack(pady=5)
        self.entry_phone = Entry(self.root)
        self.entry_phone.pack(pady=5)

        # Date selection
        Label(self.root, text="Select Appointment Date").pack(pady=5)
        self.date_var = tk.StringVar(value=self.controller.generate_dates()[0])
        self.date_dropdown = ttk.Combobox(self.root, textvariable=self.date_var, values=self.controller.generate_dates())
        self.date_dropdown.pack(pady=5)

        # Show slots button
        Button(self.root, text="Show Available Slots", command=self.controller.display_slots).pack(pady=10)

        # Canvas for slots
        self.canvas = Canvas(self.root, width=400, height=300, bg="lightgrey")
        self.canvas.pack()

        # Selected slot
        self.selected_slot = tk.StringVar()
        Label(self.root, text="Selected Slot:").pack(pady=5)
        self.entry_slot = Entry(self.root, textvariable=self.selected_slot, state="readonly")
        self.entry_slot.pack(pady=5)

        # Book appointment button
        Button(self.root, text="Book Appointment", command=self.controller.book_appointment).pack(pady=10)

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_exit)
        self.root.mainloop()
