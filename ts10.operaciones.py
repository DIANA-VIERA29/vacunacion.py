import random
from fpdf import FPDF

# Generar 500 usuarios ficticios
usuarios = [f'Usuario_{i}' for i in range(1, 501)]

# Crear conjuntos de usuarios vacunados
vacunados_pfizer = set(random.sample(usuarios, 75))
vacunados_astrazeneca = set(random.sample(usuarios, 75))

# Asegurarse de que algunos usuarios tengan ambas vacunas
usuarios_doble_vacunacion = vacunados_pfizer.intersection(vacunados_astrazeneca)
if len(usuarios_doble_vacunacion) < 10:
    adicional_doble = set(random.sample(vacunados_pfizer.union(vacunados_astrazeneca), 10 - len(usuarios_doble_vacunacion)))
    usuarios_doble_vacunacion.update(adicional_doble)

vacunados_pfizer -= usuarios_doble_vacunacion
vacunados_astrazeneca -= usuarios_doble_vacunacion

# Usuarios no vacunados
no_vacunados = set(usuarios) - (vacunados_pfizer.union(vacunados_astrazeneca).union(usuarios_doble_vacunacion))

# Crear el reporte PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Agregar título
pdf.cell(200, 10, txt="Reporte de Vacunación COVID-19", ln=True, align='C')

# Función para agregar listados al PDF
def agregar_listado(titulo, listado):
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt=titulo, ln=True)
    pdf.set_font("Arial", size=10)
    for usuario in listado:
        pdf.cell(200, 10, txt=usuario, ln=True)

# Agregar los diferentes listados al PDF
agregar_listado("Listado de ciudadanos que no se han vacunado:", no_vacunados)
agregar_listado("Listado de ciudadanos que han recibido las dos vacunas:", usuarios_doble_vacunacion)
agregar_listado("Listado de ciudadanos que solamente han recibido la vacuna de Pfizer:", vacunados_pfizer)
agregar_listado("Listado de ciudadanos que solamente han recibido la vacuna de Astrazeneca:", vacunados_astrazeneca)

# Guardar el archivo PDF
pdf_output_path = "reporte_vacunacion.pdf"
pdf.output(pdf_output_path)
print(f"Reporte generado en {pdf_output_path}")
