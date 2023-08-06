import sys
class Tree(object):
    def __init__(self,l,r,val,dat):
        self.l=l
        self.r=r
        self.val=val
        self.dat=dat
    def __repr__(self):
        return ('Tree('+repr(self.l)+','+repr(self.r)+')')
    def __str__(self):
        return ('Tree('+str(self.l)+','+repr(self.r)+')')
class BitStream(object):
    def __init__(self):
        self.bits=[]
    def add(self,bits):
        self.bits+=bits
    def _to_bytes(self,c):
        if sys.version_info.major>2:
            return bytes(c)
        else:
            return ''.join([chr(i) for i in c])
    def tobytes(self):
        res=b''
        cache=[]
        for i in self.bits:
            cache.append(str(i))
            if len(cache)==8:
                res+=self._to_bytes([int(''.join(cache),2)])
                cache=[]
        remain=8-len(cache)
        for i in range(8-len(cache)):
            cache.append('0')
        res += self._to_bytes([int(''.join(cache), 2)])
        return (res,remain)
class DeBitStream(object):
    def __init__(self,data):
        self.data,self.remain=data
    def _to_list(self,data):
        if sys.version_info.major>2:
            return list(data)
        else:
            return data
    def _to_bits(self,val):
        k=128
        l=[]
        for i in range(8):
            l.append(int(bool(val&k)))
            k>>=1
        return l
    def tobits(self):
        l=sum([self._to_bits(i) for i in self._to_list(self.data)],[])
        for i in range(self.remain):
            l.pop()
        return l
class Translator(object):
    def __init__(self,d):
        self.d=d
    def translate(self,data):
        bs=BitStream()
        for i in data:
            bs.add(self.d[self._to_int(i)])
        return bs.tobytes()

    def _to_bytes(self, c):
        if sys.version_info.major > 2:
            return bytes(c)
        else:
            return ''.join([chr(i) for i in c])
    def _to_int(self,c):
        return c
    def detranslate(self,data,remain):
        d=DeBitStream((data,remain))
        bits=d.tobits()
        Bytes=[]
        def startswith(a,b):
            return a[:len(b)]==b
        while bits:
            for i,j in self.d.items():
                if startswith(bits,j):
                    del bits[:len(j)]
                    Bytes.append(i)
                    break
        return self._to_bytes(Bytes)