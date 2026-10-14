import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="Impat S.r.l. - Generatore DiCo Dinamico", layout="centered")

st.title("⚡ Impat S.r.l. - Generatore DiCo Dinamico")
st.write("Imposta il numero di unità per far comparire dinamicamente i campi di input dei modelli e dei materiali.")

with st.form("form_dico_dinamico"):
    st.subheader("📋 1. Dati Documento e Cantiere")
    col1, col2 = st.columns(2)
    with col1:
        num_dico = st.text_input("Numero DiCo", "12-25")
        data_dico = st.text_input("Data Emissione", "21/10/2026")
    with col2:
        potenza = st.text_input("Potenza Impianto (kW)", "11,8 kW")
        norma = st.text_input("Norma Tecnica", "UNI EN 378")

    st.subheader("👥 2. Committente e Proprietario")
    committente = st.text_input("Committente", "De Paolis Mauro")
    proprietario = st.text_input("Proprietario dei locali", "Pugliese Patrizia")
    indirizzo = st.text_input("Ubicazione Impianto", "Via degli Scipioni 142, Roma (RM)")

    st.subheader("❄️ 3. Unità Esterne e Interne")
    
    # Selezione del numero di unità esterne
    num_esterne = st.number_input("Numero Unità Esterne", min_value=1, max_value=5, value=1, step=1)
    modelli_esterne = []
    for i in range(int(num_esterne)):
        mod = st.text_input(f"Modello Unità Esterna {i+1} (F{i+1})", "Daikin AZAS71MV1", key=f"est_{i}")
        modelli_esterne.append(mod)

    st.markdown("---")
    
    # Selezione del numero di unità interne (Split)
    num_interne = st.number_input("Numero Unità Interne (Split)", min_value=1, max_value=10, value=2, step=1)
    
    interne_dati = []
    for i in range(int(num_interne)):
        st.markdown(f"**Split Interno {i+1}**")
        col_a, col_b = st.columns(2)
        with col_a:
            mod_int = st.text_input(f"Modello Unità Interna {i+1}", "Daikin FBA50A9", key=f"mod_int_{i}")
        with col_b:
            tubi_int = st.text_input(f"Tubazioni Rame Split {i+1}", "3/8 + 1/4 (10m)", key=f"tubi_int_{i}")
        interne_dati.append({"modello": mod_int, "tubi": tubi_int})

    st.subheader("🔧 4. Scarico Condensa e Note")
    scarico = st.text_input("Scarico Condensa (Generale / Unificato)", "Plastica Ø 16 (10m)")

    submitted = st.form_submit_button("Genera Pacchetto PDF Dinamico")

if submitted:
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=12, alignment=1, textColor=colors.HexColor("#1F4E78"), spaceAfter=15)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=9, alignment=1, textColor=colors.HexColor("#595959"), spaceAfter=20)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=10, textColor=colors.HexColor("#1F4E78"), spaceBefore=10, spaceAfter=5)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=12)

    # --- PAGINA 1: DICHIARAZIONE DI CONFORMITÀ ---
    story.append(Paragraph("<b>IMPAT S.r.l. Artigiana Impianti</b> - Sede: Via Banditella di Sopra 12, Ardea (RM)<br/>P.IVA 10257451004 | Tel. 069135865", subtitle_style))
    story.append(Paragraph(f"<b>DICHIARAZIONE DI CONFORMITÀ DELL'IMPIANTO ALLA REGOLA DELL'ARTE</b><br/>(Decreto 22 gennaio 2008, n. 37) — N° {num_dico}", title_style))
    
    dati_comm = [
        [Paragraph("<b>DATI COMMITTENTE / UBICAZIONE</b>", body_style), ""],
        [Paragraph(f"Committente: {committente}", body_style), Paragraph(f"Proprietario: {proprietario}", body_style)],
        [Paragraph(f"Ubicazione Impianto: {indirizzo}", body_style), Paragraph(f"Data: {data_dico}", body_style)]
    ]
    t_comm = Table(dati_comm, colWidths=[270, 270])
    t_comm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#D9E1F2")),
        ('BOX', (0
    
