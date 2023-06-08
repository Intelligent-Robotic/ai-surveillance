

import cv2
import face_recognition
known_faces = ["./tester.py"]
known_names = ["tester"]
import numpy as np
def recognize_faces(known_faces, known_names):
    # Open the default webcam
    cap = cv2.VideoCapture(0)



    while True:
        # Read the video feed frame by frame
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB for face recognition
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        face_encodings = np.asarray(face_encodings, dtype=np.float32)

        # Loop through each face in the current frame
        for face_encoding in face_encodings:
            # Attempt to match the face with the known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            # Find all matching indices
            matching_indices = [index for index, match in enumerate(matches) if match]

            # Check if there are any matching faces
            if matching_indices:
                # Select the first matching face
                first_match_index = matching_indices[0]
                name = known_names[first_match_index]

            # Draw a rectangle around the face and display the name
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Facial Recognition', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
recognize_faces(known_faces,known_names)
