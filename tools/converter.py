from pathlib import Path
import json

from tools.parser import ExcelParser


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODBUS_FOLDER = PROJECT_ROOT / "modbus" / "original"

OUTPUT_FOLDER = PROJECT_ROOT / "modbus" / "json"


def banner():

    print()
    print("=" * 60)
    print(" ESPHome Easun SMS Modbus Converter ")
    print("=" * 60)
    print()


def locate_excel():

    files = list(MODBUS_FOLDER.glob("*.xlsx"))

    if not files:
        raise FileNotFoundError(
            "No Excel workbook found in modbus/original"
        )

    return files[0]


def save_json(registers):

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    filename = OUTPUT_FOLDER / "protocol.json"

    data = [register.to_dict() for register in registers]

    with open(filename, "w", encoding="utf-8") as fp:

        json.dump(
            data,
            fp,
            indent=4,
            ensure_ascii=False
        )

    return filename


def statistics(registers):

    total = len(registers)

    reserved = sum(r.reserved for r in registers)

    valid = total - reserved

    print()
    print("=" * 60)
    print("Statistics")
    print("=" * 60)

    print(f"Total Registers : {total}")
    print(f"Valid Registers : {valid}")
    print(f"Reserved        : {reserved}")

    print()

    groups = {}

    for register in registers:

        groups.setdefault(register.group, 0)

        groups[register.group] += 1

    print("Registers per group")

    print("-------------------")

    for group in sorted(groups):

        print(f"{group:20} {groups[group]}")


def preview(registers):

    print()
    print("=" * 60)
    print("Preview")
    print("=" * 60)
    print()

    for register in registers[:20]:

        print(register)


def main():

    banner()

    excel = locate_excel()

    print(f"Opening workbook : {excel.name}")

    parser = ExcelParser(excel)

    parser.load()

    print("Workbook loaded")

    print()

    print("Reading worksheets...")

    registers = parser.parse_all()

    print(f"Done ({len(registers)} registers found)")

    preview(registers)

    statistics(registers)

    filename = save_json(registers)

    print()

    print("=" * 60)

    print(f"JSON written to:")

    print(filename)

    print("=" * 60)

    print()

    print("Finished.")


if __name__ == "__main__":

    main()