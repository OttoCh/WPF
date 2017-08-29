#WiFi Based Positioning Algorithm 1
filename = "Data2.txt"

info = {}
mydata = []
mydata.append([])
mydata.append([])
mydata.append([])
mydata.append([])
mydata.append([])
#mydata.append([])
#mydata.append([])
#mydata[0].append('')
#mydata[1].append('')
#mydata[2].append('')
#mydata[3].append([])
#mydata[4].append([])
#mydata[5].append([])
#mydata[6].append([])

with open(filename) as Data_text:
	j=0
	for line in Data_text:
		Z, A = line.split('\t',1)
		#print A
		B = [item.strip() for item in A.split('\t')]
		i=0
		for x in B:
			#print i, " ", B[i]
			mydata[j].append(int(B[i]))
			i+=1
		j+=1

i=0
for x in mydata:
	print(mydata[i])
	i+=1
