from . import rep

def main():
    while True:
        try:
            text = input('json-lisfy> ')
        except (EOFError, KeyboardInterrupt):
            break
        if (val := rep.rep(text)):
            print(val)
