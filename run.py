from THD import TripleHorseDeer
import argparse
import sys


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='TripleHorseDeer(Brainfuck派生言語)', prefix_chars='-/')
    p.add_argument('THDFile', type=str, help='TripleHorseDeerで記述されたファイルへのパス')
    p.add_argument('--output', help='出力先へのパス(デフォルトは標準出力)')
    p.add_argument('--input', help='入力元へのパス(デフォルトは標準入力)')
    a = p.parse_args()

    code = open(a.THDFile, 'r', encoding='UTF-8').read()
    TripleHorseDeer(
        code,
        input=open(a.input, 'r') if a.input else sys.stdin,
        output=open(a.output, 'w') if a.output else sys.stdout).run()
