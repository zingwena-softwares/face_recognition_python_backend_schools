import asyncio
import io
import json
import os
import MySQLdb
import cv2
import face_recognition
import numpy as np
import websockets
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
def recognize_face(message):
    try:
        unknown_picture = face_recognition.load_image_file(io.BytesIO(message))
        rgb_small_frame = numpy.ascontiguousarray(unknown_picture[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_small_frame)
        unknown_face_encodings = face_recognition.face_encodings(unknown_picture, face_locations)
        if len(unknown_face_encodings) < 0:
            return {"status": True, "message": "No Face Detected", "data": 0}
        else:
            for face_encoding in unknown_face_encodings:
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(encodeListKnown, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = classNames[best_match_index]
                    return {"status": True, "message": "Hi " + name, "data": 2}
                else:
                    return {"status": True, "message": "Recognition unsuccessful", "data": 1}

    # if len(unknown_face_encodings) > 0:
    #     unknown_face_encoding = unknown_face_encodings[0]
    # else:
    #     return {"status": True, "message": "No Face Detected", "data": 0}
    # results = face_recognition.compare_faces(encodeListKnown, unknown_face_encoding, tolerance=0.5)
    # name = ""
    # face_distance = face_recognition.face_distance(encodeListKnown, unknown_face_encoding)
    # best_match_index = np.argmin(face_distance)
    # if results[0]:
    #     name = classNames[best_match_index]
    #
    # else:
    #     return {"status": True, "message": "Recognition unsuccessful", "data": 1}

    except Exception as e:
        return {"status": False, "message": str(e)}

