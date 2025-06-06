from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId  # Import ObjectId for MongoDB IDs

# MongoDB connection
MONGO_URI = "MONGODB_URI_PLEASE"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client.get_database("hotel_db")  # Database name
users_collection = db.get_collection("users")  # Collection for users
hotel_collection = db.get_collection("hotel_details")  # Collection for hotels

# HotelUser Model
class HotelUser:
    @staticmethod
    def register(username, email, password):
        if users_collection.find_one({"username": username}):
            return {"error": "User already exists"}, 409

        hashed_password = generate_password_hash(password)
        user_id = users_collection.insert_one(
            {"username": username, "email": email, "password": hashed_password}
        ).inserted_id

        return {"message": "User registered successfully", "user_id": str(user_id)}, 201

    @staticmethod
    def login(username, password):
        user = users_collection.find_one({"username": username})
        if not user or not check_password_hash(user["password"], password):
            return {"error": "Invalid username or password"}, 401

        return {"message": "Login successful", "user_id": str(user["_id"])}, 200


# HotelDetails Model
class HotelDetails:
    @staticmethod
    def add_hotel(user_id, name, location, owner, contact, rooms_available, price_per_night):
        # Validate user existence
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"error": "Invalid user ID"}, 400

        hotel_data = {
            "user_id": ObjectId(user_id),  # Store user_id as an ObjectId
            "name": name,
            "location": location,
            "owner": owner,
            "contact": contact,
            "rooms_available": rooms_available,
            "price_per_night": price_per_night
        }
        hotel_collection.insert_one(hotel_data)
        return {"message": "Hotel added successfully"}, 201

# HotelDetails Model
class HotelDetails:
    @staticmethod
    def get_hotels_by_user(user_id):
        # Validate user existence
        try:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return {"error": "Invalid user ID"}, 400
        except:
            return {"error": "Invalid ObjectId format"}, 400

        # Fetch hotels linked to user_id
        hotels = list(hotel_collection.find({"user_id": ObjectId(user_id)}))

        # Convert ObjectId to string in the response
        for hotel in hotels:
            hotel["_id"] = str(hotel["_id"])  # Convert hotel ID
            hotel["user_id"] = str(hotel["user_id"])  # Convert user ID

        return {"hotels": hotels}, 200
