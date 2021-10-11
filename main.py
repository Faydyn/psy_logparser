from psyparser import Parser


def main():
    rootpath: str = './data/'
    parser: Parser = Parser(path_rootdir=rootpath)
    print(parser)

if __name__ == '__main__':
    main()
