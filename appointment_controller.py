from datetime import datetime, timedelta
from tkinter import messagebox

class AppointmentController:
    def __init__(self, view, db):
        self.view = view
        self.db = db

    def generate_dates(self):
        today = datetime.today()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    def generate_time_slots(self):
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("17:00", "%H:%M")
        slots = []
        while start_time < end_time:
            slots.append(start_time.strftime("%H:%M"))
            start_time += timedelta(minutes=20)
        return slots

    def display_slots(self):
        selected_date = self.view.date_var.get()
        all_slots = self.generate_time_slots()
        booked_slots = self.db.fetch_appointments(selected_date)
        available_slots = [slot for slot in all_slots if slot not in booked_slots]

        canvas = self.view.canvas
        canvas.delete("all")

        x, y = 10, 10
        for i, slot in enumerate(all_slots):
            color = "yellow" if slot in available_slots else "green"
            rect = canvas.create_rectangle(x, y, x + 60, y + 30, fill=color, tags="slot")
            text = canvas.create_text(x + 30, y + 15, text=slot, fill="black")

            if slot in available_slots:
                canvas.tag_bind(rect, "<Button-1>", lambda e, s=slot: self.select_slot(s))
                canvas.tag_bind(text, "<Button-1>", lambda e, s=slot: self.select_slot(s))

            y += 40
            if (i + 1) % 4 == 0:
                x += 80
                y = 10

    def select_slot(self, slot):
        self.view.selected_slot.set(slot)
        messagebox.showinfo("Slot Selected", f"You have selected {slot}.")

    def book_appointment(self):
        name = self.view.entry_name.get()
        phone = self.view.entry_phone.get()
        date = self.view.date_var.get()
        time = self.view.selected_slot.get()

        if not name or not phone or not date or not time:
            messagebox.showwarning("Incomplete Data", "Please fill in all fields and select a time slot.")
            return

        try:
            self.db.book_appointment(name, phone, date, time)
            messagebox.showinfo("Success", f"Appointment booked for {name} on {date} at {time}.")
            self.display_slots()
        except Exception as e:
            messagebox.showerror("Error", f"Error booking appointment: {e}")

    def on_exit(self):
        self.db.close()
        self.view.root.destroy()
