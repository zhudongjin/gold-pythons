from flask import Blueprint
mf = Blueprint("mf", __name__, template_folder="mf", url_prefix="/mf")
from . import views