<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### Usage
```python
from pyhuff import compress
text=b'A'*100
print(text) # b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
comp=compress(text)
print(comp) # b'\x041\x00A\x010\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

Or use:
```commandline
pyhuff compress in.txt out.bin
pyhuff decompress out.bin dec.txt
```

### Disadvantages

1. The code is very messy because of compatibility of Python 2 (And I don't know the six package).
2. Decompression is very slow.
3. Not very good, sometimes the compressed file is larger than the original one. 