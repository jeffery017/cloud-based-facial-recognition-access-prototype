import face_recognition
import numpy as np
import pickle
import sqlite3



def register_user(file_path):
    try:
        user_image = face_recognition.load_image_file(file_path)
        user_encoding = face_recognition.face_encodings(user_image)[0]
        return user_encoding
    except:
        return None

def validate_user(registered_users, unknown_encoding):
    result = any(face_recognition.compare_faces(registered_users, unknown_encoding, tolerance=0.5))
    print(result)
    return result

