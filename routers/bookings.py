from controllers.booking_controllers import cancel_booking, create_booking, render_bookings
from flask import Blueprint

booking_bp = Blueprint("bookings", __name__)


@booking_bp.post("/")
def create_booking_route():
    return create_booking()


@booking_bp.get("/")
def get_bookings_route():
    return render_bookings()


@booking_bp.get("/<int:booking_id>/cancel")
def cancel_booking_route(booking_id):
    return cancel_booking(booking_id)
