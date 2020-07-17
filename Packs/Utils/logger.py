class Logger:
    def __init__(self, text:str = '', colors:str = 'normal', end:str = "\n") -> None:
        colorsX = {
            'normal': '{text}',
            'red': '\033[91m{text}\033[37m',
            'white': '\033[37m{text}',
            'green': '\033[92m{text}\033[37m',
            'pink': '\033[95m{text}\033[37m',
            'blue': '\033[94m{text}\033[37m',
            'yellow': '\033[93m{text}\033[37m'
        }

        print(colorsX[colors].format(text=text), end=end)


if __name__ == "__main__":
    Logger('Hello, i am a test string')
    Logger('Hello, i am a test string', 'red')
    Logger('Hello, i am a test string', 'blue')
    Logger('Hello, i am a test string', 'white')
    Logger('Hello, i am a test string', 'green')
    Logger('Hello, i am a test string', 'pink')
    Logger('Hello, i am a test string', 'yellow')
    Logger('Hello, i am a test string', 'normal')