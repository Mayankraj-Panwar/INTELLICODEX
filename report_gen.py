from fpdf import FPDF
import datetime

class CodexReport(FPDF):
    def header(self):
        # Orbitron jaisa feel dene ke liye Arial Bold
        self.set_font('Arial', 'B', 15)
        self.set_text_color(88, 166, 255) # Light Blue color
        self.cell(0, 10, 'INTELLICODEX ULTRA - AUDIT REPORT', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, f" {label}", 0, 1, 'L', fill=True)
        self.ln(4)

def generate_pdf_report(analysis, grades, verdict, code, behavior_results, suggestions):
    pdf = CodexReport()
    pdf.add_page()
    
    # --- 1. EXECUTIVE SUMMARY ---
    pdf.chapter_title('1. EXECUTIVE SUMMARY')
    pdf.set_font('Arial', 'B', 14)
    # Verdict color coding
    if verdict == "ELITE": pdf.set_text_color(0, 150, 0)
    elif verdict == "MODEST": pdf.set_text_color(255, 140, 0)
    else: pdf.set_text_color(200, 0, 0)
    
    pdf.cell(0, 10, f"VERDICT: {verdict}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"Overall Health Score: {grades['total']}/100", 0, 1)
    pdf.cell(0, 7, f"Time Complexity: {analysis.get('big_o', 'O(1)')}", 0, 1)
    pdf.ln(5)

# --- 2. BEHAVIORAL AUDIT RESULTS ---
    pdf.chapter_title('2. BEHAVIORAL AUDIT RESULTS')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 8, 'Scenario', 1)
    pdf.cell(40, 8, 'Verdict', 1)
    pdf.cell(30, 8, 'Runtime', 1)
    pdf.cell(60, 8, 'Output', 1, 1)
    
    pdf.set_font('Arial', '', 9)
    for res in behavior_results:
        # Emojis ko clean karein taaki PDF crash na ho
        v_status = str(res.get('verdict', 'N/A'))
        v_status = v_status.replace('✅', '').replace('❌', '').strip() # Remove Emojis
        
        scenario = str(res.get('scenario', 'Test'))[:30]
        runtime = str(res.get('runtime', 'N/A'))
        output = str(res.get('output', 'N/A'))[:35]
        
        # Non-latin characters (emojis) ko filter karne ka safety net
        output = output.encode('ascii', 'ignore').decode('ascii')
        scenario = scenario.encode('ascii', 'ignore').decode('ascii')

        pdf.cell(60, 8, scenario, 1)
        pdf.cell(40, 8, v_status, 1)
        pdf.cell(30, 8, runtime, 1)
        pdf.cell(60, 8, output, 1, 1)
        
        
    # --- 3. REFACTORING SUGGESTIONS ---
    if suggestions:
        pdf.chapter_title('3. AI REFACTORING SUGGESTIONS')
        pdf.set_font('Arial', '', 10)
        for s in suggestions:
            pdf.multi_cell(0, 7, f"- {s}")
        pdf.ln(5)

    # --- 4. SOURCE CODE SNAPSHOT ---
    pdf.chapter_title('4. AUDITED SOURCE CODE')
    pdf.set_font('Courier', '', 8)
    pdf.set_fill_color(250, 250, 250)
    # Code block with border
    pdf.multi_cell(0, 5, code, 1, 'L', fill=True)

    return pdf.output(dest='S').encode('latin-1')