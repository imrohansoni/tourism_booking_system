from flask import Blueprint
from controllers.tour_controllers import render_tours, render_tours_details


tour_bp = Blueprint("tours", __name__)


@tour_bp.get("/")
def get_tours_route():
    return render_tours()


@tour_bp.get("/<string:tour_slug>")
def get_tour_details(tour_slug):
    return render_tours_details(tour_slug)
