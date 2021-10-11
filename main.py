from psyparser import Parser


def main():
    rootpath: str = './data/'
    parser: Parser = Parser()
    parser.read_in(path_rootdir=rootpath)


if __name__ == '__main__':
    main()
