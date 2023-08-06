"""
PythonHuff is a simple Python package, which does Huffman compression and decompression.
"""
from .classes import *
import collections, sys,argparse


def get_freq(inbytes):
    return collections.Counter(inbytes).items()


def _to_int( c):
    if sys.version_info.major > 2:
        return c
    else:
        return ord(c)


def make_tree(freq):
    trees = []
    for i, j in freq:
        trees.append(Tree(None, None, j, i))
    while len(trees) > 1:
        a, b = trees.pop(), trees.pop()
        trees.insert(0, Tree(a, b, a.val + b.val, None))
    return trees.pop()


def _parse_tree(tree, table, prefix):
    if tree.dat is not None:
        table[tree.dat] = prefix
    else:
        _parse_tree(tree.l, table, prefix + [0])
        _parse_tree(tree.r, table, prefix + [1])


def _parse_tree2(tree, table, prefix):
    table[tree.dat] = [0]


def _to_list(inbytes):
    if sys.version_info.major > 2:
        return inbytes
    else:
        return [ord(i) for i in inbytes]


def parse_tree(tree, table, prefix):
    if tree.dat is not None:
        return _parse_tree2(tree, table, prefix)
    else:
        return _parse_tree(tree, table, prefix)


def encode(inbytes):
    freq = get_freq(_to_list(inbytes))
    tree = make_tree(freq)
    table = {}
    parse_tree(tree, table, [])
    t = Translator(table)
    if sys.version_info.major == 2:
        inbytes = [ord(i) for i in inbytes]
    return t.translate(inbytes)


def decode(table, inbytes, remain):
    t = Translator(table)
    return t.detranslate(inbytes, remain)


def get_table(inbytes):
    tree = make_tree(get_freq(_to_list(inbytes)))
    t = {}
    parse_tree(tree, t, [])
    return t


def _to_bytes(c):
    if sys.version_info.major > 2:
        return bytes(c)
    else:
        return "".join([chr(i) for i in c])


def compress(inbytes):
    enc, rem = encode(inbytes)
    table = get_table(inbytes)
    res = b""
    res += _to_bytes([rem])
    res+=str(len(list(table.keys()))).encode()+b'\0'
    for i, j in table.items():
        res += _to_bytes([i])
        res += _to_bytes([len(j)])
        res += str(int("".join([str(k) for k in j]), 2)).encode()
        res += b"\0"
    res += enc
    return res

def nextint(val,ind):
    k=b''
    while 1:
        if val[ind]:
            k+=_to_bytes([val[ind]])
        else:
            break
        ind+=1
    return (int(k),ind+1)
def decompress(inbytes):
    inbytes=_to_list(inbytes)
    rem=inbytes[0]
    it=1
    num,it=nextint(inbytes,it)
    table={}
    for i in range(num):
        val=inbytes[it]
        it+=1
        length=inbytes[it]
        it+=1
        k,it=nextint(inbytes,it)
        b=[ord(i)-ord('0') for i in ('{:0'+str(length)+'b}').format(k)][:length]
        table[val]=b
    return decode(table,inbytes[it:],rem)
def _compress_demo(args):
    infile=args.infile
    outfile=args.outfile
    with open(infile,'rb') as f:
        content=f.read()
    ccontent=compress(content)
    print('{} Bytes ---> {} Bytes'.format(len(content),len(ccontent)))
    print('Compression rate: {}%'.format(round(100.0*len(ccontent)/len(content),1)))
    with open(outfile,'wb') as f:
        f.write(ccontent)
    print('Done!')
def _decompress_demo(args):
    infile=args.infile
    outfile=args.outfile
    with open(infile,'rb') as f:
        content=f.read()
    ccontent=decompress(content)
    print('{} Bytes ---> {} Bytes'.format(len(content),len(ccontent)))
    with open(outfile,'wb') as f:
        f.write(ccontent)
    print('Done!')
def _script():
    ap=argparse.ArgumentParser()
    sp=ap.add_subparsers(help='Commands')
    cp=sp.add_parser(name='compress',help='Compress file')
    cp.add_argument('infile')
    cp.add_argument('outfile')
    cp.set_defaults(func=_compress_demo)
    dp=sp.add_parser(name='decompress',help='Decompress file')
    dp.add_argument('infile')
    dp.add_argument('outfile')
    dp.set_defaults(func=_decompress_demo)
    args=ap.parse_args()
    args.func(args)
__all__=['compress','decompress']
if __name__=='__main__':
    _script()