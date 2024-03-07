from flask import render_template, g
from database import db
from utils.authentication import authenticate


@authenticate
def get_accommodations():
    cursor = db.cursor()
    user = g.get("user_data")
    cursor.execute(
        "SELECT name, image, location, price, rating, bed, wifi, a_c, restaurant, room_service, house_keeping, map FROM accommodations"
    )

    acc = cursor.fetchall()
    acc_list = []
    for a in acc:
        acc_list.append({
            "name": a[0],
            "image": a[1],
            "location": a[2],
            "price": a[3],
            "rating": a[4],
            "bed": a[5],
            "wifi": a[6],
            "a_c": a[7],
            "restaurant": a[8],
            "room_service": a[9],
            "house_keeping": a[10],
            "map": a[11]
        })

    return render_template("accommodations.html", acc=acc_list, active_link="accommodations", user=user)
