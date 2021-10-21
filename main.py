import sys

from src.parser import Parser


def main():
    parser = Parser()  # Path is an optional argument (datapath)
    parser.run()  # Path is an optional argument (savepath)
    print(sys.version)

if __name__ == '__main__':
    main()
