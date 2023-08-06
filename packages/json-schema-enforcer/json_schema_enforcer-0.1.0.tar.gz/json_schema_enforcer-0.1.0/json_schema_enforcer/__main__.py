import curses
import json

from .schema import parser_for_schema


def main():
    schema = json.loads(input("Schema: "))

    parser = parser_for_schema(schema)
    if parser is None:
        print("Invalid schema")
        return

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    data: str = ""

    try:
        while True:
            screen.clear()
            screen.addstr(0, 0, data)

            validated = parser.validate(data)
            if not validated.valid:
                screen.addstr(1, 0, "Invalid")

            screen.refresh()

            c = screen.getch()
            if c == 10:
                break
            elif c == 263:
                data = data[:-1]
            else:
                data += chr(c)
    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main()
