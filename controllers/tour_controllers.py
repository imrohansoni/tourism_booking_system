from flask import render_template, g
from database import db
from utils.authentication import authenticate


@authenticate
def render_tours():
    cursor = db.cursor()
    cursor.execute(
        "SELECT image, name, location, duration, price_per_person, small_description, rating, slug FROM tours")
    tours = cursor.fetchall()
    tour_list = []
    for tour in tours:
        tour_list.append({
            "image": tour[0],
            "name": tour[1],
            "location": tour[2],
            "duration": tour[3],
            "price_per_person": tour[4],
            "small_description": tour[5],
            "rating": tour[6],
            "slug": tour[7]
        })
    cursor.close()
    return render_template("tours.html", user=g.get("user_data"), tours=tour_list)


@authenticate
def render_tours_details(tour_slug):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, image, name, location, duration, price_per_person, small_description, description, rating, slug FROM tours WHERE slug = %s", [tour_slug])
    tour = cursor.fetchone()
    tour_details = ({
        "id": tour[0],
        "image": tour[1],
        "name": tour[2],
        "location": tour[3],
        "duration": tour[4],
        "price_per_person": tour[5],
        "small_description": tour[6],
        "description": tour[7],
        "rating": tour[8],
        "slug": tour[9]
    })
    return render_template("tour-details.html", user=g.get("user_data"), tour=tour_details)
