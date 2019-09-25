
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
H=hex(int(B, 2))
print H



f.close() # not indented, this happens after the loop