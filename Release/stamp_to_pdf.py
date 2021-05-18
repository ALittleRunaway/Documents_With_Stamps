"""Adding watermark to the document"""
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

class StampToPdf():
    """Class for adding watermark to the document"""

    @staticmethod
    def stamp_to_pdf(input_path, output_path, watermark):
        """Merges the document and the watermark"""
        # watermark object
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)
        # document object
        pdf_reader = PdfFileReader(input_path, strict=False)
        pdf_writer = PdfFileWriter()

        # measurements
        watermark_height = float(watermark_page.mediaBox[3])
        watermark_width = float(watermark_page.mediaBox[2])
        # print(watermark_height, watermark_width)
        page_height = float(pdf_reader.getPage(0).mediaBox[3])
        page_width = float(pdf_reader.getPage(0).mediaBox[2])

        # resize watermark
        required_watermark_height = page_height * 0.1782376502
        scale_by = required_watermark_height / watermark_height
        # find he position for the watermark in the page
        y_by = int(page_height / 25)
        x_by = int(page_width - (watermark_width * scale_by)) - y_by

        # Watermark all of the pages
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergeRotatedScaledTranslatedPage(watermark_page, 0, scale_by, x_by, y_by, expand=False)
            pdf_writer.addPage(page)

        # save merged document to the file
        with open(output_path, 'wb') as out:
            pdf_writer.write(out)


