import sys
import pip
from time import sleep
from art import text2art
    
if sys.version_info[0] > 2:
    from msvcrt import getwch as getch
else:
    from msvcrt import getch

class ChoseListConsole:
    class KeysCode:
        UP = "H"
        DOWN = "P"
        SELECT = "\r"
        QUIT = "\x03"

    class Keys:
        UP = "UP"
        DOWN = "DOWN"
        SELECT = "SELECT"
        QUIT = "QUIT"

    def __init__(self, title: str, options: list):
        self.title = title
        self.options = options
        self.selected = 0

    def get_key(self) -> Keys:
        ch = getch()
        if ch == self.KeysCode.UP :
            return self.Keys.UP
        elif ch == self.KeysCode.DOWN :
            return self.Keys.DOWN
        elif ch == self.KeysCode.SELECT :
            return self.Keys.SELECT
        elif ch == self.KeysCode.QUIT :
            return self.Keys.QUIT
        else :
            return None
    

    def print(self):
        for i, option in enumerate(self.options):
            if i == self.selected:
                print(Logger.Style.bold + Logger.Foreground.green + f"➡️ {option}" + Logger.reset)
            else:
                print(f"   {option}")

    def chose(self):
        self.selected = 0
        print(self.title)
        self.print()
        while True:
            key = self.get_key()
            if key == self.Keys.UP :
                self.selected = (self.selected - 1) % len(self.options)
            elif key == self.Keys.DOWN :
                self.selected = (self.selected + 1) % len(self.options)
            elif key == self.Keys.SELECT :
                return self.selected
            elif key == self.Keys.QUIT :
                sys.exit(0)
            else :
                pass
            
            for i in range(len(self.options)):
                # clear the old list
                print("\033[F\033[K", end="")

            self.print()


class Logger:
    reset = '\033[0m'
    disable = '\033[02m'
    invisible = '\033[08m'
    separator = "--------------------------------------------------------------"

    class Style:
        bold = '\033[1m'
        dim = '\033[2m'
        normal = '\033[22m'
        underline = '\033[4m'
        reverse = '\033[7m'
        strikethrough = '\033[9m'
        big = '\033[1m\033[7m'

    class Foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        white = '\033[107m'

    @staticmethod
    def make_title(title: str = '''Solitary
Encryption''') -> None:
        title = text2art(title)
        print(Logger.Style.bold + title + Logger.reset, end="\n\n")

    @staticmethod
    def wait_animation(delay: int = 0.5) -> None:
        message = Logger.Style.bold + Logger.Foreground.yellow + "\nWaiting for data" + Logger.reset
        print(end=message)
        n_dots = 0
        while True:
            if n_dots == 3:
                print(end='\b\b\b', flush=True)
                print(end='   ',    flush=True)
                print(end='\b\b\b', flush=True)
                n_dots = 0
            else:
                print(end='.', flush=True)
                n_dots += 1
            sleep(delay)

    @staticmethod
    def missing_module(module: str) -> None:
        print(Logger.Style.bold + Logger.Foreground.red + f"'{module}' module not found !" + Logger.reset)
        chose = ChoseListConsole(["Yes", "No"], "We can install the art module for you, do you agree ? ").chose()
        if chose == 0:
            print(Logger.Style.bold + Logger.Foreground.yellow + f"Installing '{module}' module..." + Logger.reset)
            pip.main(['install', module])
            from art import text2art
        else :
            print(Logger.Style.bold + Logger.Foreground.red + f"'{module}' module is required to run this program, exiting..." + Logger.reset)
            print(Logger.Style.bold + Logger.Foreground.red + "You can install it by running 'pip install art'" + Logger.reset)
            sys.exit(0)
