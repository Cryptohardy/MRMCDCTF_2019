# MRMCDCTF_2019
CTF
#PRP - MRMCDCTF 2019


In this challenge (prp.py) , we have flag bit , size of flag (352 (44 bytes)): 
```python
def flag_bit(idx):

    return (flag[idx//8]>>(idx%8))&1


```
```python
def print_help():
    stdout.write("""Welcome player. 
This is the SPRP game. Long story short:
You can:
Tell me which bit of the flag we are playing over:
    f<num between 0 and %d>
Ask me to encrypt a message:
    e<32 bytes in hex>
Ask me to decrypt a message:
    d<32 bytes in hex>
    """%(len(flag)*8))

```

The flag bit is used to control the input to either ideal cipher (1) or Feistel (0). The Feistel output is completely random , so the array of 352 bit is grouped into 44 bytes __(idx//8)__ 


##First step
generate 352 flag with one input and sent to the server.
```python
for i in range(0,352):
	print "f", str(i)
	#print "e 0000000000000000000000000000000000000000000000000000000000000000"
	print "e 0000000000000000000000000000000000000000000000000000000000000001"
```
##Second step

I pasred the server response and collected the 352 bit 

```python
f = open( 'server_output.txt' , 'r' )

A=[]
for line in f.readlines() :
	if "ok we are now playing for bit:" in line:
		S= line[line.index(":")+1:]

	else:
		#if "0000000000000000000000000000000000000000000000000000000000000000" in line:
		if "00000000000000000000000000000000" in line:
			
			A.append(0)
		else:
			A.append(1)



print A , len(A);

B=''.join(str(e) for e in A)
print B

print hex(int(B, 2))

f.close() # not indented, this happens after the loop

```

However , the server output is 
0xb24ab2c2224c0c8c9cde4eaa429efa4eae429afa4aae469efa322cc2d60c6266faea2cacfa4e8c9c12ec84beL

it did not decode 
i did reverse the bits 

```python
flag=[0xb2,0x4a,0xb2,0xc2,0x22,0x4c,0x0c,0x8c,0x9c,0xde,0x4e,0xaa,0x42,0x9e,0xfa,0x4e,0xae,0x42,0x9a,0xfa,0x4a,0xae,0x46,0x9e,0xfa,0x32,0x2c,0xc2,0xd6,0x0c,0x62,0x66,0xfa,0xea,0x2c,0xac,0xfa,0x4e,0x8c,0x9c,0x12,0xec,0x84,0xbe]


def reverse_bit(num):
    result = 0
    while num:
        result = (result << 1) | (num & 1)
        num >>= 1
    return result

Y=[]
for u in range(0, len(flag)):
    Y.append(int('{:08b}'.format(flag[u])[::-1], 2))


S=''.join('{:02x}'.format(x) for x in Y)
print S
print S.decode('hex')
```
__(
4d524d4344323031397b725542795f727542595f527562795f4c34436b3046665f5734355f7231394837217d
MRMCD2019{rUBy_ruBY_Ruby_L4Ck0Ff_W45_r19H7!}
)__


