import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

def hex_to_rgba(hex_color, opacity=0.4):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{opacity})'

# Core Intelligence Modules
from analyzer import analyze_logic      # Layer 1
from executor import run_behavioral_audit # Layer 2
from style_detector import detect_level # Layer 3
from grader import calculate_score, get_final_verdict # Layer 4
from suggestions import get_suggestions
from report_gen import generate_pdf_report

# Page Setup
st.set_page_config(page_title="IntelliCodex Ultra", layout="wide", page_icon="🛡️")

# --- 1. FUTURISTIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .main { background-color: #0E1117; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    
    /* Input Area Styling */
    .stTextArea textarea { 
        background-color: #161B22 !important; 
        color: #00FF41 !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #30363D !important; 
    }
    
    /* Dynamic Verdict Box - Optimized */
    .verdict-box {
        color: white; 
        padding: 30px; 
        border-radius: 15px;
        text-align: center; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        transition: all 0.5s ease;
    }

    .title-text { 
        font-family: 'Orbitron', sans-serif; 
        font-size: 3rem; 
        color: #58A6FF; 
        text-align: center; 
        letter-spacing: 2px; 
        margin-bottom: 0; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR CORE ---
with st.sidebar:
    
    with st.sidebar:
        # Sirf image ko wrap karne ke liye columns ka use
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://img.icons8.com/nolan/512/artificial-intelligence.png", width=80)
    
    
    
    st.title("System Core")
    st.status("🟢 Engine Operational", expanded=False)
    st.markdown("---")
    st.subheader("Audit Settings")
    deep_scan = st.toggle("Deep AST Scan", value=True)
    sandbox_mode = st.toggle("Isolated Sandbox", value=True)
    st.divider()
    st.caption("Version 2.0 - 4-Layer Intelligence")

# --- 3. HEADER ---
st.markdown('<p class="title-text">INTELLICODEX</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8B949E; margin-bottom:30px;'>Multi-Layer AI Code Auditing & Decision System</p>", unsafe_allow_html=True)

col_code, col_report = st.columns([1, 1.3], gap="large")

with col_code:
    st.subheader("⌨️ Source Input")
    code_input = st.text_area("Input Python Script", height=550, placeholder="def solve(n):\n    # Your logic here...")
    
    if st.button("⚡START 4-LAYER AUDIT⚡", use_container_width=True, type="primary"):
        if code_input.strip():
            st.session_state.analyzed = True
        else:
            st.error("Sir Jii... Pehle code toh likho! 😂")

# --- 4. THE INTELLIGENCE ENGINE ---
if st.session_state.get('analyzed') and code_input:
    # --- LAYER 1: Structural Scan ---
    analysis = analyze_logic(code_input)
    
    # --- LAYER 3: Style & Origin Detection ---
    level_name, level_label, level_color = detect_level(code_input, analysis)
    
    # --- DYNAMIC TEST CASE GENERATOR ---
    import re
    match = re.search(r'def (\w+)\(', code_input)
    func_name = match.group(1) if match else "solve"

    # --- NEW: DYNAMIC TEST GENERATION ---
    from executor import generate_dynamic_test_cases
    test_cases = generate_dynamic_test_cases(code_input, func_name)

    # Agar dynamic generation fail ho jaye, toh purana template use karein
    if not test_cases:
        test_cases = [{"name": "Standard Test", "input": (10, 5), "expected": 15}]


    # --- LAYER 2: Behavioral Execution ---
    behavior_results, accuracy = run_behavioral_audit(code_input, test_cases)
    
    # --- LAYER 4: Decision & Verdict ---

    # 1. Base scores calculation
    grades = calculate_score(code_input, analysis)

    # 2. Accuracy Adjustment (Handling Test Case Mismatches)
    if accuracy == 0:
        try:
            compile(code_input, '<string>', 'exec')
            adj_accuracy = 50  # Syntax OK, Logic doubtful
        except:
            adj_accuracy = 0   # Syntax Error
    else:
        adj_accuracy = accuracy

    # 3. Final Score Calculation (Balanced Weights)
    final_total = int((adj_accuracy * 0.4) + (grades.get('efficiency', 100) * 0.4) + (grades.get('readability', 100) * 0.2))
    grades['total'] = final_total

    # 4. Traffic Signal Color Logic
    if final_total >= 80:
        v_color = "#00FF41" # Green (Elite)
    elif final_total >= 50:
        v_color = "#FF9800" # Orange (Modest)
    else:
        v_color = "#FF3333" # Red (Critical)

    # --- IMPORTANT FIX: Sync style_data with our new Traffic Color ---
    style_data = {
        "level_name": level_name,   # Level 3 se aaya naam (e.g., Elite)
        "level_color": v_color,     # MANUALLY OVERRIDDEN with Traffic Color ✅
        "level_label": level_label
    }

    # 5. Get Final Verdict Labels using updated style_data
    verdict, _, v_desc = get_final_verdict(grades, style_data)     

    with col_report:
        # --- VERDICT DISPLAY (Traffic Signal Style) ---
        # Yahan humne gradient ko v_color se start kiya hai taaki dynamic lage
        st.markdown(f"""
            <div class="verdict-box" style="
                border-left: 10px solid {v_color}; 
                background: linear-gradient(90deg, {v_color}44 0%, #161B22 100%);
                border-radius: 10px;
                padding: 25px;
                text-align: left;
                margin-bottom: 25px;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            ">
                <h1 style='margin:0; color: {v_color}; font-family: "Orbitron"; font-size: 2.2rem;'>{verdict}</h1>
                <p style='font-size: 18px; color: #E0E0E0; margin-top: 5px; font-weight: 500;'>{v_desc}</p>
            </div>
            """, unsafe_allow_html=True)

        # --- VISUAL DASHBOARD ---
        t1, t2 = st.columns(2)
        with t1:
            # Gauge Chart - Fully Synced with v_color
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", 
                value = grades['total'],
                title = {'text': "OVERALL HEALTH", 'font': {'size': 18, 'color': '#8B949E', 'family': 'Orbitron'}},
                gauge = {
                    'bar': {'color': v_color}, # Main bar color synced ✅
                    'bgcolor': "#161B22", 
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'steps': [
                        # Background steps ko thoda dark rakhenge taaki main bar chamke
                        {'range': [0, 100], 'color': hex_to_rgba(v_color, opacity=0.1)} 
                    ],
                }
            ))
            fig_gauge.update_layout(
                height=280, 
                margin=dict(l=20, r=20, t=50, b=20), 
                paper_bgcolor='rgba(0,0,0,0)', 
                font={'color': v_color, 'family': 'Orbitron'} # Number color also synced ✅
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with t2:
            # Radar Chart - Fixed Transparency Error
            fig_radar = go.Figure()
            
            # Convert hex to rgba for the fill
            v_rgba = hex_to_rgba(v_color, opacity=0.4) 
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[analysis.get('health', 0), accuracy, analysis.get('human_probability', 0), grades['total']],
                theta=['Structural', 'Behavioral', 'Origin', 'Decision'],
                fill='toself', 
                line_color=v_color, 
                fillcolor=v_rgba  # AB YE ERROR NAHI DEGA ✅
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(22, 27, 34, 0.5)", 
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#30363D", showticklabels=False),
                    angularaxis=dict(gridcolor="#30363D", linecolor="white")
                ),
                showlegend=False, 
                height=280, 
                margin=dict(l=40, r=40, t=40, b=40), 
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # --- NAYA COMPLEXITY STRIP ---
        st.markdown(f"""
            <div style="background-color: #161B22; padding: 10px; border-radius: 10px; border-left: 5px solid {level_color}; margin-bottom: 20px; text-align: center;">
                <span style="color: #8B949E; font-size: 16px;">System Estimation: </span>
                <span style="color: {level_color}; font-size: 20px; font-weight: bold; font-family: 'Orbitron';">
                    Estimated Time Complexity: {analysis.get('big_o', 'O(1)')}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # --- LAYER TABS ---
        tab1, tab2, tab3, tab4 = st.tabs(["🔗 Structural", "⚙️ Behavioral", "🤔 Style/Origin", "💡 Suggestions"])
        
        with tab1:
            st.markdown(f"### Code Architecture: **{analysis.get('complexity_label')}**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Nesting Level", f"{analysis.get('max_nesting', 0)}")
            c2.metric("Dead Code", analysis.get('dead_code', 0))
            c3.metric("Total Funcs", analysis.get('functions', 0))
            for issue in analysis.get('issues', []):
                st.warning(issue)

        with tab2:
            st.markdown(f"### Execution Accuracy: **{accuracy}%**")
            
            if behavior_results:
                # --- FIX: Convert large outputs to strings to avoid OverflowError ---
                safe_results = []
                for res in behavior_results:
                    safe_res = res.copy()
                    # Output ko string bana do taaki Pandas crash na ho
                    safe_res['output'] = str(res.get('output', 'N/A'))
                    safe_results.append(safe_res)
                
                # Ab Safe results ka DataFrame banayein
                res_df = pd.DataFrame(safe_results)
                
                # Columns ensure karein
                for col in ['scenario', 'verdict', 'runtime', 'output']:
                    if col not in res_df.columns:
                        res_df[col] = "N/A"
                
                st.dataframe(res_df[['scenario', 'verdict', 'runtime', 'output']], use_container_width=True)
            else:
                st.info("No execution results available for this code.")
        
        with tab3:
            st.markdown("### AI Origin Probability")
            ai_p = analysis.get('ai_probability', 0)
            hu_p = analysis.get('human_probability', 0)
            
            c_hu, c_ai = st.columns([hu_p+1, ai_p+1])
            c_hu.markdown(f"<div style='background:#1E88E5; padding:10px; text-align:center; border-radius:5px;'>Human {hu_p}%</div>", unsafe_allow_html=True)
            c_ai.markdown(f"<div style='background:#E53935; padding:10px; text-align:center; border-radius:5px;'>AI {ai_p}%</div>", unsafe_allow_html=True)
            
            st.write("#### Indicators:")
            for reason in analysis.get('origin_reasons', []):
                st.write(f"- 🚩 {reason}")

        with tab4:
            st.markdown("### Performance Refactoring Suggestions")
            suggs = get_suggestions(code_input)
            for s in suggs:
                st.success(f"💡 {s}")
                
        with st.sidebar:
            st.divider()
            st.subheader("📄 Export Results")
            
            # Report ke liye data ready karein
            if st.session_state.get('analyzed'):
                try:
                    from suggestions import get_suggestions
                    suggs = get_suggestions(code_input) 
                    
                    # PDF generate as bytes
                    pdf_output = generate_pdf_report(
                        analysis, 
                        grades, 
                        verdict, 
                        code_input, 
                        behavior_results,
                        suggs
                    )
                    
                    st.download_button(
                        label="📥 Download Full Audit Report",
                        data=pdf_output,
                        file_name=f"IntelliCodex_Report_{verdict}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Report generation failed: {e}")

else:
    with col_report:
        st.markdown("""
            <div style="border: 2px dashed #30363D; padding: 120px; text-align: center; border-radius: 20px; margin-top: 50px;">
                <h2 style="color: #8B949E; font-family: 'Orbitron';">AWAITING NEURAL INPUT</h2>
                <p style="color: #58A6FF;">System ready for 4-layer intelligence audit.</p>
            </div>
            """, unsafe_allow_html=True)