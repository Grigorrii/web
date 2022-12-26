from PyPDF2 import PdfFileReader
from io import BytesIO
import re

async def counter_pages(onj_read_coc):
    res=PdfFileReader(onj_read_coc)
    pages = res.getNumPages()

    return pages


