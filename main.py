from argparse import ArgumentParser, FileType
from datetime import datetime
from dateutil.relativedelta import relativedelta
from format import formatit
import pickle


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--file', '-f', type=FileType('rb'), required=True)
    parser.add_argument('--export', '-e', action='store_true')
    parser.add_argument('--print', '-p', action='store_true')
    parser.add_argument('--time', '-t', action='store_true')

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    ast = pickle.load(args.file)
    t1 = datetime.now()
    program = formatit(ast)
    t2 = datetime.now()

    if args.time:
        d = relativedelta(t2, t1).normalized()
        print(f'Formatting took {d.seconds}s {d.microseconds // 1000}ms')

    if args.print:
        print(program)

    if args.export:
        with open(args.file.name + '.pretty.dude', 'w') as file:
            file.write(program)


if __name__ == '__main__':
    main()
