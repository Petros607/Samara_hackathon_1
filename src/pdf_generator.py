from fpdf import FPDF


def generate(text_data, file_name):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('times_new_roman', style='', fname='../resource/timesnrcyrmt.ttf')
    pdf.add_font('times_new_roman', style='B', fname='../resource/timesnrcyrmt_bold.ttf')
    pdf.add_font('times_new_roman', style='BI', fname='../resource/timesnrcyrmt_boldinclined.ttf')
    pdf.add_font('times_new_roman', style='I', fname='../resource/timesnrcyrmt_inclined.ttf')

    pdf.set_font('times_new_roman', '', 14)
    pdf.set_left_margin(20)
    pdf.set_right_margin(25)
    pdf.add_page()
    pdf.image('../resource/image.jpg', w=pdf.epw)
    pdf.ln()
    pdf.multi_cell(w=0, h=7, text=text_data, markdown=True)
    pdf.output(file_name)


with open('../resource/text_md.txt', encoding='utf-8') as file:
    text = file.readlines()
    text = '\n'.join(text)
    generate(text, '../resource/file.pdf')
