from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings


def save_pdf(params:dict):
    template = get_template("invoice/invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
    file_name = uuid.uuid4()
    file_path = f"{settings.MEDIA_ROOT}/pdf/{file_name}.pdf"

    try:
        with open(file_path,"wb+") as f:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),f)
    except Exception as e:
        print(e)

    if pdf.err:
        return "",False
    return file_name,True
