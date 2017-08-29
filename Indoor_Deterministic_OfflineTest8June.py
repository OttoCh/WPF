#offline Indoor deterministic system (fingerprinting)
#29 mei 2017
#Program ini dibuat untuk mengolah data offline hasil dari percobaan di selasar fisika
#Program ini akan menerima input dari file .txt dan juga referensi data RSSI posisi dari file .txt
#output yang dihasilkan berupa prediksi probabilitas posisi
#program ini tidak menghitung dengan menggunakan teknik triangulasi tetapi benar benar hanya membandingkan seperti pertama kali dilakukan ditambhakan bahwa bila test data di titik itu adalah 100 maka AP itu tidak dipakai dalam perhintungan

#Penulisan file untuk referensi adalah sesuai dengan AverageData_filename
#merubah 

import math
import itertools as itertools

AverageData_filename = "AverageData.txt"
TestData_filename = "TestData.txt"
Result_filename = "result.txt"

#Ref Data 6 posisi, 6 AP
#ini harusnya 6 total positionnya tapi tidak bisa karena array yg terbentuk jadi lebih kecil dari perkiraan (ada cap di sini)
totalPosition_X = 67
# ini digunakan unuk orientasi arah
totalPosition_Y = 1
totalAP = 4
#hitung ini kalkulator kombinasi
totalPossibleCombination = 1

#masukan maksimal sesungguhnya +1
MaximumXValue = 67
MaximumYValue = 1

#RefData = [[[0 for x in range(totalPosition_X)] for y in range(totalPosition_Y)] for z in range(0,10)]
RefData = [[[0 for x in range(totalAP)] for y in range(totalPosition_Y)] for z in range(totalPosition_X)]

#Realtime data. 8 AP
TestData = [0 for x in range(0,totalAP)]

#untuk menyimpan hasil perhitungan euclidian 
SquaredDeltaSignalResult = [[[0 for x in range(totalAP)] for y in range(totalPosition_Y)] for z in range(totalPosition_X)]

#0,55 karena kombinasi 3 sample dari 8 adalah 56
#untuk menyimpan hasil euclidian
ResultEuclidian = [0 for x in range(0,totalPossibleCombination)]

#untuk menyimpan hasil posisi
ResultPosition_X = [-1 for x in range(0,totalPossibleCombination)]
ResultPosition_Y = [-1 for x in range(0,totalPossibleCombination)]

#untuk menyimpan posisi tebakan 
MostLikelyPosition_X = [-1]
MostLikelyPosition_Y = [-1]

def ReadExistingData():
	readFile = open(AverageData_filename, "r")
	i=0
	j=0
	comment = False
	for line in readFile:
		#print line
		k=0
		#remove \n from string
		a = line.rstrip()
		#split by \t
		res = a.split("\t")
		for x in res:
			#print res
			if(x=='#'):
				comment = True	
				break
			else:
				#print(str(i) + " " + str(j) + " " + str(k))
				RefData[i][j][k] = float(x)
				k = k+1
		if(comment==False):
			i=i+1
		else:
			comment=False

def ReadTestData():
	readFile = open(TestData_filename, "r")
	comment = False
	for line in readFile:
		i=0
		#remove \n from string
		a = line.rstrip()
		#split by \t
		res = a.split("\t")
		for x in res:
			#print(str(i))
			#ganti posisi koordinat x setiap kali koordinat y sudah mencapai 6
			if(x=='#'):
				comment = True
				break
			else:
				TestData[i] = float(x)
				i = i+1
		#TestData[i] = TestData[i]/len(res)


def calculateAllPossibleCombination():
	AP = [0,1,2,3]
	combinar = 4
	m=0
	l=0
	for item in itertools.combinations(AP,combinar):
		currentExpectedPosition_X = -1
		currentExpectedPosition_Y = -1
		current_diftotal = 0
		minimum_diftotal = 1000	
		for i in xrange(0,MaximumXValue):
			for l in xrange(0,MaximumYValue):
				for j in item:
					if(TestData[j] != 100):
						current_diftotal += SquaredDeltaSignalResult[i][l][j]
				current_diftotal = math.sqrt(current_diftotal)
				print(str(i) + ": " + str(current_diftotal))
				if(current_diftotal<minimum_diftotal):
					minimum_diftotal = current_diftotal
					currentExpectedPosition_X = i
					currentExpectedPosition_Y = l
				if(current_diftotal==minimum_diftotal):
					print("====================")
		ResultEuclidian[m] = minimum_diftotal
		ResultPosition_X[m] = currentExpectedPosition_X
		ResultPosition_Y[m] = currentExpectedPosition_Y
		m+=1

def determinedProbabilityOfPosition():
	textFile = open(Result_filename, "a")
	textFile.write('\n')
	a = 0
	for i in ResultPosition_X:
		j = ResultPosition_Y[a]
		textFile.write("(" + str(i) + "," + str(j) + "); ")
		a+=1
	biggestResult = 0
	textFile.close()
	for x in xrange(0,MaximumXValue):
		for y in range(0,MaximumYValue):
			countAppearance = 0
			for k in range(0, totalPossibleCombination):
				if(x == ResultPosition_X[k]):
					if(y == ResultPosition_Y[k]):
						countAppearance += 1
			result = float(countAppearance)*100.0/float(totalPossibleCombination)
			if(biggestResult<result):
				biggestResult = result
				MostLikelyPosition_Y = y
				MostLikelyPosition_X = x
			if(result != 0):
				textFile = open(Result_filename, "a")
				textFile.write('\n' + "(" + str(x) + "," + str(y) + ") :" + '\t' + str(result) + "%")
				textFile.close()
	textFile = open(Result_filename, "a")
	textFile.write('\n' + "Predicted Position: (" + str(MostLikelyPosition_X) + "," + str(MostLikelyPosition_Y) + ")")
	textFile.close()
	print('\n' + "(" + str(MostLikelyPosition_X) + "," + str(MostLikelyPosition_Y) + ")")

def calculatePosition():
	#for x in range(totalPosition):
	for i in range(0,MaximumXValue):
		for j in range(0,MaximumYValue):
			for k in range(totalAP):
				total_dif=0
				#print(str(i) + " " + str(j) + " " + str(k))
				dif = euclidianDistance(RefData[i][j][k], TestData[k])
				SquaredDeltaSignalResult[i][j][k] = dif

def euclidianDistance(num1, num2):
	return (num1-num2)**2

def calculateAverageData(Data, j):
	jumlahData= len(Data)
	total = 0
	for x in Data:
		if(float(x)==0):
			x=100.0
		total += float(x)
	avg = total/jumlahData
	RealtimeData[j] = avg
	return

def writeTimestamp():
	import time
	import datetime
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	textFile = open(Result_filename, "a")
	textFile.write("\ntimestamp: " + st + '\n')
	textFile.close()

def Routine():
	ReadExistingData()
	ReadTestData()
	writeTimestamp()
	calculatePosition()
	calculateAllPossibleCombination()
	determinedProbabilityOfPosition()

Routine()