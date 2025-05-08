import os
import pickle
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import shutil

# Load saved face embeddings
with open("face_embeddings.pkl", "rb") as f:
    embedding_data = pickle.load(f)

router = APIRouter(prefix="/image", tags=["Image Recognition"])

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check file extension
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Recognize person from uploaded image
@router.post("/recognize")
async def recognize_person(image: UploadFile = File(...)):
    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="Invalid file format. Only JPG, JPEG, PNG allowed.")

    filename = image.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Save the file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Get embedding of uploaded image
        test_obj = DeepFace.represent(img_path=filepath, model_name="Facenet", enforce_detection=True)
        if not test_obj:
            raise HTTPException(status_code=400, detail="No face detected")

        test_embedding = np.array(test_obj[0]["embedding"]).reshape(1, -1)

        # Compare with saved embeddings
        best_match = None
        best_score = -1
        threshold = 0.65

        for saved_embedding, saved_name in embedding_data:
            saved_embedding = np.array(saved_embedding).reshape(1, -1)
            score = cosine_similarity(test_embedding, saved_embedding)[0][0]

            if score > best_score:
                best_score = score
                best_match = saved_name

        if best_score >= threshold:
            return {"person": best_match, "confidence": float(best_score)}
        else:
            return {"person": "not in our Criminal Database", "confidence": float(best_score)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







# import os
# import pickle
# import numpy as np
# from flask import Blueprint, request, jsonify
# from deepface import DeepFace
# from sklearn.metrics.pairwise import cosine_similarity
# from werkzeug.utils import secure_filename

# # Load saved face embeddings
# with open("face_embeddings.pkl", "rb") as f:
#     embedding_data = pickle.load(f)

# image_bp = Blueprint("image", __name__, url_prefix="/image")

# UPLOAD_FOLDER = "uploads"  # Directory to save uploaded images
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}  # Allowed file formats

# # Ensure upload directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Helper function: Check allowed file extensions
# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# # Recognize person from uploaded image
# @image_bp.route("/recognize", methods=["POST"])
# def recognize_person():
#     if "image" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["image"]

#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)

#         try:
#             # Get embedding of uploaded image
#             test_obj = DeepFace.represent(img_path=filepath, model_name="Facenet", enforce_detection=True)
#             if not test_obj:
#                 return jsonify({"error": "No face detected"}), 400

#             test_embedding = np.array(test_obj[0]["embedding"]).reshape(1, -1)

#             # Compare with saved embeddings
#             best_match = None
#             best_score = -1
#             threshold = 0.65

#             for saved_embedding, saved_name in embedding_data:
#                 saved_embedding = np.array(saved_embedding).reshape(1, -1)
#                 score = cosine_similarity(test_embedding, saved_embedding)[0][0]

#                 if score > best_score:
#                     best_score = score
#                     best_match = saved_name

#             if best_score >= threshold:
#                 return jsonify({"person": best_match, "confidence": float(best_score)}), 200
#             else:
#                 return jsonify({"person": "not in our Criminal Database", "confidence": float(best_score)}), 200

#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return jsonify({"error": "Invalid file format. Only JPG, JPEG, PNG allowed."}), 400
