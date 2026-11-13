import io
import time
import os
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageOps

os.environ["DEEPFACE_LOG_LEVEL"] = "40"

MAX_SIDE = 960

# DeepFace gives 7 emotions, MindMate has 5 core moods
EMOTION_TO_MOOD = {
    "happy": "Happy",
    "sad": "Sad",
    "angry": "Angry",
    "disgust": "Angry",
    "fear": "Stressed",
    "surprise": "Neutral",
    "neutral": "Neutral",
}

MOOD_COLORS = {
    "Happy": {"hex": "#22c55e", "bgr": (94, 197, 34), "rgb": (34, 197, 94)},
    "Sad": {"hex": "#3b82f6", "bgr": (246, 130, 59), "rgb": (59, 130, 246)},
    "Angry": {"hex": "#ef4444", "bgr": (68, 68, 239), "rgb": (239, 68, 68)},
    "Stressed": {"hex": "#8b5cf6", "bgr": (246, 92, 139), "rgb": (139, 92, 246)},
    "Neutral": {"hex": "#94a3b8", "bgr": (184, 163, 148), "rgb": (148, 163, 184)},
}

MOOD_LIVE_ADVICE = {
    "Sad": (
        "💙 **MindMate Analysis**: We detect sadness or feeling low. "
        "It is completely okay to not feel 100%. Be gentle with yourself, "
        "take a slow breath, or try the **Heart Catch** game / a gentle journal entry."
    ),
    "Happy": (
        "✨ **MindMate Analysis**: Radiant positive mood detected! "
        "Your facial expression shows high happiness and joy. "
        "Keep the positive momentum going with **Balloon Pop** or log your gratitude!"
    ),
    "Angry": (
        "💥 **MindMate Analysis**: Tension or frustration detected. "
        "Release the built-up physical tension by taking 3 deep exhalations, "
        "or try the **Stress Smash** activity to let it out safely."
    ),
    "Stressed": (
        "🌿 **MindMate Analysis**: Signs of stress or anxiety detected. "
        "Let's slow things down. Try the **Guided Box Breathing** or "
        "the **5-4-3-2-1 Grounding** in Calm Toolkit."
    ),
    "Neutral": (
        "🎧 **MindMate Analysis**: Calm and balanced expression detected. "
        "A peaceful state of mind. Perfect for listening to relaxing music "
        "in the **Music Lounge** or checking off your daily habits."
    ),
}

BACKENDS = {
    "Smart MTCNN (Accurate)": "mtcnn",
    "Fast (Skip/Direct)": "skip",
}


@st.cache_resource(show_spinner="Loading face emotion model (first time only)...")
def _load_deepface():
    from deepface import DeepFace
    dummy = np.zeros((224, 224, 3), dtype=np.uint8)
    try:
        DeepFace.analyze(dummy, actions=["emotion"], detector_backend="skip",
                         enforce_detection=False, silent=True)
    except Exception:
        pass
    return DeepFace


@st.cache_resource(show_spinner="Loading face detector...")
def _load_mtcnn():
    from mtcnn import MTCNN
    return MTCNN()


