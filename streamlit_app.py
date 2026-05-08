import streamlit as st
import cv2
import tempfile
import numpy as np
import math
from collections import defaultdict
import pandas as pd
from ultralytics import YOLO
import time
import psutil
import os

# ==========================================
# STREAMLIT INTERFACE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Advanced Sports MOT", layout="wide")
st.title("Advanced Sports MOT: Tracking & Analytics")

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.header("Model Configuration")
model_path = st.sidebar.text_input("Detection Model Path", "best.pt")
tracker_type = st.sidebar.selectbox("Tracking Model", ["bytetrack.yaml", "botsort.yaml"])
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.3)

# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource
def load_model(path):
    return YOLO(path)

# ==========================================
# VIDEO SELECTION FROM ROOT FOLDER
# ==========================================
VIDEO_FOLDER = "."  # folder gốc hiện tại

video_files = [
    f for f in os.listdir(VIDEO_FOLDER)
    if f.lower().endswith((".mp4", ".avi", ".mov"))
]

default_video = "LIONEL_MESSI.mp4"

# Nếu file mặc định không tồn tại thì chọn file đầu tiên
default_index = 0
if default_video in video_files:
    default_index = video_files.index(default_video)

selected_video = st.selectbox(
    "Select a sports video",
    video_files,
    index=default_index
)

video_path = os.path.join(VIDEO_FOLDER, selected_video)

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
if selected_video:

    if st.button("Start Tracking & Analytics"):
        try:
            model = load_model(model_path)
            cap = cv2.VideoCapture(video_path)

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            unique_ids = set()
            conf_history = []
            track_history = defaultdict(list)
            distance_covered = defaultdict(float)
            heatmap_canvas = np.zeros((height, width), dtype=np.float32)

            st.subheader("System Performance")
            sys_col1, sys_col2, sys_col3, sys_col4 = st.columns(4)
            metric_fps = sys_col1.empty()
            metric_infer = sys_col2.empty()
            metric_cpu = sys_col3.empty()
            metric_ram = sys_col4.empty()

            st.divider()

            st.subheader("Tracking Metrics")
            trk_col1, trk_col2, trk_col3 = st.columns(3)
            metric_active = trk_col1.empty()
            metric_unique = trk_col2.empty()
            metric_conf = trk_col3.empty()

            col_vid, col_heat = st.columns(2)

            with col_vid:
                st.text("Live Tracking")
                st_frame = st.empty()

            with col_heat:
                st.text("Movement Heatmap")
                st_heatmap = st.empty()

            col_chart, col_table = st.columns(2)

            with col_chart:
                st.text("Average Confidence Score per Frame")
                st_chart = st.empty()

            with col_table:
                st.text("Distance Covered by Player (Pixels)")
                st_table = st.empty()

            prev_time = time.time()

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                start_time = time.time()

                results = model.track(
                    frame,
                    persist=True,
                    tracker=tracker_type,
                    conf=conf_threshold
                )

                annotated_frame = results[0].plot()

                end_time = time.time()

                total_process_time = end_time - start_time
                fps = 1 / total_process_time if total_process_time > 0 else 0

                infer_time_ms = results[0].speed.get('inference', 0.0)

                cpu_usage = psutil.cpu_percent()
                ram_usage = psutil.virtual_memory().percent

                boxes = results[0].boxes

                active_ids_count = 0
                avg_conf = 0.0

                if boxes is not None and boxes.id is not None:

                    active_ids_count = len(boxes)

                    track_ids = boxes.id.int().cpu().tolist()
                    confs = boxes.conf.cpu().tolist()
                    coords = boxes.xyxy.cpu().tolist()

                    avg_conf = sum(confs) / len(confs) if confs else 0.0

                    for i, track_id in enumerate(track_ids):

                        unique_ids.add(track_id)

                        x1, y1, x2, y2 = coords[i]

                        cx = int((x1 + x2) / 2)
                        cy = int(y2)

                        if len(track_history[track_id]) > 0:

                            prev_x, prev_y = track_history[track_id][-1]

                            dist = math.hypot(cx - prev_x, cy - prev_y)

                            distance_covered[track_id] += dist

                        track_history[track_id].append((cx, cy))

                        cv2.circle(
                            heatmap_canvas,
                            (cx, cy),
                            radius=15,
                            color=1,
                            thickness=-1
                        )

                conf_history.append(avg_conf)

                blurred_canvas = cv2.GaussianBlur(
                    heatmap_canvas,
                    (51, 51),
                    0
                )

                normalized_canvas = cv2.normalize(
                    blurred_canvas,
                    None,
                    0,
                    255,
                    cv2.NORM_MINMAX,
                    dtype=cv2.CV_8U
                )

                colored_heatmap = cv2.applyColorMap(
                    normalized_canvas,
                    cv2.COLORMAP_JET
                )

                heatmap_overlay = cv2.addWeighted(
                    frame,
                    0.5,
                    colored_heatmap,
                    0.5,
                    0
                )

                metric_fps.metric(
                    "Realtime FPS",
                    f"{fps:.1f} fps"
                )

                metric_infer.metric(
                    "YOLO Inference",
                    f"{infer_time_ms:.1f} ms"
                )

                metric_cpu.metric(
                    "CPU Usage",
                    f"{cpu_usage}%"
                )

                metric_ram.metric(
                    "RAM Usage",
                    f"{ram_usage}%"
                )

                metric_active.metric(
                    "Active IDs",
                    active_ids_count
                )

                metric_unique.metric(
                    "Total Unique IDs",
                    len(unique_ids)
                )

                metric_conf.metric(
                    "Avg Confidence",
                    f"{avg_conf:.2f}"
                )

                st_frame.image(
                    cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True
                )

                st_heatmap.image(
                    cv2.cvtColor(heatmap_overlay, cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True
                )

                if len(conf_history) > 0:
                    st_chart.line_chart(conf_history)

                if len(distance_covered) > 0:

                    df_dist = pd.DataFrame(
                        list(distance_covered.items()),
                        columns=['Player ID', 'Distance (Pixels)']
                    )

                    df_dist['Distance (Pixels)'] = (
                        df_dist['Distance (Pixels)'].astype(int)
                    )

                    df_dist = df_dist.sort_values(
                        by='Distance (Pixels)',
                        ascending=False
                    ).head(10)

                    st_table.dataframe(
                        df_dist,
                        use_container_width=True,
                        hide_index=True
                    )

            cap.release()

            st.success("Analysis completed successfully!")

        except Exception as e:
            st.error(f"Error processing video: {e}")