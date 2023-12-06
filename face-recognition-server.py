import asyncio
import io
import json
import os
import MySQLdb
import cv2
import face_recognition
import numpy as np
import websockets
# from flask import Flask
# from flask_mysqldb import MySQL
from datetime import datetime

# app = Flask(__name__)

images_path = 'images'
images = []
classNames = []
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'hrm'
# app.app_context().push()

# mysql = MySQL(app)

myList = os.listdir(images_path)
for cl in myList:
    curImg = cv2.imread(f'{images_path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


def find_encodings(cimages):
    encode_list = []
    for img in cimages:
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


encodeListKnown = find_encodings(images)
print('Encoding Complete')


async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            response = recognize_face(message)
            await websocket.send(json.dumps(response))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")


def recognize_face(message):
    try:
        unknown_picture = face_recognition.load_image_file(io.BytesIO(message))
        unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
        if len(unknown_face_encodings) > 0:
            unknown_face_encoding = unknown_face_encodings[0]
        else:
            return {"status": True, "message": "No Face Detected", "data": 0}
        results = face_recognition.compare_faces(encodeListKnown, unknown_face_encoding)
        face_distance = face_recognition.face_distance(encodeListKnown, unknown_face_encoding)
        best_match_index = np.argmin(face_distance)
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if results[best_match_index]:
            name = classNames[best_match_index]
            # cursor.execute('INSERT INTO attendances (`company_id`,`user_id`,`date`, `check_in`, `check_out`) VALUES ('
            #                '%s, %s, %s, %s, %s)', (
            #                    1, 2, datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'),
            #                    datetime.today().strftime('%Y-%m-%d')))
            # mysql.connection.commit()
            return {"status": True, "message": "Welcome ," + name, "data": 2}
        else:
            return {"status": True, "message": "Recognition unsuccessful", "data": 1}

    except Exception as e:
        print(e)
        return {"status": False, "message": str(e)}


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        websockets.serve(websocket_handler, "195.35.9.96", 8765)
    )
    loop.run_forever()
