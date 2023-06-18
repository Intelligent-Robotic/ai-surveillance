import face_recognition
import cv2
import numpy as np
import notifier
import io
import logger
import os
import requests


url = 'http://192.168.192.55:5000/video_feed'

folder_path = "./guest_list"


# Check if the folder is empty
if len(os.listdir(folder_path)) == 0:
    print("Folder is empty!")
else:
    # Initialize arrays for the face encodings and names
    known_face_encodings = []
    known_face_names = []

    # Loop through the images in the folder
    for filename in os.listdir(folder_path):
        # Load the image and extract the face encoding
        image_path = os.path.join(folder_path, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]

        # Extract the label from the folder name
        label = os.path.splitext(filename)[0]

        # Add the face encoding and name to the arrays
        known_face_encodings.append(face_encoding)
        known_face_names.append(label)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
notifier_triggered = False

while True:
    stream = requests.get(url, stream=True)
    stream_bytes = bytes()
    for chunk in stream.iter_content(chunk_size=4096):
        stream_bytes += chunk
        a = stream_bytes.find(b'\xff\xd8')
        b = stream_bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = stream_bytes[a:b+2]
            stream_bytes = stream_bytes[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
           

            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    if not any(matches):
                        if not notifier_triggered:
                            
                            for (top, right, bottom, left), name in zip(face_locations, face_names):
                                top *= 4
                                right *= 4
                                bottom *= 4
                                left *= 4
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)                        # Convert the image to JPEG format in memory
                            _, jpeg_img = cv2.imencode('.jpg', frame)

                            # Convert the JPEG image bytes to a byte stream
                            img_byte_stream = io.BytesIO(jpeg_img.tobytes())

                            notifier.alert(img_byte_stream)
                        
                            logger.log_data('data.csv', {'type':'alert','info':'unidentified person detected'})
                            notifier_triggered = True
                    
            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()