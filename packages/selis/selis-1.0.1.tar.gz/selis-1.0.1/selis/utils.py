import os
import webbrowser


def convert_color(string, style):
    colors = {
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m'
    }
    return colors[style] + string


def open_url(url):
    webbrowser.open(url)


def clear_screen():
    os.system("clear")


def guide_to_exit():
    print(convert_color("[+] Press 'Ctrl + C' or 'Enter' to exit", style="ENDC"))