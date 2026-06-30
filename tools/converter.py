from pathlib import Path

from tools.parser import ExcelParser


PROJECT_ROOT = Path(__file__).resolve().parent.parent


EXCEL_FILE = (
    PROJECT_ROOT /
    "modbus" /
    "original" /
    "CVTE_Modbus_v1.20.xlsx"
)


def banner():

    print()

    print("=" * 60)

    print(" ESPHome Easun SMS Modbus Converter ")

    print("=" * 60)

    print()


def main():

    banner()

    print(f"Opening: {EXCEL_FILE}")

    parser = ExcelParser(EXCEL_FILE)

    parser.load()

    print()

    print("Workbook successfully loaded")

    print()

    sheets = parser.worksheet_names()

    print(f"Found {len(sheets)} worksheets")

    print()

    for sheet in sheets:

        print(f"  ✓ {sheet}")

    print()

    print("Ready.")


if __name__ == "__main__":

    main()