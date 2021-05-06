"""Pushing and pulling pdf files"""
import requests
from datetime import datetime
from Demo.stamp_to_pdf import StampToPdf
# from stamp_to_pdf import StampToPdf

class PushPullFile():
    """Class for pushing and pulling pdf files"""

    @staticmethod
    def pull_file(arguments):
        """for pulling pdf files"""
        res = requests.get(arguments['take_path'])
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        with open(f"input_files/InputPdf_{timestamp}.pdf", "wb") as f:
            f.write(res.content)
        # command = f"curl {arguments['take_path']} -o InputPdf.pdf"
        # os.system(f'cmd /k {command}')
        StampToPdf.stamp_to_pdf(
            input_pdf=f'input_files/InputPdf_{timestamp}.pdf',
            output=f'output_files/OutputPdf_{timestamp}.pdf',
            watermark='stamps/stamp_3.pdf')
        # StampToPdf.stamp_to_pdf(
        #     input_pdf=f'sertificates/test_pdf_2.pdf',
        #     output=f'output_files/OutputPdf_2.pdf',
        #     watermark='stamps/stamp_2.pdf')
        # return f'output_files/OutputPdf_2.pdf'
        return f'output_files/OutputPdf_{timestamp}.pdf'

    @staticmethod
    def push_file():
        """for pushing pdf files"""
        pass
