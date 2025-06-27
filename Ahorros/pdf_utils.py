# utils/pdf_utils.py
from reportlab.pdfgen import canvas
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

def generar_pdf_ahorro_con_pagos(ahorro):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, "Resumen de Ahorro CROMU")

    # Datos del ahorro
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Usuario: {ahorro.nombre.username}")
    c.drawString(100, 750, f"Descripción: {ahorro.descripcion}")
    c.drawString(100, 730, f"Monto base: ${ahorro.monto}")
    c.drawString(100, 710, f"Cuota mensual: ${ahorro.cuota_mensual}")
    c.drawString(100, 690, f"Total acumulado: ${ahorro.dinero_total}")
    c.drawString(100, 670, f"Meses restantes: {ahorro.meses_restantes}")
    c.drawString(100, 650, f"Fecha de creación: {ahorro.fecha_creacion.strftime('%d/%m/%Y')}")

    # Encabezado de pagos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 620, "Pagos mensuales:")
    
    y = 600
    pagos = ahorro.pagos.all().order_by('año', 'mes')
    for pago in pagos:
        estado = "Pagado" if pago.pagado else "Pendiente"
        linea = f"{pago.mes} {pago.año} - {estado}"
        if pago.fecha_pago:
            linea += f" ({pago.fecha_pago.strftime('%d/%m/%Y')})"
        c.setFont("Helvetica", 11)
        c.drawString(100, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()

    # Encriptar el PDF
    buffer.seek(0)
    reader = PdfReader(buffer)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Puedes usar una contraseña fija
    password = f"{ahorro.nombre.username}123" 
    writer.encrypt(password)

    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output
