from art import text2art
from colorama import Fore, Back, Style

from c_custom_code_checker.constants.strings import StringsConstants
import shutil


def print_line_of_hashes():
    terminal_width = shutil.get_terminal_size().columns
    line_of_hashes = "#" * terminal_width
    print(line_of_hashes)

def print_header():
    print(text2art(StringsConstants.TITLE))
    print(Style.RESET_ALL)
    print_line_of_hashes()

def print_error(error_msg):
    print(Fore.RED + f"\r\n{error_msg}\r\n")
    print(Style.RESET_ALL)

def print_success(msg):
    print(Fore.GREEN + f"\r\n{msg}\r\n")
    print(Style.RESET_ALL)
    print_line_of_hashes()


def print_process(msg):
    print(f"\r\n{msg}\r\n")
    print(Style.RESET_ALL)


def print_exception(e:Exception):
    print(Fore.RED + f"\r\n{str(e)}\r\n")
    print(Style.RESET_ALL)

def print_failure(msg):
    print(f"\r\n{msg}\r\n")
    print(Style.RESET_ALL)
    print_line_of_hashes()

