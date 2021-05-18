"""Pushing and pulling pdf files"""
import requests
from datetime import datetime
from stamp_to_pdf import StampToPdf
from pathlib import Path
import os


class PushPullFile():
    """Class for pushing and pulling pdf files"""

    @staticmethod
    def push_pull_file(arguments):
        """for pulling pdf files"""
        # Handling exceptions if required
        if (arguments["take_path"] is None) or (arguments["take_path"] == ""):
            raise AttributeError("take_path")
        if (arguments["put_path"] is None) or (arguments["put_path"] == ""):
            raise AttributeError("put_path")

        res = requests.get(arguments['take_path'])

        # Create name and directory(optional) for the document
        now = datetime.now()
        timestamp = int(datetime.timestamp(now))
        filename = f"DocumentWithStamp_{timestamp}.pdf"
        Path("input_files").mkdir(parents=True, exist_ok=True)

        # Save the document to the 'input_files'
        with open(os.path.join("input_files", filename), "wb") as f:
            f.write(res.content)

        # Handle the document
        StampToPdf.stamp_to_pdf(
            input_path=os.path.join("input_files", filename),
            output_path=os.path.join(arguments["put_path"], filename),
            watermark='stamps/stamp_2.pdf')

        # Delete our document from 'input_files' after saving it to the required destination
        os.remove(os.path.join("input_files", filename))
