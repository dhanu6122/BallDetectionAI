import streamlit as st
import cv2
import av
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

st.set_page_config(page_title="Ball Detection AI", page_icon="🔴", layout="wide")

# -------------------- LOGIN --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

USER_CREDENTIALS = {
    "user1": "pass123",
    "judge": "hack2026"
}

if not st.session_state.logged_in:

    st.title("🔴 Ball Detection AI")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()

# -------------------- MAIN PAGE --------------------

st.title("🔴 Ball Detection AI")

st.success("Login Successful!")

st.write("Start the webcam below.")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        results = model(img)

        for r in results:

            for box in r.boxes:

                cls = int(box.cls[0])

                name = model.names[cls]

                if name == "sports ball":

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(img,
                                  (x1, y1),
                                  (x2, y2),
                                  (0,255,0),
                                  3)

                    cv2.putText(img,
                                "BALL",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0,255,0),
                                2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]}
)

webrtc_streamer(
    key="ball-detection",
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video":True,
        "audio":False
    }
)