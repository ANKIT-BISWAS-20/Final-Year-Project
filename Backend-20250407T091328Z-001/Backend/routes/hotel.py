from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from models.hotel import HotelUser, HotelDetails

router = APIRouter(prefix="/hotel", tags=["Hotel"])

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AddHotelRequest(BaseModel):
    user_id: str
    name: str
    location: str
    owner: str
    contact: str
    rooms_available: int
    price_per_night: float

# Register endpoint
@router.post("/register")
async def register(data: RegisterRequest):
    response, status_code = HotelUser.register(data.username, data.email, data.password)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("error", "Registration failed"))
    return response

# Login endpoint
@router.post("/login")
async def login(data: LoginRequest):
    response, status_code = HotelUser.login(data.username, data.password)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("error", "Login failed"))
    return response

# Add hotel details
@router.post("/add_hotel")
async def add_hotel(data: AddHotelRequest):
    response, status_code = HotelDetails.add_hotel(
        data.user_id, data.name, data.location, data.owner,
        data.contact, data.rooms_available, data.price_per_night
    )
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("error", "Could not add hotel"))
    return response

# Get hotels by user
@router.get("/hotels/{user_id}")
async def get_hotels_by_user(user_id: str):
    response, status_code = HotelDetails.get_hotels_by_user(user_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("error", "Could not fetch hotels"))
    return response







# from flask import Blueprint, request, jsonify
# from models.hotel import HotelUser, HotelDetails

# hotel_bp = Blueprint("hotel", __name__, url_prefix="/hotel")

# # Register endpoint
# @hotel_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")

#     if not username or not email or not password:
#         return jsonify({"error": "Username, email, and password are required"}), 400

#     response, status_code = HotelUser.register(username, email, password)
#     return jsonify(response), status_code

# # Login endpoint
# @hotel_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password are required"}), 400

#     response, status_code = HotelUser.login(username, password)
#     return jsonify(response), status_code

# # Add hotel details (linked with user)
# @hotel_bp.route("/add_hotel", methods=["POST"])
# def add_hotel():
#     data = request.json
#     user_id = data.get("user_id")  # Required to link with a user
#     name = data.get("name")
#     location = data.get("location")
#     owner = data.get("owner")
#     contact = data.get("contact")
#     rooms_available = data.get("rooms_available")
#     price_per_night = data.get("price_per_night")

#     if not all([user_id, name, location, owner, contact, rooms_available, price_per_night]):
#         return jsonify({"error": "All hotel details and user_id are required"}), 400

#     response, status_code = HotelDetails.add_hotel(user_id, name, location, owner, contact, rooms_available, price_per_night)
#     return jsonify(response), status_code

# # Get hotels by user
# @hotel_bp.route("/hotels/<user_id>", methods=["GET"])
# def get_hotels_by_user(user_id):
#     response, status_code = HotelDetails.get_hotels_by_user(user_id)
#     return jsonify(response), status_code
