from parser import Parser


def main():
    ROOTPATH = './data/'
    SAVEPATH = './out/'

    parser = Parser(path_rootdir=ROOTPATH)
    parser.run(path_savedir=SAVEPATH)


if __name__ == '__main__':
    main()
