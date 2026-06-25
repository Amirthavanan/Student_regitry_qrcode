import streamlit as st
import numpy as np
import qrcode
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
import io
import base64
from PIL import Image
import cv2

# ── Streamlit Option Menu Import Fallback ───────────────────────────────────
try:
    from streamlit_option_menu import option_menu
except ImportError:
    option_menu = None

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Feedback Matrix | QR & Barcode Manager",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Premium Global CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

/* Base style overrides */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #09090e 0%, #11111f 50%, #07070b 100%) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #f3f4f6 !important;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

/* Main layout padding */
[data-testid="stMainBlockContainer"] {
    padding: 2rem 1rem !important;
    max-width: 800px;
    margin: 0 auto;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* Glassmorphism main card */
.glass-container {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.2rem;
    margin: 1.5rem 0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    animation: fadeInUp 0.6s ease;
}

/* Custom glass card for DB records */
.glass-card-db {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.glass-card-db:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
}

/* Badges */
.badge-id {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #a5b4fc;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    font-family: 'Space Grotesk', monospace;
    letter-spacing: 0.5px;
}
.badge-platform {
    background: rgba(167, 139, 250, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.3);
    color: #c084fc;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}

/* Action links */
.action-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #818cf8 !important;
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 600;
    transition: color 0.2s;
    margin-top: 8px;
}
.action-link:hover {
    color: #a5b4fc !important;
}

/* Hero Header styling */
.hero-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    animation: fadeInDown 0.8s ease;
}
.hero-header h1 {
    font-size: 3.2rem;
    background: linear-gradient(90deg, #818cf8, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1.5px;
    margin-bottom: 0.5rem;
}
.hero-header p {
    color: rgba(255, 255, 255, 0.6);
    font-size: 1.1rem;
    font-weight: 400;
}

/* Form controls customization */
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label, [data-testid="stColorPicker"] label, [data-testid="stSlider"] label {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px;
}
[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
}

/* Streamlit Buttons */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 18px rgba(99, 102, 241, 0.3) !important;
    width: 100%;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5) !important;
    opacity: 0.95 !important;
}

/* Result and scanning cards */
.result-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1.5px solid rgba(52, 211, 153, 0.3);
    border-radius: 20px;
    padding: 1.75rem;
    margin-top: 1.5rem;
    box-shadow: 0 8px 32px rgba(52, 211, 153, 0.1);
    animation: scaleUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.error-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1.5px solid rgba(248, 113, 113, 0.3);
    border-radius: 20px;
    padding: 1.75rem;
    margin-top: 1.5rem;
    box-shadow: 0 8px 32px rgba(248, 113, 113, 0.1);
    animation: scaleUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.result-card h3, .error-card h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
}

/* Big redirect button */
.redirect-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1.1rem;
    text-decoration: none !important;
    margin-top: 1.25rem;
    text-align: center;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    transition: all 0.3s ease;
}
.redirect-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.6);
}

/* Animations */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleUp {
    from { opacity: 0; transform: scale(0.92); }
    to { opacity: 1; transform: scale(1); }
}

/* Divider lines */
hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
    margin: 1.75rem 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ── NumPy Database Setup ──────────────────────────────────────────────────────
# Define the NumPy structured array dtype
db_dtype = np.dtype([
    ('id', 'U10'),
    ('business_name', 'U50'),
    ('platform', 'U20'),
    ('url', 'U256'),
    ('description', 'U100')
])

def get_initial_db():
    data = [
        ('FB-001', 'Wrench Wise Services', 'Google Maps', 'https://maps.google.com/?cid=wrenchwise_sample', 'Leave feedback on Google Maps for our mechanical services'),
        ('FB-002', 'Gearheads Tuning', 'Yelp', 'https://www.yelp.com/biz/gearheads-tuning-sample', 'Review our performance tuning shop on Yelp'),
        ('FB-003', 'AutoSpa Detailers', 'Trustpilot', 'https://www.trustpilot.com/review/autospa-sample', 'Share your car detailing experience on Trustpilot'),
        ('FB-004', 'CyclePath Rentals', 'Facebook', 'https://www.facebook.com/cyclepath-rentals-sample/reviews', 'Review our bike rental shop on Facebook')
    ]
    return np.array(data, dtype=db_dtype)

if 'feedback_db' not in st.session_state:
    st.session_state.feedback_db = get_initial_db()

