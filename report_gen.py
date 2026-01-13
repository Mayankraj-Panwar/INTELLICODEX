from fpdf import FPDF

def generate_pdf_report(res):
    pdf = FPDF()
    pdf.add_page()
    
    # 🎨 HEADER - Evergreen Theme
    pdf.set_fill_color(56, 82, 76) 
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(15)
    pdf.cell(0, 10, "INTELLICODEX: ARCHITECTURAL AUDIT", 0, 1, 'C')
    
    # --- 1. ARCHITECTURAL GRADING ---
    pdf.set_y(50)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "SYSTEM ARCHITECTURAL GRADE", 0, 1)
    
    score = res.get('accuracy', 0)
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(10, 62, 190, 8, 'F')
    pdf.set_fill_color(56, 82, 76)
    pdf.rect(10, 62, (190 * (score/100)), 8, 'F')
    
    pdf.set_y(72)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"Verdict: {res.get('v_str')} | Integrity Score: {score}%", 0, 1)

    # --- 2. TECHNICAL METRICS (Graph Data) ---
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(63, 119, 140)
    pdf.cell(0, 10, "TECHNICAL PERFORMANCE METRICS", 0, 1)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"- Computational Complexity: {res.get('complexity', 'O(N)')}", 0, 1)
    
    # Pulling Radar Data node counts
    nodes = res.get('origin', {}).get('node_counts', {"Logic": 0, "Structure": 0, "Data": 0})
    for cat, val in nodes.items():
        pdf.cell(0, 7, f"- {cat} Node Count: {val}", 0, 1)

    # --- 3. EVOLUTION STRATEGY (Suggestions) ---
    pdf.ln(5)
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " NEURAL EVOLUTION ROADMAP", 0, 1, 'L', True)
    
    pdf.set_font("Arial", '', 10)
    suggs = res.get('suggs', ["Follow PEP8 and modularize logic."])
    for s in suggs:
        # Strip potential emojis to prevent font errors
        clean_s = str(s).encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 7, f"> {clean_s}")

    # --- 4. SOURCE CODE ARCHIVE ---
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "AUDITED SOURCE CODE SNAPSHOT", 0, 1)
    
    pdf.set_font("Courier", '', 8)
    pdf.set_fill_color(250, 250, 250)
    code_text = res.get('code', 'No code provided.')
    pdf.multi_cell(0, 4, code_text, border=1, fill=True)

    # Output handling
    pdf_out = pdf.output(dest='S')
    return pdf_out.encode('latin-1', 'ignore') if isinstance(pdf_out, str) else bytes(pdf_out)
