import io
import time
from flask import Flask, Response
from picamera2 import Picamera2

app = Flask(__name__)

def generate_video_stream():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration())
    picam2.start()

    # Create an in-memory bytes buffer for the video frames
    output_buffer = io.BytesIO()

    # Capture video frames for a specified duration
    start_time = time.time()
    duration = 10  # Capture for 10 seconds

    while time.time() - start_time < duration:
        frame = picam2.capture_array()
        output_buffer.write(frame.tobytes())

    picam2.stop()

    # Get the captured video data from the output buffer
    output_data = output_buffer.getvalue()
    return output_data

@app.route('/video')
def video():
    def generate():
        output_data = generate_video_stream()
        yield output_data

    return Response(generate(), mimetype='video/h264')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