def _prepare(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    return img


def _mood_scores(scores, moods):
    out = {m: 0.0 for m in moods}
    for emo, val in scores.items():
        if emo in EMOTION_TO_MOOD:
            out[EMOTION_TO_MOOD[emo]] += float(val)
    total = sum(out.values())
    if total > 0:
        out = {k: (v / total) * 100.0 for k, v in out.items()}
    return out


def _top_mood(scores, moods):
    ms = _mood_scores(scores, moods)
    best = max(ms, key=ms.get)
    return best, ms[best], ms


def _detect_static(img_bytes, backend, moods):
    """Detect faces and emotions for static uploaded image or snapshot."""
    DeepFace = _load_deepface()
    mtcnn_detector = _load_mtcnn()
    img = _prepare(img_bytes)
    rgb_arr = np.array(img)
    
    faces = []
    try:
        detections = mtcnn_detector.detect_faces(rgb_arr)
    except Exception:
        detections = []

    if detections:
        for det in detections:
            if det.get("confidence", 1) < 0.6:
                continue
            x, y, w, h = det["box"]
            x, y = max(0, int(x)), max(0, int(y))
            w, h = max(10, int(w)), max(10, int(h))
            
            # Crop face for emotion analysis
            face_crop = rgb_arr[y:y+h, x:x+w]
            if face_crop.size == 0:
                continue
            
            try:
                res = DeepFace.analyze(
                    face_crop,
                    actions=["emotion"],
                    detector_backend="skip",
                    enforce_detection=False,
                    silent=True
                )
                if isinstance(res, list) and len(res) > 0:
                    emo_scores = {k: float(v) for k, v in res[0]["emotion"].items()}
                elif isinstance(res, dict):
                    emo_scores = {k: float(v) for k, v in res["emotion"].items()}
                else:
                    emo_scores = {"neutral": 100.0}
            except Exception:
                emo_scores = {"neutral": 100.0}
            
            faces.append({
                "x": x, "y": y, "w": w, "h": h,
                "scores": emo_scores
            })
    else:
        # Fallback: analyze whole image directly
        try:
            res = DeepFace.analyze(
                rgb_arr,
                actions=["emotion"],
                detector_backend="skip",
                enforce_detection=False,
                silent=True
            )
            if isinstance(res, list) and len(res) > 0:
                emo_scores = {k: float(v) for k, v in res[0]["emotion"].items()}
            elif isinstance(res, dict):
                emo_scores = {k: float(v) for k, v in res["emotion"].items()}
            else:
                emo_scores = {"neutral": 100.0}
            faces.append({
                "x": int(img.width * 0.15), "y": int(img.height * 0.15),
                "w": int(img.width * 0.70), "h": int(img.height * 0.70),
                "scores": emo_scores
            })
        except Exception:
            pass

    faces.sort(key=lambda f: f["w"] * f["h"], reverse=True)
    return faces


def _draw_static_faces(img, faces, chosen, moods):
    img = img.copy()
    d = ImageDraw.Draw(img)
    for i, f in enumerate(faces):
        mood, conf, _ = _top_mood(f["scores"], moods)
        color = MOOD_COLORS.get(mood, {}).get("hex", "#22c55e") if i == chosen else "#94a3b8"
        
        # Bounding box
        box_thickness = max(3, img.width // 200)
        d.rectangle(
            [f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]],
            outline=color, width=box_thickness,
        )
        
        # Header text
        label = f"#{i + 1} {moods[mood]['emoji']} {mood} ({conf:.0f}%)"
        d.text((f["x"] + 6, max(0, f["y"] - 18)), label, fill=color)
    return img


def _use_mood(mood, add_xp=None):
    st.session_state.current_mood = mood
    st.session_state.face_scanned = True
    st.session_state.face_flash = f"Current mood updated to {mood}."
    if add_xp:
        add_xp(20, "Face Mood Scan")


def _use_and_log(mood, save_entry, add_xp=None):
    save_entry(mood, "Logged from Face Mood Scan")
    st.session_state.current_mood = mood
    st.session_state.face_scanned = True
    st.session_state.face_flash = f"{mood} set as current mood and logged in history (+40 XP)."
    if add_xp:
        add_xp(40, "Face Mood Scan & Log")


def render_face_page(MOODS, save_entry, render_html=None, add_xp=None):
    """Main render function for the Face Mood Analysis page."""

    if render_html:
        render_html('<div class="main-title">Face Mood Analysis 📸</div>')
        render_html(
            '<div class="subtitle">Real-time facial emotion recognition & mood intelligence. '
            'Show your face and MindMate will instantly detect how you feel.</div>'
        )
    else:
        st.markdown('### Face Mood Analysis 📸')
        st.caption('Show your face and MindMate will instantly detect your mood.')

    try:
        _load_deepface()
    except ImportError:
        st.error("DeepFace is required. Please ensure deepface and tf-keras are installed.")
        return

    flash = st.session_state.pop("face_flash", None)
    if flash:
        st.success("💙 " + flash)

    scan_mode = st.radio(
        "Select Detection Mode",
        ["🎥 Live Real-Time Camera", "📷 Camera Snapshot", "🖼️ Upload Photo"],
        horizontal=True,
        key="face_scan_mode"
    )

    # ============================================================
    # MODE 1: LIVE REAL-TIME CAMERA
    # ============================================================
    if scan_mode == "🎥 Live Real-Time Camera":
        st.markdown(
            "#### 🎥 Live Webcam Mood Detection\n"
            "MindMate will continuously analyze your facial expressions in real-time "
            "and identify whether you are **Sad 😔**, **Happy 😊**, **Angry 😡**, "
            "**Stressed 😰**, or **Neutral 😐**."
        )

        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])
        
        cam_idx = ctrl_col1.selectbox("Camera Device Index", [0, 1, 2], index=0, key="cam_device_idx")
        fps_target = ctrl_col2.select_slider("Detection Speed", options=["Fast (Responsive)", "Balanced", "High Accuracy"], value="Balanced")
        frame_interval = 4 if fps_target == "Fast (Responsive)" else (6 if fps_target == "Balanced" else 8)

        if "live_face_running" not in st.session_state:
            st.session_state.live_face_running = False

        c_start, c_stop = ctrl_col3.columns(2)
        start_btn = c_start.button("▶️ Start Live", use_container_width=True, type="primary", disabled=st.session_state.live_face_running)
        stop_btn = c_stop.button("⏹️ Stop", use_container_width=True, disabled=not st.session_state.live_face_running)

        if start_btn:
            st.session_state.live_face_running = True
            st.rerun()

        if stop_btn:
            st.session_state.live_face_running = False
            st.rerun()

        col_video, col_hud = st.columns([3, 2])

        video_feed = col_video.empty()
        status_box = col_hud.empty()

        if st.session_state.live_face_running:
            DeepFace = _load_deepface()
            mtcnn_detector = _load_mtcnn()

            cap = cv2.VideoCapture(cam_idx)
            if not cap.isOpened():
                st.error(f"Could not open camera {cam_idx}. Please check webcam connections and permissions.")
                st.session_state.live_face_running = False
                return

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            last_scores = {"neutral": 100.0}
            last_mood = "Neutral"
            last_conf = 100.0
            last_boxes = []
            frame_count = 0

            st.caption("🔴 **Live Detection Active**. Press '⏹️ Stop' in the controls above when finished.")

            try:
                while st.session_state.get("live_face_running", False):
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("Webcam stream disconnected.")
                        break

                    frame = cv2.flip(frame, 1)  # Mirror view
                    h, w, _ = frame.shape
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_count += 1

                    # Run face detection and emotion analysis periodically for fluid FPS
                    if frame_count % frame_interval == 0 or len(last_boxes) == 0:
                        try:
                            detections = mtcnn_detector.detect_faces(rgb)
                        except Exception:
                            detections = []

                        if detections:
                            last_boxes = []
                            for det in detections:
                                if det.get("confidence", 0) > 0.6:
                                    bx, by, bw, bh = det["box"]
                                    bx, by = max(0, int(bx)), max(0, int(by))
                                    bw, bh = max(10, int(bw)), max(10, int(bh))
                                    last_boxes.append((bx, by, bw, bh))

                            if last_boxes:
                                # Analyze primary face
                                bx, by, bw, bh = last_boxes[0]
                                face_crop = rgb[by:by+bh, bx:bx+bw]
                                if face_crop.size > 0:
                                    try:
                                        res = DeepFace.analyze(
                                            face_crop,
                                            actions=["emotion"],
                                            detector_backend="skip",
                                            enforce_detection=False,
                                            silent=True
                                        )
                                        if isinstance(res, list) and len(res) > 0:
                                            raw_scores = res[0]["emotion"]
                                        elif isinstance(res, dict):
                                            raw_scores = res["emotion"]
                                        else:
                                            raw_scores = {"neutral": 100.0}
                                        
                                        # Exponential moving average smoothing
                                        alpha = 0.6
                                        for k in raw_scores:
                                            last_scores[k] = alpha * float(raw_scores[k]) + (1 - alpha) * last_scores.get(k, 0.0)
                                        
                                        best_m, best_c, _ = _top_mood(last_scores, MOODS)
                                        last_mood = best_m
                                        last_conf = best_c
                                    except Exception:
                                        pass
                        else:
                            last_boxes = []

                    # Draw stylish HUD overlays on the frame
                    for (bx, by, bw, bh) in last_boxes:
                        mood_info = MOOD_COLORS.get(last_mood, MOOD_COLORS["Neutral"])
                        bgr_color = mood_info["bgr"]
                        
                        # Rounded corner bounding box
                        cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), bgr_color, 2)
                        
                        # Top label background
                        label_text = f"{last_mood} {last_conf:.0f}%"
                        cv2.rectangle(frame, (bx, max(0, by - 28)), (bx + len(label_text) * 12 + 10, by), bgr_color, -1)
                        cv2.putText(frame, label_text, (bx + 5, max(12, by - 8)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

                    # Update video feed in Streamlit
                    display_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_feed.image(display_rgb, channels="RGB", use_container_width=True)

                    # Update the live HUD on the right
                    with status_box.container():
                        info = MOODS.get(last_mood, MOODS["Neutral"])
                        color_hex = MOOD_COLORS.get(last_mood, {}).get("hex", "#22c55e")
                        
                        if render_html:
                            render_html(
                                f"""
                                <div style="background:linear-gradient(135deg,#172033,#1e293b);
                                            border-radius:20px; padding:22px; color:white;
                                            border:2px solid {color_hex}; box-shadow:0 10px 30px rgba(0,0,0,0.25); text-align:center;">
                                    <div style="font-size:52px; line-height:1;">{info['emoji']}</div>
                                    <h2 style="color:white; margin:8px 0 4px;">{last_mood}</h2>
                                    <div style="font-size:15px; color:#cbd5e1; font-weight:600;">{last_conf:.0f}% Confidence Match</div>
                                    <div style="font-size:13px; color:#94a3b8; margin-top:4px;">{info['description']}</div>
                                </div>
                                """
                            )
                        else:
                            st.markdown(f"### {info['emoji']} {last_mood} ({last_conf:.0f}%)")

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("##### 📊 Live Emotion Spectrum")
                        _, _, cur_mood_scores = _top_mood(last_scores, MOODS)
                        for m_name in MOODS:
                            score_val = cur_mood_scores.get(m_name, 0.0)
                            st.progress(min(1.0, max(0.0, score_val / 100.0)),
                                        text=f"{MOODS[m_name]['emoji']} {m_name}: {score_val:.1f}%")

                        st.markdown(MOOD_LIVE_ADVICE.get(last_mood, ""))

                        # Store latest detected mood in session for quick actions
                        st.session_state.live_detected_mood = last_mood

                    # Tiny sleep to yield thread
                    time.sleep(0.02)

            finally:
                cap.release()
                cv2.destroyAllWindows()
        else:
            col_video.info("💡 Click **▶️ Start Live** above to begin real-time face mood recognition.")
            if render_html:
                render_html(
                    """
                    <div style="background:white; border-radius:20px; padding:24px; border:1px solid #e2e8f0; text-align:center;">
                        <div style="font-size:45px;">🎥</div>
                        <h3 style="color:#172554; margin:10px 0;">Camera Ready</h3>
                        <p style="color:#64748b; font-size:14px;">
                            Point your webcam towards your face. Good lighting will deliver the most accurate mood recognition.
                        </p>
                    </div>
                    """
                )
            else:
                st.info("Point your webcam towards your face and click Start Live.")

        if "live_detected_mood" in st.session_state:
            act_m = st.session_state.live_detected_mood
            st.markdown("---")
            st.markdown(f"#### ⚡ Quick Actions for detected mood: **{MOODS[act_m]['emoji']} {act_m}**")
            b1, b2 = st.columns(2)
            if b1.button(f"✅ Set {act_m} as my current MindMate mood (+20 XP)", use_container_width=True, key="live_set_mood"):
                _use_mood(act_m, add_xp)
                st.toast(f"Mood updated to {act_m}! (+20 XP)", icon="💙")
            if b2.button(f"📌 Log {act_m} into Journal & History (+40 XP)", use_container_width=True, key="live_log_mood"):
                _use_and_log(act_m, save_entry, add_xp)
                st.toast(f"Logged {act_m} into history! (+40 XP)", icon="📌")

    # ============================================================
    # MODE 2: CAMERA SNAPSHOT
    # ============================================================
    elif scan_mode == "📷 Camera Snapshot":
        st.markdown(
            "#### 📷 Capture Snapshot\n"
            "Take a single photo using your browser camera for deep mood analysis."
        )
        shot = st.camera_input("Look at the camera and take a picture", key="face_cam_snapshot")
        if shot is not None:
            _process_static_image(shot.getvalue(), MOODS, save_entry, render_html, add_xp)

    # ============================================================
    # MODE 3: UPLOAD PHOTO
    # ============================================================
    elif scan_mode == "🖼️ Upload Photo":
        st.markdown(
            "#### 🖼️ Upload Photo\n"
            "Upload any clear face photo (JPG, PNG, WEBP) to scan the mood."
        )
        shot = st.file_uploader(
            "Select an image file",
            type=["jpg", "jpeg", "png", "webp"],
            key="face_upload_static"
        )
        if shot is not None:
            _process_static_image(shot.getvalue(), MOODS, save_entry, render_html, add_xp)


def _process_static_image(img_bytes, MOODS, save_entry, render_html=None, add_xp=None):
    with st.spinner("Analyzing facial expressions..."):
        faces = _detect_static(img_bytes, "mtcnn", MOODS)

    if not faces:
        st.warning(
            "No clear face detected. Tips: Ensure face is well-lit, looking directly at camera, "
            "and unobstructed by masks or shadows."
        )
        return

    chosen = 0
    if len(faces) > 1:
        st.success(f"✨ Found {len(faces)} faces in image.")
        chosen = st.selectbox(
            "Which face would you like to analyze?",
            range(len(faces)),
            format_func=lambda i: f"Face #{i + 1}" + (" (Prominent)" if i == 0 else ""),
            key="static_chosen_face"
        )

    base_img = _prepare(img_bytes)
    left, right = st.columns([3, 2])

    with left:
        st.image(_draw_static_faces(base_img, faces, chosen, MOODS), use_container_width=True)

    mood, conf, mood_scores = _top_mood(faces[chosen]["scores"], MOODS)
    info = MOODS[mood]
    color_hex = MOOD_COLORS.get(mood, {}).get("hex", "#22c55e")

    with right:
        if render_html:
            render_html(
                f"""
                <div style="background:linear-gradient(135deg,#172033,#273449,#334155);
                            border-radius:24px; padding:30px; text-align:center;
                            color:white; border:2px solid {color_hex};
                            box-shadow:0 15px 40px rgba(15,23,42,0.20);">
                    <div style="font-size:65px; line-height:1;">{info["emoji"]}</div>
                    <h2 style="color:white; margin:10px 0;">{mood}</h2>
                    <p style="color:#e2e8f0; font-size:17px; margin:0;">
                        {conf:.0f}% match · {info["description"]}
                    </p>
                </div>
                """
            )
        else:
            st.markdown(f"## {info['emoji']} {mood} ({conf:.0f}%)")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Facial Emotion Breakdown")
    chart = pd.Series(
        {f"{MOODS[m]['emoji']} {m}": round(v, 1) for m, v in mood_scores.items()}
    )
    st.bar_chart(chart, height=240)

    st.markdown(MOOD_LIVE_ADVICE.get(mood, ""))

    b1, b2 = st.columns(2)
    b1.button(
        f"✅ Use {mood} as my current mood (+20 XP)",
        use_container_width=True,
        on_click=_use_mood, args=(mood, add_xp),
        key="btn_use_static_mood"
    )
    b2.button(
        "📌 Use it and log it to history (+40 XP)",
        use_container_width=True,
        on_click=_use_and_log, args=(mood, save_entry, add_xp),
        key="btn_log_static_mood"
    )