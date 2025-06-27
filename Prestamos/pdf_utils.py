# utils/pdf_utils.py
from reportlab.pdfgen import canvas
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

def generar_pdf_prestamo_con_cuotas(prestamo):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, "Resumen de Préstamo CROMU")

    # Datos del préstamo
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Usuario: {prestamo.nombre.username}")
    c.drawString(100, 750, f"Descripción: {prestamo.descripcion}")
    c.drawString(100, 730, f"Monto prestado: ${prestamo.monto}")
    c.drawString(100, 710, f"Cuota mensual: ${prestamo.cuota_mensual}")
    c.drawString(100, 690, f"Meses restantes: {prestamo.cantidad_meses}")
    c.drawString(100, 670, f"Fecha de creación: {prestamo.fecha_creacion.strftime('%d/%m/%Y')}")

    # Encabezado de cuotas
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 640, "Historial de cuotas:")
    
    y = 620
    cuotas = prestamo.cuotas.all().order_by('año', 'mes')
    for cuota in cuotas:
        estado = "Pagado" if cuota.pagado else "Pendiente"
        linea = f"{cuota.mes} {cuota.año} - {estado}"
        if cuota.fecha_pago:
            linea += f" ({cuota.fecha_pago.strftime('%d/%m/%Y')})"
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

    password = f"{prestamo.nombre.username}123" 
    writer.encrypt(password)

    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output
