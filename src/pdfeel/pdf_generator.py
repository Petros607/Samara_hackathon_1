from datetime import date
from pathlib import Path

from fpdf import FPDF

from config import PATH

path_resources = Path(PATH) / 'src/pdfeel/resource/'
font_family = 'arial'
font_size = 12


class BbbPDF(FPDF):

    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font(font_family, style='', fname=str(path_resources / font_family / 'regular.ttf'))
        self.add_font(font_family, style='B', fname=str(path_resources / font_family / 'bold.ttf'))
        self.add_font(font_family, style='BI', fname=str(path_resources / font_family / 'bold_inclined.ttf'))
        self.add_font(font_family, style='I', fname=str(path_resources / font_family / 'inclined.ttf'))
        self.set_font(font_family, '', font_size)
        self.set_left_margin(20)
        self.set_right_margin(25)
        self.add_page()

    def footer(self):
        self.set_y(-15)
        self.set_font(family=font_family, style='')
        page = str(self.page_no())
        self.cell(text=page, center=True)


def generate_filename(url_id, subject='', speaker='', date_time=str(date.today())):
    '''
    filename = date_time + '.pdf'
    if speaker != '':
        filename = speaker + ' - ' + filename
    if subject != '':
        filename = subject + ' - ' + filename
    '''

    filename = url_id + ".pdf"

    return filename


def generate_pdf(images, texts, summary, file_path):
    pdf = BbbPDF()

    pdf.set_font(family=font_family, style='B')
    pdf.cell(w=0, h=7, text='Аннотация')
    pdf.ln()
    pdf.set_font(family=font_family, style='')
    pdf.multi_cell(w=0, h=7, text=summary)
    pdf.ln()
    pdf.set_font(family=font_family, style='B')
    pdf.cell(w=0, h=7, text='Протокол лекции')
    pdf.ln()

    for i in range(len(images)):
        pdf.image(images[i], w=pdf.epw)
        pdf.ln()
        for paragraph in texts[i]:
            pdf.set_font(family=font_family, style='B')
            pdf.cell(w=0, h=7, text=str(paragraph['time']))
            pdf.ln()
            pdf.set_font(family=font_family, style='')
            pdf.multi_cell(w=0, h=7, text=str(paragraph['text'].strip()))
            pdf.ln()

    pdf.output(file_path)
