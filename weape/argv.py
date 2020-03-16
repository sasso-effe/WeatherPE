import sys


def __get_argv() -> str:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Invalid number of arguments")
        sys.exit()
    else:
        return str(sys.argv[1])


XLSX_PATH: str = __get_argv()
