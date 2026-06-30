from pathlib import Path

from openpyxl import load_workbook


class ExcelParser:

    def __init__(self, filename: Path):

        self.filename = filename

        self.workbook = None

    def load(self):

        self.workbook = load_workbook(
            self.filename,
            data_only=True
        )

    def worksheet_names(self):

        return self.workbook.sheetnames