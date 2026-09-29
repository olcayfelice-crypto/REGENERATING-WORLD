import sys
import re
from pathlib import Path


class RegeneratingWorld:

    def number_to_letter(self, number):
        number = int(number)

        if number == 0 or number == 1:
            return "A"

        if 2 <= number <= 26:
            return chr(ord("A") + number - 1)

        return ""

    def letter_to_number(self, letter):
        if letter == "A":
            return 0

        if "B" <= letter <= "Z":
            return ord(letter) - ord("A") + 1

        return 0

    def next_letter(self, letter):
        if letter == "Z":
            return ""

        return chr(ord(letter) + 1)

    def calculate(self, number, operator):
        number = int(number)

        if operator == "*":
            first = number * number

            def operation(value):
                return value * number

        elif operator == "+":
            first = number + number

            def operation(value):
                return value + number

        elif operator == "[]":
            first = number - number

            def operation(value):
                return value - number

        elif operator == "><":
            first = number / number

            def operation(value):
                return value / number

        elif operator == "//":
            first = number / number

            def operation(value):
                value = value / number
                value = value / number
                return value

        elif operator.startswith("="):
            extra = int(operator[1:])

            first = number * extra

            def operation(value):
                return value * extra

        else:
            return ""

        first = int(first)

        letter = self.number_to_letter(first)

        if not letter:
            return ""

        next_letter = self.next_letter(letter)

        if not next_letter:
            return ""

        next_number = self.letter_to_number(next_letter)

        result = operation(next_number)

        return self.number_to_letter(int(result))

    def execute(self, line):
        line = line.strip()

        if not line:
            return ""

        match = re.fullmatch(
            r"(-?\d+)=(-?\d+)",
            line
        )

        if match:
            number = int(match.group(1))
            extra = int(match.group(2))

            return self.calculate(
                number,
                "=" + str(extra)
            )

        match = re.fullmatch(
            r"(-?\d+)(\[\]|><|//|\*|\+)",
            line
        )

        if match:
            number = int(match.group(1))
            operator = match.group(2)

            return self.calculate(
                number,
                operator
            )

        return ""

    def run(self, filename):
        path = Path(filename)

        if not path.exists():
            return

        try:
            source = path.read_text(encoding="utf-8")

            result = []

            for line in source.splitlines():
                output = self.execute(line)

                if output == "":
                    return

                result.append(output)

            sys.stdout.write("".join(result))

        except Exception:
            return


if len(sys.argv) == 2:
    RegeneratingWorld().run(sys.argv[1])