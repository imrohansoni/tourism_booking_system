from flask import redirect, render_template, request, session, g
from database import db
from utils.authentication import authenticate
import uuid


@authenticate
def create_booking():
    if g.get("user_data") is None:
        return redirect("/login")
    data = request.form
    cursor = db.cursor()

    cursor.execute("SELECT name, image, location, price_per_person, duration, rating FROM tours WHERE id=%s", [
        data["tour_id"]])

    tour = cursor.fetchone()

    total_price = int(data["total_people"]) * int(tour[3])

    transaction_id = str(uuid.uuid4()).replace('-', '')

    cursor.execute(
        "INSERT INTO bookings(user_id,tour_id, total_people, total_price, transaction_id, booking_status) value (%s, %s, %s, %s, %s, 'confirmed')", (data["user_id"], data["tour_id"], data["total_people"], total_price, transaction_id))

    cursor.close()
    db.commit()
    return render_template("/confirmation.html", title="Booking confirmation", booking_details={
        "name": tour[0],
        "image": tour[1],
        "location": tour[2],
        "price_per_person": tour[3],
        "duration": tour[4],
        "rating": tour[5],
        "transaction_id": transaction_id,
        "total_price": total_price,
        "total_people": data["total_people"]
    }, user=g.get("user_data"))


@authenticate
def render_bookings():
    if g.get("user_data") is None:
        return redirect("/login")

    user = g.get("user_data")
    cursor = db.cursor()

    cursor.execute(
        "SELECT tours.image, tours.name, tours.location, tours.duration, bookings.created_at, bookings.total_people, bookings.total_price, bookings.transaction_id, bookings.booking_status, bookings.id FROM tours JOIN bookings ON tours.id = bookings.tour_id WHERE bookings.user_id=%s", [user["id"]])

    bookings = cursor.fetchall()
    cursor.close()
    booking_list = []

    for booking in bookings:
        formatted_date = booking[4].strftime("%I:%M %p %d %b %Y")

        booking_list.append({
            "image": booking[0],
            "name": booking[1],
            "location": booking[2],
            "duration": booking[3],
            "created_at": formatted_date,
            "total_people": booking[5],
            "total_price": booking[6],
            "transaction_id": booking[7],
            "booking_status": booking[8],
            "id": booking[9]
        })

    return render_template("bookings.html", user=user, bookings=booking_list)


@authenticate
def cancel_booking(booking_id):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE bookings SET booking_status = 'cancelled' WHERE id =%s", [booking_id])
    cursor.close()
    return redirect("/bookings")
