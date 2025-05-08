from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from routes.hotel import router as hotel_router  # Assuming FastAPI router
from routes.image import router as image_router  # Assuming FastAPI router

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Register routers (equivalent to blueprints)
app.include_router(hotel_router, prefix="/hotel")
app.include_router(image_router, prefix="/image")

# Root endpoint
@app.get("/")
async def home():
    return {"message": "HOME API is running!"}

# Error handler for 404 Not Found
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Endpoint not found"})

# Error handler for 500 Internal Server Error
@app.exception_handler(500)
async def server_error(request: Request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Run the app
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)




# from flask import Flask
# from flask_cors import CORS
# import logging
# from routes.hotel import hotel_bp  # Import hotel blueprint
# from routes.image import image_bp  # Import image recognition blueprint

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all routes

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Register Blueprints
# app.register_blueprint(hotel_bp)  # Register the hotel blueprint
# app.register_blueprint(image_bp)  # Register the image recognition blueprint

# @app.route("/")
# def home():
#     return "HOME API is running!"

# # Error handling for 404 - Not Found
# @app.errorhandler(404)
# def not_found(error):
#     return {"error": "Endpoint not found"}, 404

# # Error handling for 500 - Internal Server Error
# @app.errorhandler(500)
# def server_error(error):
#     return {"error": "Internal server error"}, 500

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 5000))  # Use environment PORT or default to 5000
#     app.run(host="0.0.0.0", port=port, debug=True)
