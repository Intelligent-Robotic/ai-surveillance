import cv2
import requests
import numpy as np

def display_mjpeg_stream(url):
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
            cv2.imshow('MJPEG Stream', frame)
            if cv2.waitKey(1) == ord('q'):
                break

    cv2.destroyAllWindows()

# Specify the URL of the MJPEG video stream
mjpeg_url = 'http://192.168.192.55:5000/video_feed'

# Call the function to display the MJPEG stream
display_mjpeg_stream(mjpeg_url)
