from psyparser import Parser


def main():
    rootpath= './data/'
    savepath= './out/'

    parser= Parser(path_rootdir=rootpath)
    parser.run(path_savedir=savepath)


if __name__ == '__main__':
    main()
