import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="Impat S.r.l. - Generatore DiCo Avanzato", layout="centered")

st.title("⚡ Impat S.r.l. - Generatore DiCo con Tabella Materiali Automatica")
st.write("Compila il form per generare la Dichiarazione di Conformità e l'Allegato Tabella Materiali (DM 37/08).")

with st.form("form_dico_avanzato"):
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

    st.subheader("❄️ 3. Macchine e Componenti")
    col3, col4 = st.columns(2)
    with col3:
        num_esterne = st.number_input("Numero Unità Esterne", min_value=1, max_value=5, value=1)
        modello_esterna = st.text_input("Modello Unità Esterna", "Daikin AZAS71MV1")
    with col4:
        num_interne = st.number_input("Numero Unità Interne", min_value=1, max_value=10, value=2)
        modello_interna = st.text_input("Modello Unità Interne", "Daikin FBA71A9 + FBA50A9")

    st.subheader("🔧 4. Tubazioni e Materiali")
    lunghezza_tubi = st.text_input("Lunghezza e Diametro Tubazioni Rame", "5/8 + 3/8 (13m e 10m)")
    scarico = st.text_input("Scarico Condensa", "Plastica Ø 16 (10m)")

    submitted = st.form_submit_button("Genera Pacchetto PDF Completo (DiCo + Materiali)")

if submitted:
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=12,
        alignment=1, # Center
        textColor=colors.HexColor("#1F4E78"),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=1,
        textColor=colors.HexColor("#595959"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=colors.HexColor("#1F4E78"),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12
    )

    # --- PAGINA 1: DICHIARAZIONE DI CONFORMITÀ ---
    story.append(Paragraph("<b>IMPAT S.r.l. Artigiana Impianti</b> - Sede: Via Banditella di Sopra 12, Ardea (RM)<br/>P.IVA 10257451004 | Tel. 069135865", subtitle_style))
    story.append(Paragraph(f"<b>DICHIARAZIONE DI CONFORMITÀ DELL'IMPIANTO ALLA REGOLA DELL'ARTE</b><br/>(Decreto 22 gennaio 2008, n. 37) — N° {num_dico}", title_style))
    
    # Dati Committente Table
    dati_comm = [
        [Paragraph("<b>DATI COMMITTENTE / UBICAZIONE</b>", body_style), ""],
        [Paragraph(f"Committente: {committente}", body_style), Paragraph(f"Proprietario: {proprietario}", body_style)],
        [Paragraph(f"Ubicazione Impianto: {indirizzo}", body_style), Paragraph(f"Data: {data_dico}", body_style)]
    ]
    t_comm = Table(dati_comm, colWidths=[270, 270])
    t_comm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#D9E1F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1F4E78")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_comm)
    story.append(Spacer(1, 15))

    # Descrizione Impianto Table
    dati_imp = [
        [Paragraph("<b>DESCRIZIONE DELL'IMPIANTO E NORMATIVA</b>", body_style), ""],
        [Paragraph(f"Tipologia: Impianto di climatizzazione a pompa di calore", body_style), Paragraph(f"Potenza: {potenza}", body_style)],
        [Paragraph(f"Norma Tecnica Applicata: {norma}", body_style), Paragraph("Esito verifiche: POSITIVO", body_style)]
    ]
    t_imp = Table(dati_imp, colWidths=[270, 270])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#D9E1F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1F4E78")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_imp)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>DICHIARAZIONE DI RISpondenza / CONFORMITÀ (Art. 6 DM 37/08)</b>", heading_style))
    story.append(Paragraph("Il sottoscritto Responsabile Tecnico dichiara sotto la propria personale responsabilità che l'impianto è stato realizzato in modo conforme alla regola dell'arte, avendo seguito la norma tecnica applicabile, installato componenti adatti e controllato l'impianto ai fini della sicurezza con esito positivo.", body_style))
    story.append(Spacer(1, 30))

    # Firme Table
    firme_data = [
        [Paragraph("<b>Il Responsabile Tecnico</b><br/><br/>Roberto Cortelletti", body_style), Paragraph(f"<b>Il Committente</b><br/><br/>{committente}", body_style)]
    ]
    t_firme = Table(firme_data, colWidths=[270, 270])
    t_firme.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_firme)

    # Interruzione di pagina per l'Allegato Materiali
    story.append(PageBreak())

    # --- PAGINA 2: TABELLA DEI MATERIALI E COMPONENTI (ALLEGATO) ---
    story.append(Paragraph(f"<b>ALLEGATO TECNICO OBBLIGATORI - TABELLA DEI MATERIALI</b><br/>Allegato alla Dichiarazione N° {num_dico}", title_style))
    story.append(Spacer(1, 10))

    # Generazione automatica delle righe della tabella in base alle unità
    materiali_data = [
        ["Rif.", "Ubicazione", "Componente / Descrizione", "Modello / Specifiche", "Q.tà", "Note / Normativa"]
    ]

    ref_counter = 1
    # Unità esterne
    for i in range(1, num_esterne + 1):
        materiali_data.append([f"F{ref_counter}", "Parete Esterna", "Unità Esterna", modello_esterna, "1", "Conforme DM 37/08"])
        ref_counter += 1

    # Unità interne
    for i in range(1, num_interne + 1):
        materiali_data.append([f"F{ref_counter}", "Parete Interna", "Unità Interna", modello_interna, "1", "Conforme DM 37/08"])
        ref_counter += 1

    # Tubazioni Rame
    for i in range(1, num_interne + 1):
        materiali_data.append([f"A{i}", "Parete Interna", "Tubazioni Frigorifere Rame", lunghezza_tubi, "1", "UNI EN 12735-1"])

    # Scarico Condensa
    materiali_data.append([f"B1", "Parete Interna", "Scarico Condensa", scarico, "1", "Plastica rigida/corrugata"])

    t_mat = Table(materiali_data, colWidths=[40, 90, 130, 160, 30, 90])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F4E78")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1F4E78")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    
    story.append(t_mat)

    doc.build(story)
    pdf_buffer.seek(0)

    st.success("Pacchetto PDF (DiCo + Tabella Materiali) generato con successo!")
    st.download_button(
        label="📥 Scarica PDF Completo DiCo & Allegati",
        data=pdf_buffer,
        file_name=f"DiCo_Completa_{num_dico.replace('-', '_')}.pdf",
        mime="application/pdf"
    )
