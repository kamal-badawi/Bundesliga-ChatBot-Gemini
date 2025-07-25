# Diese Methode wurde schon im Masterprojekt verwendet und an diesem Fall angepasst
# Diese Methode wurde mit ChatGPT erstellt aber auch zu einem großen Teil angepasst
def run_create_pdf(text) -> dict:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import re
    import os
    from io import BytesIO
    import datetime
    
    def replace_german_umlauts(text):
        umlaut_map = {
            'ä': 'ae',
            'ö': 'oe',
            'ü': 'ue',
            'Ä': 'Ae',
            'Ö': 'Oe',
            'Ü': 'Ue',
            'ß': 'ss'
        }
        for umlaut, replacement in umlaut_map.items():
            text = text.replace(umlaut, replacement)
        return text
   
    # Text in Linien mit Zeilenumbruch
    def parse_text_to_lines(text, c, max_width, font_name="Helvetica"):
        """
        Gibt eine Liste von (text, bold) Paaren pro Zeile zurück,
        wobei langer Text umgebrochen wird und **fett** erkannt wird.
        """
        lines = []
        current_line = []
        current_width = 0
        output = ""
        
        for item in text:
            question = replace_german_umlauts(text=item['question']).encode('latin1').decode('utf-8', errors='replace')
            answer =  replace_german_umlauts(text=item['answer']).encode('latin1').decode('utf-8', errors='replace')
            output += f"**{question}**\n{answer}"
            output += f"\n--------\n"


        text = output

        for paragraph in text.split('\n'):
            if paragraph.strip() == "--------":
                lines.extend([[], []])  # 4 Leerzeilen
                continue

            

            tokens = re.split(r'(\*\*.*?\*\*|\s+)', paragraph)
            line = []
            line_width = 0

            for token in tokens:
                if not token:
                    continue

                is_bold = token.startswith("**") and token.endswith("**")

                display_text = token[2:-2] if is_bold else token

                font = "Helvetica-Bold" if is_bold else font_name
                text_width = c.stringWidth(display_text, font, 14 if is_bold else 12)

                if line_width + text_width > max_width:
                    lines.append(line)
                    line = []
                    line_width = 0

                line.append((display_text, is_bold))
                line_width += text_width

            if line:
                lines.append(line)

        return lines




    # Basisverzeichnis: ein Verzeichnis über `backend`
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_image_path = os.path.join(base_dir, "Images", "Logo with BG.png")
    signature_image_path = os.path.join(base_dir, "Images", "Signature.png")

    
    logo_image = ImageReader(logo_image_path)

    
    signature_image = ImageReader(signature_image_path)

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    margin = 20 * mm
    max_width = width - 2 * margin
    x = margin
    y = height - margin
    line_height = 14

    # Bild mit fester Größe 200x100 px zeichnen (oben links)
    c.drawImage(logo_image, (max_width / 2) - 75 + x, y - 100, width=150, height=100)
    y -= (150 + 10)  # Platz unter dem Bild

    # Jetzt den Header-Text einfügen, immer Platz vorher prüfen
    header_lines = [
        'Liebe Kundin, lieber Kunde,',
        ' ',
        'anbei übersenden wir Ihnen die Unterhaltung',
        ' ',
        ' ',
    ]

    for header_text in header_lines:
        if y - line_height < margin:
            c.showPage()
            y = height - margin
            c.setFont('Helvetica', 12)

        y -= line_height
        c.drawString(x, y, header_text)

    # --- Trennlinie---
    def create_sep_line(y):
        if y - line_height < margin:
            c.showPage()
            y = height - margin
            c.setFont('Helvetica', 12)

        y -= line_height
        c.setDash(3, 2)  # gestrichelte Linie: 3 Punkte Linie, 2 Punkte Lücke
        c.line(x, y, width - margin, y)
        c.setDash()  # zurücksetzen auf durchgezogene Linie
        y -= line_height
        return y

    y = create_sep_line(y) - line_height

    # Text vorbereiten (parse_text_to_lines musst du selbst definiert haben)
    lines = parse_text_to_lines(text, c, max_width)
    c.setFont('Helvetica', 12)

    for line in lines:
        # Platz für eine Zeile prüfen
        if y - line_height < margin:
            c.showPage()
            y = height - margin
            c.setFont('Helvetica', 12)

        if not line:
            y -= line_height
            continue

        current_x = x
        for word, is_bold in line:
            font = "Helvetica-Bold" if is_bold else "Helvetica"
            c.setFont(font, 12)
            c.drawString(current_x, y, word)
            current_x += c.stringWidth(word, font, 12)
        y -= line_height

    y = create_sep_line(y)

    now = datetime.datetime.now()
    created_datetime_sending_time = now.strftime("%d. %m. %Y um %H:%M:%S")
    created_datetime_file_name = now.strftime("%d-%m-%Y-%H-%M-%S")


    # Jetzt den Schluss-Text einfügen, immer Platz vorher prüfen
    footer_lines = [
        'Vielen Dank für die Nutzung des Bundesliga-ChatBots.',
        ' ',
        'Mit freundlichen Grüßen,',
        ' ',
        ' ',
        'Ihr Bundesliga-ChatBot Team'
    ]

    for footer_text in footer_lines:
        if y - line_height < margin:
            c.showPage()
            y = height - margin
            c.setFont('Helvetica', 12)

        y -= line_height
        c.drawString(x, y, footer_text)

    # Abschließend Bild unten einfügen (eventuell neue Seite)
    if y - 60 < margin:
        c.showPage()
        y = height - margin

    y -= 60
    c.drawImage(signature_image, x + 40, y, width=100, height=50)

    if y - (line_height) < margin:
        c.showPage()
        y = height - margin
        c.setFont('Helvetica', 12)

    y -= (line_height)
    c.drawString(x, y, f'Erstellt am {created_datetime_sending_time}')

    c.save()
    pdf_buffer.seek(0)
    response = {'pdf_buffer' : pdf_buffer,
                'created_datetime_file_name' : created_datetime_file_name,
                'created_datetime_sending_time' : created_datetime_sending_time}
    return response