# ── NumPy Database Helper Functions ───────────────────────────────────────────
def add_record(new_id, name, platform, url, desc):
    db = st.session_state.feedback_db
    new_id = new_id.strip().upper()
    
    # Validation
    if not new_id:
        return False, "ID cannot be empty."
    if not name.strip():
        return False, "Business Name cannot be empty."
    if not url.strip():
        return False, "Feedback URL cannot be empty."
    
    # Check if ID already exists using NumPy's vector operations
    if np.any(db['id'] == new_id):
        return False, f"ID '{new_id}' already exists in the database!"
        
    # Create the new record row
    new_row = np.array([(new_id, name.strip(), platform.strip(), url.strip(), desc.strip())], dtype=db_dtype)
    
    # Concatenate using numpy
    st.session_state.feedback_db = np.concatenate([db, new_row])
    return True, f"Record '{new_id}' successfully added!"

def get_record(target_id):
    db = st.session_state.feedback_db
    target_id = target_id.strip().upper()
    
    # Query using NumPy's np.where
    indices = np.where(db['id'] == target_id)[0]
    if len(indices) > 0:
        # Return record fields as a dictionary for easy reading
        record = db[indices[0]]
        return {
            'id': record['id'],
            'business_name': record['business_name'],
            'platform': record['platform'],
            'url': record['url'],
            'description': record['description']
        }
    return None

