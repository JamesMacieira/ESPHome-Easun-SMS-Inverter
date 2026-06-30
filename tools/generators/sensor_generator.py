from pathlib import Path


class ESPHomeSensorGenerator:
    """
    Generates ESPHome sensor YAML files from Register objects.
    """

    VALUE_TYPES = {
        "int16": "S_WORD",
        "uint16": "U_WORD",
        "int32": "S_DWORD",
        "uint32": "U_DWORD",
    }

    def __init__(self, output_folder: Path):

        self.output_folder = output_folder

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def generate(self, registers):

        #
        # Group registers by worksheet
        #

        groups = {}

        for register in registers:

            if register.access != "RO":
                continue

            if register.reserved:
                continue

            if register.description_cn == "":
                continue

            groups.setdefault(register.group, [])

            groups[register.group].append(register)

        #
        # Generate one yaml file per group
        #

        for group, regs in groups.items():

            filename = self.output_folder / f"{group.lower()}.yaml"

            with open(filename, "w", encoding="utf-8") as fp:

                fp.write("# ------------------------------------------\n")
                fp.write("# Auto-generated\n")
                fp.write("# DO NOT EDIT\n")
                fp.write("# ------------------------------------------\n\n")

                fp.write("sensor:\n\n")

                for register in regs:

                    self.write_sensor(fp, register)

            print(f"Generated {filename.name}")

    def write_sensor(self, fp, register):

        value_type = self.VALUE_TYPES.get(
            register.datatype,
            "U_WORD"
        )

        entity_id = self.make_id(register)

        accuracy = self.accuracy(register.scale)

        fp.write("  - platform: modbus_controller\n")

        fp.write("    modbus_controller_id: inverter\n")

        fp.write(f"    id: {entity_id}\n")

        #
        # Prefer English description if available
        #

        name = register.description_en

        if name == "":
            name = register.description_cn

        fp.write(f'    name: "{name}"\n')

        fp.write("    register_type: holding\n")

        fp.write(f"    address: {register.address}\n")

        fp.write(f"    value_type: {value_type}\n")

        if register.unit != "":

            fp.write(
                f'    unit_of_measurement: "{register.unit}"\n'
            )

        fp.write(
            f"    accuracy_decimals: {accuracy}\n"
        )

        if register.scale != 1:

            fp.write("    filters:\n")

            fp.write(
                f"      - multiply: {register.scale}\n"
            )

        fp.write("\n")

    def accuracy(self, scale):

        text = str(scale)

        if "." not in text:

            return 0

        return len(text.split(".")[1])

    def make_id(self, register):

        #
        # Use translated name if available
        #

        text = register.description_en

        if text == "":
            text = register.description_cn

        text = text.lower()

        text = text.replace("%", "percent")

        text = text.replace("°", "")

        text = text.replace("/", "_")

        text = text.replace("-", "_")

        text = text.replace("(", "")

        text = text.replace(")", "")

        text = text.replace(".", "")

        result = []

        previous = False

        for c in text:

            if c.isalnum():

                result.append(c)

                previous = False

            else:

                if not previous:

                    result.append("_")

                    previous = True

        entity = "".join(result)

        while "__" in entity:

            entity = entity.replace("__", "_")

        return entity.strip("_")