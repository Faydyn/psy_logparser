from psyparser import Parser


def main():
    rootpath: str = './data/'
    parser: Parser = Parser(path_rootdir=rootpath)
    parser.run()

if __name__ == '__main__':
    main()
