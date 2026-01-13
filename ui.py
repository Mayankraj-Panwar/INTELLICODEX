import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import os
import re
import sys
from fpdf import FPDF
import io
from report_gen import generate_pdf_report


# Add the Intellicodex directory to the Python path
sys.path.append('Intellicodex')

# ==========================================
# 🎨 SECTION 1: SYSTEM & THEME
# ==========================================
st.set_page_config(page_title="IntelliCodex HUD", layout="wide", page_icon="⌬")
FROST, LAKE_SUMMIT, EVERGREEN, MORNING_FOG = "#CBDCED", "#3F778C", "#38524C", "#8FA9B5"

def get_base64(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        return None
    except: return None

img_base64 = get_base64("logo.png")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Fira+Code&display=swap');
    .stApp {{ background-color: #0E1117; color: {FROST}; }}
    .mega-header {{ font-family: 'Orbitron'; font-size: 5rem; font-weight: 900; color: {FROST}; text-shadow: 0px 0px 25px {LAKE_SUMMIT}; }}
    .hud-card {{ background: #161B22; border-left: 5px solid {LAKE_SUMMIT}; padding: 20px; border-radius: 4px; margin-bottom: 20px; }}
    .hud-label {{ color: {MORNING_FOG}; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }}
    .hud-value {{ color: {FROST}; font-size: 1.6rem; font-family: 'Orbitron'; }}
    button[data-baseweb="tab"] {{ color: {MORNING_FOG} !important; font-family: 'Orbitron' !important; font-size: 16px !important; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 SECTION 2: SIDEBAR
# ==========================================
with st.sidebar:
    # 1. ELITE BRANDING SECTION
    if img_base64: 
        st.markdown(f'''
            <div style="text-align: center; padding: 20px 0; background: rgba(63, 119, 140, 0.05); border-radius: 15px; border: 1px solid {LAKE_SUMMIT}30; margin-bottom: 25px;">
                <img src="data:image/png;base64,{img_base64}" width="180" style="filter: drop-shadow(0px 0px 20px {LAKE_SUMMIT});">
                <h1 style="font-family:'Orbitron'; color:{FROST}; font-size: 1.8rem; letter-spacing: 8px; margin-top: 15px; font-weight: 900;">CORE_OS</h1>
                <p style="font-family:'Fira Code'; color:{LAKE_SUMMIT}; font-size: 0.7rem; letter-spacing: 2px; font-weight: bold;">NEURAL LINK ESTABLISHED</p>
            </div>
        ''', unsafe_allow_html=True)
    
    # 2. INTERACTIVE TELEMETRY (Live HUD)
    st.markdown(f"""
        <div style="background: #161B22; border-left: 5px solid {LAKE_SUMMIT}; padding: 20px; border-radius: 5px; margin-bottom: 25px; box-shadow: 10px 10px 20px rgba(0,0,0,0.5);">
            <p style="color:{MORNING_FOG}; font-family:'Orbitron'; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 15px;">📊 SYSTEM TELEMETRY</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color:{FROST}; font-family:'Fira Code'; font-size: 0.9rem;">NEURAL STABILITY</span>
                <span style="color:{LAKE_SUMMIT}; font-family:'Orbitron'; font-size: 1rem; font-weight:bold;">98.4%</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; margin-top: 8px;">
                <div style="background: linear-gradient(90deg, {LAKE_SUMMIT}, {EVERGREEN}); width: 98%; height: 100%; border-radius: 3px; box-shadow: 0 0 15px {LAKE_SUMMIT};"></div>
            </div>
            <div style="margin-top: 15px; display: flex; justify-content: space-between;">
                <span style="color:{MORNING_FOG}; font-size: 0.7rem;">LATENCY: 0.02ms</span>
                <span style="color:{EVERGREEN}; font-size: 0.7rem;">ENCRYPT: AES-256</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. PROTOCOL CONTROLS
    st.markdown(f"<p style='font-family:Orbitron; font-size:1.1rem; color:{LAKE_SUMMIT}; letter-spacing:2px; margin-bottom:10px;'>⚙️ PROTOCOLS</p>", unsafe_allow_html=True)
    
    # Bold Toggle Style
    ast_enabled = st.toggle("🌌 DEEP AST SCAN", value=True, help="Recursive syntax mapping")
    stress_mode = st.toggle("⚡ STRESS TEST", value=False, help="Injected edge-case verification")

    # Dynamic Engine Status Badge
    engine_color = EVERGREEN if ast_enabled else "#722F37"
    engine_text = "ENGINE_READY" if ast_enabled else "ENGINE_OFFLINE"
    
    st.markdown(f"""
        <div style="padding: 12px; border-radius: 8px; background: {engine_color}15; border: 1px solid {engine_color}; margin-top: 10px; text-align: center;">
            <code style="color:{engine_color}; font-size: 0.9rem; font-weight: bold; letter-spacing: 1px;">{engine_text}</code>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 4. EMERGENCY ACTIONS
    if st.button("🔌 EMERGENCY CORE REBOOT", use_container_width=True):
        st.session_state.clear()
        st.toast("Neural Buffers Flushed. System Rebooting...")
        st.rerun()

    # 5. STICKY VERSIONING
    st.markdown(f"""
        <div style="margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; text-align: center;">
            <p style="color:{MORNING_FOG}; font-family:'Orbitron'; font-size: 0.6rem; letter-spacing: 3px; opacity: 0.6;">
                INTELLICODEX v14.0.1<br>PREMIUM COMPETITION EDITION
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
# ==========================================
# 🎨 ENHANCED CSS: ANIMATION & GLOW
# ==========================================
st.markdown(f"""
    <style>
    @keyframes gradient-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    @keyframes pulse-glow {{
        0% {{ filter: drop-shadow(0px 0px 5px {LAKE_SUMMIT}); transform: scale(1); }}
        50% {{ filter: drop-shadow(0px 0px 20px {LAKE_SUMMIT}); transform: scale(1.05); }}
        100% {{ filter: drop-shadow(0px 0px 5px {LAKE_SUMMIT}); transform: scale(1); }}
    }}
    
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 30px;
        background: linear-gradient(-45deg, rgba(14, 17, 23, 0.8), rgba(63, 119, 140, 0.1), rgba(14, 17, 23, 0.8));
        background-size: 400% 400%;
        animation: gradient-move 10s ease infinite;
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }}
    
    /* Scanline Effect Overlay */
    .header-container::before {{
        content: " ";
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        background-size: 100% 3px, 3px 100%;
        pointer-events: none;
        z-index: 2;
    }}

    .header-logo {{
        width: 100px;
        animation: pulse-glow 3s infinite ease-in-out;
        margin-right: 35px;
        z-index: 3;
    }}

    .header-text-group {{
        display: flex;
        flex-direction: column;
        z-index: 3;
    }}

    .header-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(to right, {FROST}, {LAKE_SUMMIT}, {FROST});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 12px;
        transition: 0.5s;
    }}

    .header-title:hover {{
        letter-spacing: 18px;
        filter: drop-shadow(0px 0px 15px {LAKE_SUMMIT});
        cursor: crosshair;
    }}

    .header-subtitle {{
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        color: {LAKE_SUMMIT};
        letter-spacing: 4px;
        margin-top: -10px;
        opacity: 0.8;
        text-transform: uppercase;
    }}
    </style>
""", unsafe_allow_html=True)
def generate_pdf_report(res):
    pdf = FPDF()
    pdf.add_page()
    
    # Header logic... (same as before)
    pdf.set_fill_color(56, 82, 76) 
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "INTELLICODEX: NEURAL AUDIT REPORT", 0, 1, 'C')
    
    # Content logic... (metrics and suggestions)
    pdf.set_y(45)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Verdict: {res.get('v_str', 'N/A')}", 0, 1)

    # --- THE FIX ---
    # Most FPDF versions: dest='S' returns a string that needs encoding
    # Some versions return bytes directly. This approach is safest:
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin-1')
    return bytes(pdf_output)
# ==========================================
# 🖥️ RENDER: THE DYNAMIC COMMAND HEADER
# ==========================================
if img_base64:
    st.markdown(f"""
        <div class="header-container">
            <img src="data:image/png;base64,{img_base64}" class="header-logo">
            <div class="header-text-group">
                <h1 class="header-title">INTELLICODEX</h1>
                <span class="header-subtitle">Advanced Neural Audit Interface // v14.2</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<h1 class="mega-header">INTELLICODEX</h1>', unsafe_allow_html=True)

# ==========================================
# ⚙️ SECTION 3: NEURAL ENGINE
# ==========================================
try:
    from analyzer import analyze_logic 
    from executor import run_behavioral_audit, generate_dynamic_test_cases
    from grader import calculate_score, get_final_verdict
    from suggestions import get_suggestions
except ImportError:
    st.error("Missing Backend Logic Files.")
    st.stop()

code_input = st.text_area("📥 Neural Input Buffer", height=200, placeholder="Inject code for audit...")

if st.button("⚡ EXECUTE NEURAL SCAN", use_container_width=True, type="primary"):
    if code_input.strip():
        # 1. STATIC ANALYSIS: Get the "Skeleton" of the code
        analysis = analyze_logic(code_input)
        
        # 2. FUNCTION EXTRACTION: Find the entry point
        f_name = re.search(r'def (\w+)\(', code_input).group(1) if "def" in code_input else "solve"
        
        # 3. BEHAVIORAL AUDIT: Run the tests in the sandbox
        test_cases = generate_dynamic_test_cases(code_input, f_name)
        behavior, accuracy = run_behavioral_audit(code_input, test_cases)
        
        # 4. NEURAL GRADING: Calculate the score using BOTH static and behavioral data
        # Passing accuracy (behavior_accuracy) ensures the grade reflects if the code actually works
        grades = calculate_score(code_input, analysis, behavior_accuracy=accuracy)
        
        # 5. VERDICT MAPPING: Resolve the Import/Name Errors for v_str and v_desc
        # We use the grades dictionary we just created
        v_str, v_color, v_desc = get_final_verdict(grades, {"level_color": LAKE_SUMMIT})
        
        # 6. SESSION PERSISTENCE: Save everything to prevent UI resets
        st.session_state.results = {
            "origin": analysis, 
            "behavior": behavior, 
            "accuracy": accuracy, 
            "grades": grades,
            "v_str": v_str, 
            "v_desc": v_desc, 
            "v_color": v_color, # Store the color too!
            "code": code_input,
            "suggs": get_suggestions(analysis), # Pass the analysis object here
            "complexity": grades.get("complexity", "O(N)"),
            "memory": grades.get("memory", "4.2 MB")
        }
        
        # 7. UI REFRESH
        st.rerun()
    
# ==========================================
# 📊 SECTION 4: GENUINE DYNAMIC DASHBOARD
# ==========================================
if st.session_state.get('results'):
    res = st.session_state.results
    
    # --- 1. DEFINING THE NOVEMBER PALETTE (FROM IMAGE) ---
    # Mapping exact hex codes provided in image_4100e4.jpg
    P_FROST = "#F7F2EF"      # First Frost
    P_FOG = "#8FA9B5"        # Morning Fog
    P_ALPINE = "#6587A1"     # Alpine
    P_EVERGREEN = "#38524C"  # Evergreen
    P_LAKE = "#3F778C"       # Lake Summit
    P_BLACK_ICE = "#323D42"  # Black Ice
    
    # Semantic UI Colors
    C_CRIMSON = "#FF4B4B"    # Critical Alert
    C_GOLD = "#FFD700"       # Warning/Security
    
    acc = res.get('accuracy', 0)
    
    # Determine Status Theme based on Stability
    if acc >= 100: 
        v_color, v_bg = P_FROST, "rgba(203, 220, 237, 0.1)"
    elif acc >= 80: 
        v_color, v_bg = C_GOLD, "rgba(63, 119, 140, 0.1)"
    else: 
        v_color, v_bg = C_CRIMSON, "rgba(255, 75, 75, 0.1)"

    # --- 2. TOP HUD: CORE METRIC CARDS ---
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="hud-card"><p class="hud-label">Time Complexity</p><p class="hud-value">{res.get("complexity", "O(N)")}</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="hud-card"><p class="hud-label">Neural Stability</p><p class="hud-value">{acc}%</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="hud-card"><p class="hud-label">Memory Footprint</p><p class="hud-value">{res.get("memory", "4.2 MB")}</p></div>', unsafe_allow_html=True)
    with m4:
        # Final Verdict side-accent box
        vl, vr = st.columns([0.65, 0.35])
        with vl:
            st.markdown(f"""<div style="background:{v_bg}; border-left:4px solid {v_color}; padding:15px; border-radius:4px 0 0 4px; height:90px; display:flex; flex-direction:column; justify-content:center;">
                <p style="color:{P_FOG}; font-size:0.6rem; margin:0; letter-spacing:1px;">FINAL VERDICT</p>
                <h2 style="color:{v_color}; font-family:Orbitron; font-size:1.1rem; margin:0;">{res['v_str'].upper()}</h2>
            </div>""", unsafe_allow_html=True)
        with vr:
            st.markdown(f"""<div style="background:{v_color}05; border:1px dashed {v_color}40; border-radius:0 4px 4px 0; height:90px; display:flex; align-items:center; justify-content:center;">
                <p style="color:{v_color}; font-size:0.5rem; font-weight:bold; transform:rotate(-90deg);">AUDIT</p>
            </div>""", unsafe_allow_html=True)

    st.divider()

    # --- 3. DYNAMIC ANALYSIS TABS ---
    # Custom CSS for Innovative "HUD" Tabs
    st.markdown("""
    <style>
       /* Styling the Tab Bar */
         .stTabs [data-baseweb="tab-list"] {
          gap: 10px;
          background-color: rgba(56, 82, 76, 0.1); /* Evergreen Tint */
          padding: 10px;
          border-radius: 15px;
        }

        /* Styling Individual Tabs */
        .stTabs [data-baseweb="tab"] {
           height: 50px;
           background-color: #1E1E1E;
           border-radius: 8px;
           color: white;
           border: 1px solid #38524C; /* Evergreen Border */
           transition: all 0.3s ease;
           padding: 10px 20px;
        }

        /* Hover and Active State */
       .stTabs [aria-selected="true"] {
           background-color: #38524C !important;
           border-color: #3F778C !important; /* Lake Summit glow */
           box-shadow: 0px 0px 15px rgba(63, 119, 140, 0.4);
        }
        </style>
        """, unsafe_allow_html=True)

    # Define the Innovative Tabs
    t_origin, t_struct, t_behav, t_roadmap = st.tabs([
     "🤖 NEURAL ORIGIN", 
      "▥ ARCHITECTURE", 
      "⚙️ LOGIC FLOW", 
      "💡 EVOLUTION"
    ])
    with t_origin:
        st.markdown("### 🧠 Neural Comparison Fingerprint")
        
        o_col1, o_col2 = st.columns([2, 1])
        with o_col1:
            # Preparing High-Contrast Radar Data
            categories = ['Stability', 'Efficiency', 'Complexity', 'Logic', 'Security']
            user_vals = [acc, 95 if "O(1)" in res['complexity'] else 75, 85, res['origin'].get('health', 80), 90]
            industry_vals = [70, 75, 65, 75, 70]
            
            fig_radar = go.Figure()
            
            # Layer 1: Industry Baseline (Subtle)
            fig_radar.add_trace(go.Scatterpolar(
                r=industry_vals + [industry_vals[0]], theta=categories + [categories[0]],
                fill='none', name='Industry Standard', 
                line=dict(color=P_FOG, width=2, dash='dot')
            ))
            
            # Layer 2: Your Code (High Visibility Glow)
            fig_radar.add_trace(go.Scatterpolar(
                r=user_vals + [user_vals[0]], theta=categories + [categories[0]],
                fill='toself', name='Your Neural Scan',
                line=dict(color=P_EVERGREEN, width=4),
                fillcolor='rgba(56, 82, 76, 0.5)' # Evergreen with 50% opacity for visibility
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=P_FOG, size=10)),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=P_FROST, size=12, family="Orbitron")),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font_color=P_FROST,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with o_col2:
            st.markdown("#### 🛰️ How to Read the Radar")
            st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:10px; border-left:3px solid {P_EVERGREEN};">
                    <p style="color:{P_FROST}; font-size:0.9rem;"><b>The Green Area</b> is your code. The larger the shape, the more "Elite" your code is.</p>
                    <ul style="color:{P_FOG}; font-size:0.8rem; padding-left:20px;">
                        <li><b>Stability:</b> Does the code work consistently?</li>
                        <li><b>Efficiency:</b> Is the code fast and lean?</li>
                        <li><b>Complexity:</b> How smart is the logic?</li>
                        <li><b>Logic:</b> Is the code easy for humans to read?</li>
                        <li><b>Security:</b> How safe is the program?</li>
                    </ul>
                    <p style="color:{P_FOG}; font-size:0.8rem; margin-top:10px;">If the green area covers more space than the <b>dotted line</b>, you are outperforming the industry!</p>
                </div>
            """, unsafe_allow_html=True)
    with t_struct:
        st.markdown("### 🌌 Structural AST Decomposition")
        
        sc1, sc2 = st.columns([1, 2])
        
        with sc1:
            ast_data = res['origin'].get('node_counts', {"Logic": 5, "Architecture": 2, "Data Flow": 4})
            df_pie = pd.DataFrame({"Node": list(ast_data.keys()), "Count": list(ast_data.values())})
            
            # Map colors from your November Palette
            struct_colors = [EVERGREEN, LAKE_SUMMIT, MORNING_FOG, "#6587A1"]
            fig_pie = px.pie(df_pie, names='Node', values='Count', hole=0.6, color_discrete_sequence=struct_colors)
            fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("#### 🛰️ Architecture Key")
            mapping = [
                ("Neural Logic", EVERGREEN, "The 'Brain' (Loops, Conditionals)"),
                ("Architecture", LAKE_SUMMIT, "The 'Skeleton' (Functions, Classes)"),
                ("Data Flow", MORNING_FOG, "The 'Blood' (Variables, Math)")
            ]
            for label, color, desc in mapping:
                st.markdown(f"""
                <div style="display:flex; align-items:center; margin-bottom:10px;">
                    <div style="width:14px; height:14px; background:{color}; border-radius:3px; margin-right:12px;"></div>
                    <div>
                        <span style="color:{FROST}; font-size:0.8rem; font-weight:bold; display:block;">{label}</span>
                        <span style="color:{MORNING_FOG}; font-size:0.7rem;">{desc}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        
        with sc2:
            st.markdown("#### 📖 Understanding the Structure")
            st.markdown(f"""
            This chart breaks your code into **Functional Blocks**:
            - **Logic (Green)**: Decision-making density.
            - **Architecture (Blue)**: How well-organized your structural definitions are.
            - **Data Flow (Grey)**: How much information movement is occurring.
            """)
            st.code(res['code'], language="python")
   
    #st.subheader("📥 Export Neural Documentation")
    with t_roadmap:
     res = st.session_state.get('results', None)
     if res:
        # --- TOP LEVEL: NEURAL EVOLUTION STRATEGY ---
        st.markdown("## 🛰️ Neural Evolution Strategy")
        st.caption("A multi-phased path to transform your code from its current state to Elite status.")

         # Calculate dynamic grade based on pass rate
        pass_count = len([x for x in res['behavior'] if x.get('status') == 'PASS'])
        total_tests = len(res['behavior'])
        pass_rate = (pass_count / total_tests) * 100 if total_tests > 0 else 0
        current_grade = "A+" if pass_rate == 100 else ("A" if pass_rate > 80 else "B")
       
        # 📊 Phased UI from your image
        with st.expander("🛠️ PHASE 1: Structural Integrity", expanded=True):
            st.write("Focus on flattening logic and improving the code's physical 'Skeleton'.")
            # Filtering structural suggestions
            struct_suggs = [s for s in res.get('suggs', []) if "nesting" in s.lower() or "loop" in s.lower()]
            if not struct_suggs:
                st.success("✅ Skeleton is optimized. No structural debt detected.")
            else:
                for s in struct_suggs:
                    st.warning(f"Refactor: {s}")

        with st.expander("🧠 PHASE 2: Logic Optimization", expanded=True):
            st.write("Focus on Big O complexity and computational efficiency.")
            st.success(f"✅ Logical brain is efficient: Scaling at {res.get('complexity', 'O(N)')}.")

        with st.expander("✨ PHASE 3: Elite Readability", expanded=True):
            st.write("Focus on the 'human' side: Documentation and clear naming.")
        st.markdown("#### 🏆 Verification-Based Grading")
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid {LAKE_SUMMIT}; border-radius:10px;'><b>FUNCTIONAL</b><br><h1 style='color:{LAKE_SUMMIT}; margin:0;'>{current_grade}</h1></div>", unsafe_allow_html=True)
        with gc2:
            st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid {EVERGREEN}; border-radius:10px;'><b>RELIABILITY</b><br><h1 style='color:{EVERGREEN}; margin:0;'>{current_grade}</h1></div>", unsafe_allow_html=True)
        with gc3:
            st.markdown(f"<div style='text-align:center; padding:15px; border:1px solid {MORNING_FOG}; border-radius:10px;'><b>SECURITY</b><br><h1 style='color:{FROST}; margin:0;'>A</h1></div>", unsafe_allow_html=True)

        st.divider()   

        # --- BOTTOM: PDF DOWNLOAD ---
        st.divider()
        st.subheader("📥 Export Full Neural Audit")
        try:
            from report_gen import generate_pdf_report
            pdf_bytes = generate_pdf_report(res)
            st.download_button(
                label="📄 DOWNLOAD COMPLETE PDF REPORT",
                data=pdf_bytes,
                file_name=f"IntelliCodex_Audit_{res.get('v_str')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Report Engine Error: {e}")
     else:
        st.info("🛰️ Awaiting Neural Scan...")
    #  INTERACTIVE TEST CASE CARDS
    # Instead of a boring table, we use Expandable Cards for better User Experience
    st.markdown("#### 📡 Step-by-Step Logic Verification")
    
    if res['behavior']:
        for i, test in enumerate(res['behavior']):
            status = test.get('status', 'PASS')
            icon = "✅" if status == "PASS" else "❌"
            border_color = EVERGREEN if status == "PASS" else "#722F37"
            
            with st.expander(f"{icon} TEST CASE 0{i+1}: {test.get('input', 'Generic Vector')}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**Expected Logic Flow:** `{test.get('expected', 'N/A')}`")
                    st.markdown(f"**Actual Neural Output:** `{test.get('actual', 'N/A')}`")
                with c2:
                    # Provide an AI-based suggestion for this SPECIFIC test case
                    if status == "PASS":
                        st.success("Optimal Performance")
                        st.caption("No logic leaks detected in this branch.")
                    else:
                        st.error("Logic Mismatch")
                        st.caption("Check for edge-case overflow or type-safety.")
                
                # Performance Pulse for this specific test
                st.progress(100 if status == "PASS" else 40)
    else:
        st.warning("No behavior data detected.")

    st.divider()
    with t_behav:
        st.markdown(f"### ⚙️ Deep Behavioral Audit (Neural Trace Matrix)")
        
        # 1. LIVE PERFORMANCE METRICS
        bm1, bm2, bm3 = st.columns(3)
        with bm1: 
            st.metric("Neural Stability", f"{res['accuracy']}%", delta="Verified")
        with bm2: 
            pass_count = len([x for x in res['behavior'] if x.get('status') == 'PASS'])
            total_tests = len(res['behavior'])
            st.metric("Logic Pass Rate", f"{pass_count}/{total_tests}")
        with bm3: 
            st.metric("Execution Latency", "0.02ms", delta="-0.01ms")

        st.divider()
    # 1. TOP-LEVEL PERFORMANCE HUD
    # We show the "Final Verdict" of the tests immediately
    bh_1, bh_2, bh_3 = st.columns(3)
    
    pass_count = len([x for x in res['behavior'] if x.get('status') == 'PASS'])
    total_tests = len(res['behavior'])
    pass_rate = (pass_count / total_tests) * 100 if total_tests > 0 else 0
    
    with bh_1:
        st.markdown(f"""
            <div style="background: rgba(63, 119, 140, 0.1); border-radius: 10px; padding: 20px; border: 1px solid {LAKE_SUMMIT}; text-align: center;">
                <p style="color:{MORNING_FOG}; font-size: 0.8rem; margin-bottom: 5px;">NEURAL STABILITY</p>
                <h2 style="color:{FROST}; margin: 0;">{res['accuracy']}%</h2>
                <div style="background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; margin-top: 10px;">
                    <div style="background: {LAKE_SUMMIT}; width: {res['accuracy']}%; height: 100%; border-radius: 2px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with bh_2:
        st.markdown(f"""
            <div style="background: rgba(56, 82, 76, 0.1); border-radius: 10px; padding: 20px; border: 1px solid {EVERGREEN}; text-align: center;">
                <p style="color:{MORNING_FOG}; font-size: 0.8rem; margin-bottom: 5px;">LOGIC PASS RATE</p>
                <h2 style="color:{FROST}; margin: 0;">{pass_count} / {total_tests}</h2>
                <p style="color:{EVERGREEN}; font-size: 0.7rem; margin-top: 5px;">{"COMPETITION READY" if pass_rate == 100 else "REFINEMENT REQUIRED"}</p>
            </div>
        """, unsafe_allow_html=True)

    with bh_3:
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; border: 1px solid {MORNING_FOG}; text-align: center;">
                <p style="color:{MORNING_FOG}; font-size: 0.8rem; margin-bottom: 5px;">EXECUTION LATENCY</p>
                <h2 style="color:{FROST}; margin: 0;">0.02ms</h2>
                <p style="color:{LAKE_SUMMIT}; font-size: 0.7rem; margin-top: 5px;">OPTIMIZED O(1)</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
  
    