import io
from docx import Document
from docx.shared import Cm

from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_CO')


def createReport(report_data, analysis):

    doc = Document()

    for style in doc.styles:
        try:
            doc.styles[style.name].font.name = 'Arial'
        except:
            None

    # Sección de Encabezado

    header = doc.sections[0].header
    h_content = header.paragraphs[0]

    h_run = h_content.add_run()
    h_run.add_picture('logo.png', width=Cm(1.5))

    text_run = h_content.add_run()
    text_run.text = '\t' + 'Roboat Stingray - Generador de Reportes'

    # Sección de Pié de Página

    bottom = doc.sections[0]
    footer = bottom.footer

    f_content = footer.paragraphs[0]
    f_content.text = '''
    Roboat Stingray Web App
    Universidad de Boyacá © - Todos los derechos reservados (2021) '''

    # Contenido del Documento

    doc.add_heading(report_data['title'], 1) if report_data['title'] else doc.add_heading(
        'Reporte Preliminar de Calidad del Agua', 0)

    doc.add_paragraph(
        'Este es un reporte preliminar de la calidad del agua generado en la aplicación web del Sistema Roboat '
        'Stingray. Aquí se describen las caracteristicas de las variables medidas y los datos estadisticos '
        'recolectados a partir del análisis.')

    p = doc.add_paragraph('\n')
    p.add_run(str(datetime.now().strftime("%A, %d de %B de %Y")) + '\n\n').bold = True

    p.add_run('Autor(es): ').bold = True
    p.add_run(report_data['author'] + '\n\n') if report_data['author'] else p.add_run('Aquí va el nombre del autor(es)\n\n')

    p.add_run('Dirigido a: ').bold = True
    p.add_run(report_data['sendTo'] + '\n\n') if report_data['sendTo'] else p.add_run('Aquí va la entidad o persona a quien se dirige el reporte\n\n')

    p.add_run('Razón del reporte:\n').bold = True
    p.add_run(report_data['reason'] + '\n\n') if report_data['reason'] else p.add_run('Aquí va la descripción del por qué se genera el reporte\n\n')

    # Tabla
    t = doc.add_table(analysis['B'].shape[0] + 1, analysis['B'].shape[1])

    # add the header rows.
    for j in range(analysis['B'].shape[-1]):
        t.cell(0, j).text = analysis['B'].columns[j]

    # add the rest of the data frame
    for i in range(analysis['B'].shape[0]):
        for j in range(analysis['B'].shape[-1]):
            t.cell(i + 1, j).text = str(analysis['B'].values[i, j])

    # Guardado del archivo en memoria

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    return file_stream