# ── QR / Barcode Generator Functions ──────────────────────────────────────────
def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_code(data: str, fg_color: str, bg_color: str, style: str, box_size: int, border: int):
    # QR setup
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    fg_rgb = hex_to_rgb(fg_color)
    bg_rgb = hex_to_rgb(bg_color)
    
    img = qr.make_image(fill_color=fg_rgb, back_color=bg_rgb)
    pil_img = img.convert("RGBA")
    
    # Custom pixel patterns using numpy for Gapped Square style
    if style == "Gapped Square":
        arr = np.array(pil_img)
        bs = box_size
        for y in range(0, arr.shape[0], bs):
            for x in range(0, arr.shape[1], bs):
                patch = arr[y:y+bs, x:x+bs]
                if patch.size > 0:
                    # shrink module by creating a gap on borders
                    gap = max(1, bs // 6)
                    arr[y:y+gap, x:x+bs] = (*bg_rgb, 255)
                    arr[y+bs-gap:y+bs, x:x+bs] = (*bg_rgb, 255)
                    arr[y:y+bs, x:x+gap] = (*bg_rgb, 255)
                    arr[y:y+bs, x+bs-gap:x+bs] = (*bg_rgb, 255)
        pil_img = Image.fromarray(arr, "RGBA")
        
    return pil_img

def generate_barcode_img(data: str, fg_color: str, bg_color: str):
    rv = io.BytesIO()
    options = {
        'foreground': fg_color,
        'background': bg_color,
        'module_height': 16.0,
        'module_width': 0.35,
        'text_distance': 4.0,
        'font_size': 11
    }
    barcode_instance = Code128(data, writer=ImageWriter())
    barcode_instance.write(rv, options=options)
    
    return Image.open(rv).convert("RGBA")

# ── Code Scanning and Decoding ───────────────────────────────────────────────
def decode_code_image(image: Image.Image):
    img_rgb = image.convert('RGB')
    
    # 1. Attempt decoding with pyzbar
    try:
        import pyzbar.pyzbar as pyzbar
        decoded_objs = pyzbar.decode(img_rgb)
        if decoded_objs:
            data = decoded_objs[0].data.decode('utf-8')
            type_ = decoded_objs[0].type
            return data, type_
    except Exception:
        pass
        
    # 2. Fallback to OpenCV QRCodeDetector
    try:
        img_np = np.array(img_rgb)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        detector = cv2.QRCodeDetector()
        val, pts, qr_img = detector.detectAndDecode(img_cv)
        if val:
            return val, "QRCODE"
    except Exception:
        pass
        
    return None, None

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>⚡ Feedback Matrix</h1>
    <p>Manage review locations, generate scannable codes, and retrieve customer feedback portals.</p>
</div>
""", unsafe_allow_html=True)

# ── Navigation Menu ───────────────────────────────────────────────────────────
if option_menu:
    selected = option_menu(
        menu_title=None,
        options=["Database Dashboard", "Code Generator", "Scan & Retrieve"],
        icons=["database", "qr-code", "camera"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)", "border": "1px solid rgba(255,255,255,0.08)", "border-radius": "14px"},
            "icon": {"color": "#818cf8", "font-size": "15px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": "#9ca3af", "--hover-color": "rgba(255,255,255,0.06)", "font-weight": "500"},
            "nav-link-selected": {"background-color": "#4f46e5", "color": "#ffffff", "font-weight": "700"},
        }
    )
else:
    selected = st.radio("Navigate", ["Database Dashboard", "Code Generator", "Scan & Retrieve"], horizontal=True)


# ── TAB 1: Database Dashboard ─────────────────────────────────────────────────
if selected == "Database Dashboard":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>📂 Feedback Database (NumPy Array)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Stored in a custom structured NumPy array. High performance retrieval via vector indexes.</p>", unsafe_allow_html=True)
    
    db = st.session_state.feedback_db
    
    if len(db) == 0:
        st.info("No feedback links stored. Add a new record below.")
    else:
        # Render the custom cards
        for row in db:
            st.markdown(f"""
            <div class="glass-card-db">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span class="badge-id">{row['id']}</span>
                        <strong style="color:white; font-size:1.05rem; margin-left:8px;">{row['business_name']}</strong>
                    </div>
                    <span class="badge-platform">{row['platform']}</span>
                </div>
                <p style="color:rgba(255,255,255,0.65); font-size:0.88rem; margin-top:8px; margin-bottom:8px; line-height:1.4;">{row['description']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
                    <a href="{row['url']}" target="_blank" class="action-link">🌐 Visit Review Portal</a>
                    <span style="color:rgba(255,255,255,0.3); font-size:0.75rem; word-break:break-all;">{row['url'][:55] + '...' if len(row['url']) > 55 else row['url']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Form to add a new record
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>➕ Register New Feedback Portal</h3>", unsafe_allow_html=True)
    
    with st.form("add_portal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_id = st.text_input("Feedback ID (e.g. FB-005)", placeholder="FB-005")
            new_name = st.text_input("Business / Product Name", placeholder="My Shop")
        with col2:
            new_platform = st.selectbox("Platform", ["Google Maps", "Yelp", "Trustpilot", "Facebook", "TripAdvisor", "Custom Platform"])
            new_platform_val = st.text_input("Custom Platform Name (if selected Custom)", placeholder="E.g. AppStore")
            
        new_url = st.text_input("Feedback/Review URL", placeholder="https://g.page/r/...")
        new_desc = st.text_input("Short Description", placeholder="Leave a review for our service...")
        
        submit_btn = st.form_submit_button("✨ Save to NumPy Array")
        
        if submit_btn:
            platform = new_platform_val if new_platform == "Custom Platform" else new_platform
            success, msg = add_record(new_id, new_name, platform, new_url, new_desc)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
                
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 2: Code Generator ─────────────────────────────────────────────────────
elif selected == "Code Generator":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>🎨 Generate Scannable Portal Code</h3>", unsafe_allow_html=True)
    
    db = st.session_state.feedback_db
    
    if len(db) == 0:
        st.warning("Please add records to the database dashboard first before generating codes.")
    else:
        # Create option labels: "FB-001 (Wrench Wise Services)"
        options_list = [f"{row['id']} - {row['business_name']} [{row['platform']}]" for row in db]
        selected_option = st.selectbox("Select Feedback Record", options_list)
        
        # Get target record ID
        target_id = selected_option.split(" - ")[0]
        record = get_record(target_id)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            code_type = st.radio("Code Format", ["QR Code", "1D Barcode (Code 128)"])
            
            if code_type == "QR Code":
                qr_style = st.selectbox("Module Shape Style", ["Square", "Gapped Square"])
                fg_color = st.color_picker("Foreground Color", "#ffffff")
                bg_color = st.color_picker("Background Color", "#0d0b21")
                box_size = st.slider("Module Pixel Size", 8, 20, 12)
                border_size = st.slider("Border Margin size", 1, 6, 3)
            else: # Barcode
                fg_color = st.color_picker("Barcode Color", "#ffffff")
                bg_color = st.color_picker("Background Color", "#09090e")
                
        with col2:
            st.markdown("<div style='text-align: center; margin-top: 1.5rem;'>", unsafe_allow_html=True)
            
            if code_type == "QR Code":
                # Generate QR code
                code_img = generate_qr_code(
                    data=record['id'],
                    fg_color=fg_color,
                    bg_color=bg_color,
                    style=qr_style,
                    box_size=box_size,
                    border=border_size
                )
            else:
                # Generate Barcode
                code_img = generate_barcode_img(
                    data=record['id'],
                    fg_color=fg_color,
                    bg_color=bg_color
                )
                
            # Display generated image
            st.image(code_img, width=280)
            
            # Use NumPy to analyze image pixels
            img_arr = np.array(code_img.convert("L"))
            # Calculate dark / foreground ratio
            dark_pixels_ratio = float(np.mean(img_arr < 128) * 100)
            
            st.markdown(f"""
            <div style="margin-top:0.8rem; font-size:0.82rem; color:rgba(255,255,255,0.4);">
                <strong>Dimensions:</strong> {code_img.size[0]}×{code_img.size[1]} px &nbsp;|&nbsp; 
                <strong>Dark Modules:</strong> {dark_pixels_ratio:.1f}%
            </div>
            """, unsafe_allow_html=True)
            
            # Download Image Bytes
            buf = io.BytesIO()
            code_img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label=f"⬇ Download {code_type} (PNG)",
                data=img_bytes,
                file_name=f"{record['id']}_{code_type.replace(' ', '_').lower()}.png",
                mime="image/png"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 3: Scan & Retrieve ──────────────────────────────────────────────────
elif selected == "Scan & Retrieve":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>🔍 Scan QR Code or Barcode</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Upload an image or use your device camera. The application decodes the code and queries the NumPy database.</p>", unsafe_allow_html=True)
    
    # Three Modes
    scan_mode = st.radio("Scanning Source", ["Simulated Quick Scan (Developer Mode)", "Upload Code Image", "Use Webcam"], horizontal=True)
    
    scanned_id = None
    code_type = None
    
    if scan_mode == "Simulated Quick Scan (Developer Mode)":
        db = st.session_state.feedback_db
        if len(db) == 0:
            st.warning("Database is empty. Please add records first.")
        else:
            # Let developer test both valid and invalid scenarios
            test_scenarios = ["-- Select Scenario --"]
            for row in db:
                test_scenarios.append(f"Valid Scanned Code: {row['id']}")
            test_scenarios.extend(["Invalid Code Scenario: FB-999", "Invalid Code Scenario: BADCODE123", "Custom Code Input"])
            
            chosen_scenario = st.selectbox("Select Scenario or Custom Input", test_scenarios)
            
            if "Valid Scanned Code" in chosen_scenario:
                scanned_id = chosen_scenario.split(": ")[1]
                code_type = "QRCODE"
            elif "Invalid Code Scenario" in chosen_scenario:
                scanned_id = chosen_scenario.split(": ")[1]
                code_type = "QRCODE"
            elif chosen_scenario == "Custom Code Input":
                custom_id = st.text_input("Enter Scanned Code String", placeholder="FB-001")
                if custom_id:
                    scanned_id = custom_id
                    code_type = "CUSTOM"
                    
    elif scan_mode == "Upload Code Image":
        uploaded_file = st.file_uploader("Upload QR code or Barcode Image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, width=200, caption="Uploaded Image")
            
            with st.spinner("Decoding image…"):
                scanned_id, code_type = decode_code_image(image)
                if not scanned_id:
                    st.error("❌ Could not decode any QR Code or Barcode from this image. Make sure it is clear and well-lit.")
                    
    elif scan_mode == "Use Webcam":
        webcam_img = st.camera_input("Capture QR/Barcode")
        if webcam_img is not None:
            image = Image.open(webcam_img)
            with st.spinner("Processing camera capture…"):
                scanned_id, code_type = decode_code_image(image)
                if not scanned_id:
                    st.error("❌ Could not decode any QR Code or Barcode from this capture. Keep the code flat, aligned and close to the camera.")
                    
    # ── Process Result ──
    if scanned_id:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:rgba(255,255,255,0.4); font-size:0.85rem;'>Decoded Data: <code>{scanned_id}</code> (Type: <code>{code_type}</code>)</p>", unsafe_allow_html=True)
        
        # Retrieve from numpy array
        record = get_record(scanned_id)
        
        if record:
            # RENDER SUCCESS CARD
            st.markdown(f"""
            <div class="result-card">
                <span class="badge-id" style="background:rgba(52,211,153,0.15); border-color:#34d399; color:#34d399;">✓ MATCH FOUND</span>
                <h3 style="margin-top: 8px; color: white;">{record['business_name']}</h3>
                <p style="color: rgba(255,255,255,0.8); font-size: 0.95rem; line-height: 1.4; margin-bottom: 8px;">
                    {record['description']}
                </p>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.45); margin-bottom: 12px;">
                    <strong>Portal:</strong> {record['platform']} &nbsp;|&nbsp; <strong>Record ID:</strong> {record['id']}
                </div>
                
                <a href="{record['url']}" target="_blank" class="redirect-btn">
                    ⭐ Open Feedback & Review Portal
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            # Show a nice interactive display of the URL
            st.text_input("Review Portal URL", value=record['url'], disabled=True)
        else:
            # RENDER ERROR CARD (Invalid ID)
            st.markdown(f"""
            <div class="error-card">
                <span class="badge-id" style="background:rgba(248,113,113,0.15); border-color:#f87171; color:#f87171;">✗ UNKNOWN CODE / ID</span>
                <h3 style="margin-top: 8px; color: white;">Invalid ID: {scanned_id}</h3>
                <p style="color: rgba(255,255,255,0.75); font-size: 0.9rem; line-height: 1.4;">
                    This code decodes to <strong>"{scanned_id}"</strong>, which does not match any registered feedback portal in our NumPy database.
                </p>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem; margin-top: 10px;">
                    Please go to the <strong>Database Dashboard</strong> tab to register this ID, or scan/upload a different code.
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;color:rgba(255,255,255,0.25);font-size:0.8rem;">
    Built with ♥ using NumPy, OpenCV, pyzbar &amp; Streamlit · Wrench Wise
</div>
""", unsafe_allow_html=True)
