import cv2
import time
 
def capture(filename):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    # Wait for the camera to warm up
    time.sleep(0.2)

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        cap.release()
        return False

    save_result = cv2.imwrite(filename, frame)

    cap.release()
    
    return save_result


def generate_frames():
    """Generate frames from the webcam for streaming."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert the frame to bytes and yield as a multipart response
        frame_bytes = buffer.tobytes()

        # Yield the image bytes in a multipart stream format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


if __name__ == '__main__':
    filename = 'snapshot.png'
    capture(filename)

