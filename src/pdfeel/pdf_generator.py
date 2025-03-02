import os.path
from datetime import date, time
from os import listdir
from pathlib import Path
from fpdf import FPDF
from config import PATH
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image
import fitz



path_resources = Path(PATH) / "src/pdfeel/resource/"
font_family = "arial"
font_size = 12




class BbbPDF(FPDF):

    def __init__(self):
        # инициализация
        super().__init__(orientation="P", unit="mm", format="A4")
        # установка шрифтов
        self.add_font(
            font_family,
            style="",
            fname=str(path_resources / font_family / "regular.ttf"),
        )
        self.add_font(
            font_family, style="B", fname=str(path_resources / font_family / "bold.ttf")
        )
        self.add_font(
            font_family,
            style="BI",
            fname=str(path_resources / font_family / "bold_inclined.ttf"),
        )
        self.add_font(
            font_family,
            style="I",
            fname=str(path_resources / font_family / "inclined.ttf"),
        )
        self.set_font(font_family, "", font_size)
        # установка отступов
        self.set_left_margin(20)
        self.set_right_margin(25)
        # создание первой страницы
        self.add_page()

    def footer(self):
        # добавление номера страницы
        self.set_y(-15)
        self.set_font(family=font_family, style="")
        page = str(self.page_no())
        self.cell(text=page, center=True)


def generate_filename(url_id, subject="", speaker="", date_time=str(date.today())):
    """
    filename = date_time + '.pdf'
    if speaker != '':
        filename = speaker + ' - ' + filename
    if subject != '':
        filename = subject + ' - ' + filename
    """

    filename = url_id + ".pdf"

    return filename

def process_image(svg_path: str) -> str:
    pdf_path = str(svg_path).replace(".svg", ".pdf")
    png_path = str(svg_path).replace(".svg", ".png")
    drawing = svg2rlg(svg_path)
    renderPDF.drawToFile(drawing, pdf_path)
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(png_path, "PNG")
    return png_path

def generate_pdf(images_path, texts, summary, file_path):
    """
    Недокументированная функция без единого тайпхинта, написанная джавистом
    """
    # загрузка изображений с сортировкой по порядку
    images = None
    if os.path.exists(images_path):
        images = listdir(images_path)
        images.sort(key=lambda x: int(x.replace("slide", "").replace(".svg", "")))

    pdf = BbbPDF()
    # вставка аннотации
    pdf.set_font(family=font_family, style="B")
    pdf.cell(w=0, h=7, text="Аннотация")
    pdf.ln()
    pdf.set_font(family=font_family, style="")
    pdf.multi_cell(w=0, h=7, text=summary)
    pdf.ln()

    # вставка протокола
    pdf.set_font(family=font_family, style="B")
    pdf.cell(w=0, h=7, text="Протокол лекции")
    pdf.ln()
    
    # #КООООСТТЫЫЫЫЛЬЬЬЬ!!!!!!!
    # length = min(len(images), len(texts))
    
    for i in range(len(images)):
        
        if images is not None and len(images) > 0:
          
            # вставка слайдов (если имеются)
            svg_path = Path(images_path) / images[i]
            png_path = process_image(svg_path)
            
            pdf.image(png_path, w=pdf.epw)
            pdf.ln()
        for paragraph in texts[i]:
            # вставка тайм-кода
            pdf.set_font(family=font_family, style="B")
            pdf.cell(w=0, h=7, text=str(paragraph["time"]))
            pdf.ln()
            # вставка текста
            pdf.set_font(family=font_family, style="")
            pdf.multi_cell(w=0, h=7, text=str(paragraph["text"].strip()))
            pdf.ln()
            
    # #КООООСТТЫЫЫЫЛЬЬЬЬ!!!!!!!
    # for i in range(len(images), len(texts)):
    #     for paragraph in texts[i]:
    #         # вставка тайм-кода
    #         pdf.set_font(family=font_family, style="B")
    #         pdf.cell(w=0, h=7, text=str(paragraph["time"]))
    #         pdf.ln()
    #         # вставка текста
    #         pdf.set_font(family=font_family, style="")
    #         pdf.multi_cell(w=0, h=7, text=str(paragraph["text"].strip()))
    #         pdf.ln()
    # сохранение файла
    pdf.output(file_path)
