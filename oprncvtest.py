import cv2

def open_webcam():
    # Open the default webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the video feed frame by frame
        ret, frame = cap.read()

        # Display the frame in a window called "Webcam"
        cv2.imshow('Webcam', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to open the webcam
open_webcam()
