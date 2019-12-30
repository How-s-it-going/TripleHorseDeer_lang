# TripleHorseDeer
Brainfuck派生言語の「さんばか」言語です

オペレーターがそれぞれ
['+', '-', '>', '<', '[', ']', '.', ',']
から
['いぬい', 'とこ', 'アン', 'カト', 'さん', 'ばか', 'リゼ', 'エスタ']
に置き換えられています

```shell
python run.py <source_path> [-o(or --output) <output_path>] [-i(or --input) <input_path>]
```
で実行する事が出来ます(入出力はデフォルトで標準入出力です)
出力はマルチバイト文字に対応しています


`THD.py`は[こちら](https://github.com/fboender/pybrainfuck/)のコードを改変したものになります
[Ferry Boender](https://github.com/fboender)に感謝
