import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    page_title="Student ID Matrix & Analytics",
    page_icon="🎓",
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
    background: linear-gradient(135deg, #060814 0%, #0d1127 50%, #05060f 100%) !important;
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

/* Glassmorphism main container */
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

/* Student Directory Grid Card */
.glass-card-student {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 14px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.glass-card-student:hover {
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
.badge-dept {
    background: rgba(167, 139, 250, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.3);
    color: #c084fc;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
}
.badge-status {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    text-transform: uppercase;
}
.badge-status-active {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
}
.badge-status-suspended {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.35);
    color: #f87171;
}
.badge-status-graduated {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.35);
    color: #60a5fa;
}

/* Hero Header styling */
.hero-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    animation: fadeInDown 0.8s ease;
}
.hero-header h1 {
    font-size: 3.2rem;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
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

/* Form input adjustments */
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label, [data-testid="stColorPicker"] label, [data-testid="stSlider"] label, [data-testid="stNumberInput"] label {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
}

/* Matplotlib chart wrapper card */
.chart-card {
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
}

/* Premium Student ID Card */
.student-id-card {
    background: linear-gradient(135deg, rgba(20, 24, 48, 0.9) 0%, rgba(10, 12, 28, 0.95) 100%);
    border: 1.5px solid rgba(99, 102, 241, 0.4);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(99, 102, 241, 0.15);
    position: relative;
    overflow: hidden;
    margin-top: 1.5rem;
    animation: scaleUp 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.student-id-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 60%);
    pointer-events: none;
}
.id-card-header {
    border-bottom: 1.5px dashed rgba(255, 255, 255, 0.15);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.id-card-title {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 2px;
    font-size: 0.9rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
}
.id-card-body {
    display: flex;
    gap: 1.75rem;
    align-items: center;
    flex-wrap: wrap;
}
.id-card-avatar {
    width: 110px;
    height: 110px;
    border-radius: 20px;
    border: 2px solid rgba(255,255,255,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.03);
    overflow: hidden;
    flex-shrink: 0;
}
.id-card-info {
    flex-grow: 1;
}
.id-card-name {
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.4rem;
}

/* Invalid Scanned Card */
.invalid-id-card {
    background: linear-gradient(135deg, rgba(40, 16, 16, 0.9) 0%, rgba(20, 8, 8, 0.95) 100%);
    border: 1.5px solid rgba(239, 68, 68, 0.4);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
    margin-top: 1.5rem;
    animation: scaleUp 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
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
# Define structured NumPy array dtype for student details
student_dtype = np.dtype([
    ('student_id', 'U15'),
    ('name', 'U50'),
    ('gender', 'U15'),
    ('department', 'U30'),
    ('gpa', 'f4'),
    ('attendance', 'i4'),
    ('status', 'U15')
])

def get_initial_student_db():
    data = [
        ('STU-1001', 'Alexander Vance', 'Male', 'Computer Science', 3.85, 92, 'Active'),
        ('STU-1002', 'Beatriz Sterling', 'Female', 'Mechanical Eng', 3.42, 88, 'Active'),
        ('STU-1003', 'Charles Dupont', 'Male', 'Electrical Eng', 2.91, 74, 'Active'),
        ('STU-1004', 'Diana Prince', 'Female', 'Computer Science', 3.98, 96, 'Active'),
        ('STU-1005', 'Evan Wright', 'Male', 'Civil Eng', 3.15, 82, 'Active'),
        ('STU-1006', 'Fiona Gallagher', 'Female', 'Physics', 3.67, 90, 'Active'),
        ('STU-1007', 'George Brooks', 'Male', 'Mechanical Eng', 2.75, 78, 'Suspended'),
        ('STU-1008', 'Helena Rostova', 'Female', 'Electrical Eng', 3.55, 85, 'Graduated')
    ]
    return np.array(data, dtype=student_dtype)

if 'student_db' not in st.session_state:
    st.session_state.student_db = get_initial_student_db()

# ── NumPy Database Helper Functions ───────────────────────────────────────────
def add_student_record(sid, name, gender, dept, gpa, att, status):
    db = st.session_state.student_db
    sid = sid.strip().upper()
    name = name.strip()
    
    # Validation
    if not sid:
        return False, "Student ID cannot be empty."
    if not name:
        return False, "Student Name cannot be empty."
    if gpa < 0.0 or gpa > 4.0:
        return False, "GPA must be between 0.0 and 4.0."
    if att < 0 or att > 100:
        return False, "Attendance must be between 0% and 100%."
        
    # Check if student ID already exists using NumPy vector indexing
    if np.any(db['student_id'] == sid):
        return False, f"Student ID '{sid}' is already registered!"
        
    # Create the new record row
    new_row = np.array([(sid, name, gender, dept, gpa, att, status)], dtype=student_dtype)
    
    # Concatenate using numpy
    st.session_state.student_db = np.concatenate([db, new_row])
    return True, f"Student '{name}' successfully registered with ID {sid}!"

def lookup_student_record(target_id):
    db = st.session_state.student_db
    target_id = target_id.strip().upper()
    
    # Query using NumPy's np.where
    indices = np.where(db['student_id'] == target_id)[0]
    if len(indices) > 0:
        record = db[indices[0]]
        return {
            'student_id': record['student_id'],
            'name': record['name'],
            'gender': record['gender'],
            'department': record['department'],
            'gpa': float(record['gpa']),
            'attendance': int(record['attendance']),
            'status': record['status']
        }
    return None

# ── Code Generators ──────────────────────────────────────────────────────────
def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_code(data: str, fg_color: str, bg_color: str, box_size: int, border: int):
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
    return img.convert("RGBA")

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
    
    # 1. Decode with pyzbar
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

# ── SVG Avatars (WOW factor) ──────────────────────────────────────────────────
def get_avatar_svg_base64(gender: str):
    if gender == "Male":
        svg = """<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="20" fill="#1e1b4b"/>
            <circle cx="50" cy="38" r="18" fill="#818cf8"/>
            <path d="M22 80 C 22 62, 78 62, 78 80" stroke="#818cf8" stroke-width="8" stroke-linecap="round"/>
        </svg>"""
    elif gender == "Female":
        svg = """<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="20" fill="#311042"/>
            <circle cx="50" cy="38" r="18" fill="#f472b6"/>
            <path d="M22 80 C 22 62, 78 62, 78 80" stroke="#f472b6" stroke-width="8" stroke-linecap="round"/>
        </svg>"""
    else: # Other
        svg = """<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="20" fill="#111827"/>
            <circle cx="50" cy="38" r="18" fill="#9ca3af"/>
            <path d="M22 80 C 22 62, 78 62, 78 80" stroke="#9ca3af" stroke-width="8" stroke-linecap="round"/>
        </svg>"""
    return base64.b64encode(svg.encode('utf-8')).decode('utf-8')

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🎓 Student ID Matrix</h1>
    <p>Enroll student profiles, generate secure ID codes, scan credentials, and track visual department stats.</p>
</div>
""", unsafe_allow_html=True)

# ── Navigation Menu ───────────────────────────────────────────────────────────
if option_menu:
    selected = option_menu(
        menu_title=None,
        options=["Student Registry", "Visual Analytics", "ID Card Generator", "Scan ID Portal"],
        icons=["people", "bar-chart-line", "credit-card", "qr-code-scan"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)", "border": "1px solid rgba(255,255,255,0.08)", "border-radius": "14px"},
            "icon": {"color": "#38bdf8", "font-size": "15px"}, 
            "nav-link": {"font-size": "13px", "text-align": "center", "margin":"0px", "color": "#9ca3af", "--hover-color": "rgba(255,255,255,0.06)", "font-weight": "500"},
            "nav-link-selected": {"background-color": "#38bdf8", "color": "#060814", "font-weight": "700"},
        }
    )
else:
    selected = st.radio("Navigate", ["Student Registry", "Visual Analytics", "ID Card Generator", "Scan ID Portal"], horizontal=True)


# ── TAB 1: Student Registry ───────────────────────────────────────────────────
if selected == "Student Registry":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>📂 Registered Student Registry (NumPy Storage)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Database is stored as a vector structured NumPy array. Data conversions use Pandas.</p>", unsafe_allow_html=True)
    
    db = st.session_state.student_db
    
    if len(db) == 0:
        st.info("No student records available. Register students below.")
    else:
        # Export database with Pandas (Bonus Requirement)
        df_export = pd.DataFrame(db)
        df_export['gpa'] = df_export['gpa'].astype(float)
        df_export['attendance'] = df_export['attendance'].astype(int)
        
        csv_bytes = df_export.to_csv(index=False).encode('utf-8')
        
        col_title, col_export = st.columns([2, 1])
        with col_export:
            st.download_button(
                label="📊 Export CSV (Pandas)",
                data=csv_bytes,
                file_name="registered_students.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        # Display students directory
        for row in db:
            status_class = "badge-status-active" if row['status'] == "Active" else ("badge-status-suspended" if row['status'] == "Suspended" else "badge-status-graduated")
            st.markdown(f"""
            <div class="glass-card-student">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span class="badge-id">{row['student_id']}</span>
                        <strong style="color:white; font-size:1.15rem; margin-left:8px;">{row['name']}</strong>
                    </div>
                    <span class="badge-status {status_class}">{row['status']}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-top:10px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px;">
                    <div style="font-size:0.88rem; color:rgba(255,255,255,0.7);">
                        <strong>Dept:</strong> {row['department']} &nbsp;|&nbsp; <strong>Gender:</strong> {row['gender']}
                    </div>
                    <div style="font-size:0.88rem; color:rgba(255,255,255,0.7);">
                        <strong>GPA:</strong> <span style="color:#38bdf8; font-weight:700;">{float(row['gpa']):.2f}</span> &nbsp;|&nbsp; 
                        <strong>Attendance:</strong> <span style="color:#10b981; font-weight:700;">{int(row['attendance'])}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Registration Form
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>➕ Enroll New Student</h3>", unsafe_allow_html=True)
    
    with st.form("enroll_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            enroll_id = st.text_input("Student ID (e.g. STU-1009)", placeholder="STU-1009")
            enroll_name = st.text_input("Full Name", placeholder="Jane Doe")
            enroll_gender = st.selectbox("Gender", ["Female", "Male", "Other"])
            enroll_dept = st.selectbox("Department", ["Computer Science", "Mechanical Eng", "Electrical Eng", "Civil Eng", "Physics", "Mathematics", "Bio-Chemistry"])
        with col2:
            enroll_gpa = st.number_input("Cumulative GPA (0.00 - 4.00)", min_value=0.00, max_value=4.00, value=3.00, step=0.01)
            enroll_att = st.slider("Attendance Rate (%)", 0, 100, 85)
            enroll_status = st.selectbox("Status", ["Active", "Graduated", "Suspended"])
            
        enroll_submit = st.form_submit_button("✨ Register Student to NumPy Array")
        
        if enroll_submit:
            success, msg = add_student_record(enroll_id, enroll_name, enroll_gender, enroll_dept, enroll_gpa, enroll_att, enroll_status)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
                
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 2: Visual Analytics ───────────────────────────────────────────────────
elif selected == "Visual Analytics":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>📈 Demographic & Academic Analytics (Matplotlib)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Visualizing student distributions and grades dynamically using Matplotlib styling.</p>", unsafe_allow_html=True)
    
    db = st.session_state.student_db
    
    if len(db) == 0:
        st.warning("No records in student array to visualize.")
    else:
        # Convert NumPy to Pandas DataFrame for aggregation
        df_anal = pd.DataFrame(db)
        df_anal['gpa'] = df_anal['gpa'].astype(float)
        df_anal['attendance'] = df_anal['attendance'].astype(int)
        
        # Style plots globally for dark UI
        plt.style.use('dark_background')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['text.color'] = '#f3f4f6'
        plt.rcParams['axes.labelcolor'] = '#9ca3af'
        plt.rcParams['xtick.color'] = '#9ca3af'
        plt.rcParams['ytick.color'] = '#9ca3af'
        
        # 1. GPA Chart
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:10px;'>📊 Average GPA by Department</h4>", unsafe_allow_html=True)
        
        gpa_stats = df_anal.groupby('department')['gpa'].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(6, 3.2))
        bars = ax1.bar(
            gpa_stats['department'], 
            gpa_stats['gpa'], 
            color=['#38bdf8', '#6366f1', '#a855f7', '#ec4899', '#10b981', '#f59e0b', '#3b82f6'][:len(gpa_stats)],
            edgecolor='#1e293b',
            width=0.55
        )
        ax1.set_ylabel('GPA Score', fontsize=9)
        ax1.set_ylim(0, 4.3)
        ax1.grid(axis='y', linestyle='--', alpha=0.15)
        plt.xticks(rotation=20, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        
        # Add labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, color='#f3f4f6')
                        
        plt.tight_layout()
        st.pyplot(fig1)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Split Charts (Pie Chart & Histogram)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:10px;'>Sector Split</h4>", unsafe_allow_html=True)
            
            dept_counts = df_anal['department'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(4, 4))
            wedges, texts, autotexts = ax2.pie(
                dept_counts, 
                labels=dept_counts.index, 
                autopct='%1.0f%%', 
                colors=['#6366f1', '#06b6d4', '#ec4899', '#10b981', '#eab308', '#a855f7'],
                wedgeprops=dict(width=0.4, edgecolor='#1e293b'), # Donut chart
                startangle=90
            )
            for text in texts:
                text.set_fontsize(8)
            for autotext in autotexts:
                autotext.set_fontsize(8)
                autotext.set_weight('bold')
            ax2.set_title('Students by Department', fontsize=10, weight='bold')
            plt.tight_layout()
            st.pyplot(fig2)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:10px;'>Attendance Density</h4>", unsafe_allow_html=True)
            
            fig3, ax3 = plt.subplots(figsize=(4, 4))
            ax3.hist(
                df_anal['attendance'], 
                bins=6, 
                color='#10b981', 
                edgecolor='#064e3b', 
                alpha=0.75,
                rwidth=0.85
            )
            ax3.set_xlabel('Attendance Rate (%)', fontsize=8)
            ax3.set_ylabel('Number of Students', fontsize=8)
            ax3.grid(axis='y', linestyle='--', alpha=0.15)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            ax3.set_title('Attendance Spread', fontsize=10, weight='bold')
            plt.tight_layout()
            st.pyplot(fig3)
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 3: ID Card Generator ──────────────────────────────────────────────────
elif selected == "ID Card Generator":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>🎨 Generate Student Scannable Codes</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Choose a student record to generate scannable QR Codes or 1D Barcodes encoding their ID.</p>", unsafe_allow_html=True)
    
    db = st.session_state.student_db
    
    if len(db) == 0:
        st.warning("Registry is empty. Register students under the Student Registry tab first.")
    else:
        student_list = [f"{row['student_id']} - {row['name']} ({row['department']})" for row in db]
        selected_student = st.selectbox("Select Student Record", student_list)
        
        target_id = selected_student.split(" - ")[0]
        student = lookup_student_record(target_id)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            code_type = st.radio("Code Layout", ["QR Code", "1D Barcode (Code 128)"])
            fg_color = st.color_picker("Foreground Color", "#ffffff")
            bg_color = st.color_picker("Background Color", "#0d1127")
            
            if code_type == "QR Code":
                box_size = st.slider("Pixel Density", 8, 20, 12)
                border_size = st.slider("Quiet Border size", 1, 6, 3)
                
        with col2:
            st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
            
            if code_type == "QR Code":
                code_img = generate_qr_code(
                    data=student['student_id'],
                    fg_color=fg_color,
                    bg_color=bg_color,
                    box_size=box_size,
                    border=border_size
                )
            else:
                code_img = generate_barcode_img(
                    data=student['student_id'],
                    fg_color=fg_color,
                    bg_color=bg_color
                )
                
            st.image(code_img, width=240)
            
            # Pixel analysis using NumPy
            img_arr = np.array(code_img.convert("L"))
            dark_ratio = float(np.mean(img_arr < 128) * 100)
            
            st.markdown(f"""
            <div style="margin-top:0.6rem; font-size:0.8rem; color:rgba(255,255,255,0.4);">
                <strong>Dimensions:</strong> {code_img.size[0]}×{code_img.size[1]} px &nbsp;|&nbsp; 
                <strong>Dark Fill:</strong> {dark_ratio:.1f}%
            </div>
            """, unsafe_allow_html=True)
            
            # Download trigger
            buf = io.BytesIO()
            code_img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label=f"⬇ Download ID Code (PNG)",
                data=img_bytes,
                file_name=f"{student['student_id']}_{code_type.replace(' ', '_').lower()}.png",
                mime="image/png"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 4: Scan ID Portal ─────────────────────────────────────────────────────
elif selected == "Scan ID Portal":
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3>🔍 Validate Student Credentials</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.55); font-size:0.9rem; margin-top:-0.5rem;'>Verify Student ID Cards via webcam scans or uploaded code images.</p>", unsafe_allow_html=True)
    
    scan_method = st.radio("Scanning Source", ["Simulated Quick Scan", "Webcam Scanner (OpenCV)", "Upload Image"], horizontal=True)
    
    scanned_id = None
    code_type = None
    
    if scan_method == "Simulated Quick Scan":
        db = st.session_state.student_db
        if len(db) == 0:
            st.warning("Database is empty. Add students first.")
        else:
            scenarios = ["-- Select Scan Case --"]
            for row in db:
                scenarios.append(f"Scanned Valid Card: {row['student_id']}")
            scenarios.extend(["Scanned Invalid Card: STU-9999", "Scanned Invalid Card: STU-ERR55", "Custom ID Input"])
            
            choice = st.selectbox("Select Simulated Scenario", scenarios)
            if "Scanned Valid Card" in choice:
                scanned_id = choice.split(": ")[1]
                code_type = "QRCODE"
            elif "Scanned Invalid Card" in choice:
                scanned_id = choice.split(": ")[1]
                code_type = "QRCODE"
            elif choice == "Custom ID Input":
                custom = st.text_input("Enter Student ID String", placeholder="STU-1001")
                if custom:
                    scanned_id = custom
                    code_type = "CUSTOM"
                    
    elif scan_method == "Upload Image":
        upload = st.file_uploader("Upload QR code or Barcode Image", type=["png", "jpg", "jpeg"])
        if upload is not None:
            image = Image.open(upload)
            st.image(image, width=200, caption="Uploaded Image File")
            with st.spinner("Decoding image..."):
                scanned_id, code_type = decode_code_image(image)
                if not scanned_id:
                    st.error("❌ Decoded failed. Check the focus or crop of your image file.")
                    
    elif scan_method == "Webcam Scanner (OpenCV)":
        capture = st.camera_input("Snap ID Code")
        if capture is not None:
            image = Image.open(capture)
            with st.spinner("Decoding camera snapshot..."):
                scanned_id, code_type = decode_code_image(image)
                if not scanned_id:
                    st.error("❌ Scanner failed to isolate code. Hold card steady, flat, and centered.")
                    
    # ── Process Result ──
    if scanned_id:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:rgba(255,255,255,0.4); font-size:0.85rem;'>Decoded Data: <code>{scanned_id}</code> (Format: <code>{code_type}</code>)</p>", unsafe_allow_html=True)
        
        # Search using NumPy
        student = lookup_student_record(scanned_id)
        
        if student:
            # Display Student ID Card
            status_class = "badge-status-active" if student['status'] == "Active" else ("badge-status-suspended" if student['status'] == "Suspended" else "badge-status-graduated")
            avatar_b64 = get_avatar_svg_base64(student['gender'])
            
            st.markdown(f"""
            <div class="student-id-card">
                <div class="id-card-header">
                    <span class="id-card-title">STUDENT IDENTIFICATION CARD</span>
                    <span class="badge-status {status_class}">{student['status']}</span>
                </div>
                <div class="id-card-body">
                    <div class="id-card-avatar">
                        <img src="data:image/svg+xml;base64,{avatar_b64}" width="100" height="100"/>
                    </div>
                    <div class="id-card-info">
                        <div class="id-card-name">{student['name']}</div>
                        <div style="font-size:0.92rem; color:rgba(255,255,255,0.7); margin-bottom:6px;">
                            <strong>ID Number:</strong> <span style="font-family:monospace; color:#38bdf8; font-weight:700;">{student['student_id']}</span>
                        </div>
                        <div style="font-size:0.92rem; color:rgba(255,255,255,0.7); margin-bottom:6px;">
                            <strong>Major Dept:</strong> {student['department']}
                        </div>
                        <div style="font-size:0.92rem; color:rgba(255,255,255,0.7);">
                            <strong>CGPA score:</strong> <span style="color:#38bdf8; font-weight:700;">{student['gpa']:.2f}</span> &nbsp;|&nbsp; 
                            <strong>Attendance:</strong> <span style="color:#10b981; font-weight:700;">{student['attendance']}%</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Handle invalid IDs gracefully
            st.markdown(f"""
            <div class="invalid-id-card">
                <span class="badge-status" style="background:rgba(239,68,68,0.15); border-width:1px; border-style:solid; border-color:#f87171; color:#f87171;">✗ UNVERIFIED CREDENTIALS</span>
                <h3 style="margin-top: 8px; color: white;">Student ID: {scanned_id}</h3>
                <p style="color: rgba(255,255,255,0.75); font-size: 0.9rem; line-height: 1.5; margin-bottom:0;">
                    The scanned credentials decode to <strong>"{scanned_id}"</strong>, which does not exist in the NumPy registry. 
                    Verify the student credentials under the <strong>Student Registry</strong> tab or scan another card.
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;color:rgba(255,255,255,0.25);font-size:0.8rem;">
    Built with ♥ using NumPy, Pandas, Matplotlib, OpenCV &amp; Streamlit · Wrench Wise
</div>
""", unsafe_allow_html=True)
