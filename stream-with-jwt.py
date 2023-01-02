import cv2
from flask import Flask, Response
import jwt

app = Flask(__name__)

# Set up the RTSP server
server = "rtsp://localhost:8888/live"
rtsp_server = cv2.VideoWriter(server, cv2.VideoWriter_fourcc(*'MJPG'), 30, (width, height))

# Read and write frames until the video ends
def generate_frame():
    while True:
        # Read a frame
        _, frame = video_capture.read()

        if frame is None:
            # If the video is over, break the loop
            break

        # Write the frame to the RTSP server
        rtsp_server.write(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Function to check the authorization header and extract the JWT token
def check_auth(auth):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        try:
            payload = jwt.decode(auth_token, 'secret', verify=True)
            return True
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    return False

# Function to authenticate and return the RTSP stream
@app.route('/live')
def live():
    auth = check_auth(request.headers)
    if not auth:
        return 'Could not verify your access level for that URL. You have to login with proper credentials'
    return Response(generate_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', port=8888)
