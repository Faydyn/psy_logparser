from psyparser import Parser

if __name__ == '__main__':
    rootpath: str = './data_gonogo/'
    parser: Parser = Parser()
    parser.read_in(path_rootdir=rootpath)
