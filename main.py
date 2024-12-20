from models.db_model import Database
from views.appointment_view import AppointmentView
from controllers.appointment_controller import AppointmentController

if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="123456789", database="healthcare_db")
    view = AppointmentView(None)
    controller = AppointmentController(view, db)
    view.controller = controller
    view.start()
