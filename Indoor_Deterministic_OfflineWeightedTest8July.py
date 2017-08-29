#offline Indoor deterministic system (fingerprinting)
#8 Juli 2017
#Program ini dibuat untuk mengolah data offline hasil dari percobaan di saung fisika
#Program ini akan menerima input dari file .txt dan juga referensi data RSSI posisi dari file .txt
#output yang dihasilkan berupa posisi tepat dmn prediksinya berada
#program ini tidak menghitung dengan menggunakan teknik triangulasi tetapi benar benar hanya membandingkan seperti pertama kali dilakukan ditambhakan bahwa bila test data di titik itu adalah 100 maka AP itu tidak dipakai dalam perhintungan

#Penulisan file untuk referensi adalah sesuai dengan AverageData_filename
#program ini sudah dirubah dari versi sebelumnya sehingga bisa langsung mengolah semua yang adad di dalam TestData.txt tanpa perlu dikasi # lagi
#Progarm yang ini berbeda karena melakukan aplikasi weight dan digunakan untuk menghitung 2 jenis weight yang berbeda (lihat fungsi applyWeight dan Jurnal halaman 79)
#per 11 juli fungsi apply weight ditambah bagian untuk menghitung beban dengan persamaan garis lurus
#per 15 juli ditambah fungsi untuk menghitung bobot dengan 

import sys
import math
import itertools as itertools

AverageData_filename = "AverageData.txt"
TestData_filename = "TestData.txt"
Result_filename = "result.txt"
errorResult_filename = "errorResult.txt"

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

#Realtime data. 4 AP
TestData = [0 for x in range(0,totalAP)]
TestDataPosition = [-1]

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

#beban 
weightData = [-1 for x in range(0, totalAP)]

#untuk logika skip perhitungan terhadap posisi tertentu
skipNumb = 1

#untuk membedakan RSSI di test data dan posisi
totalRSSIatTestData = 4

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

def ReadTestData(res):
	i=0
	for x in res:
		if(i==totalRSSIatTestData):
			TestDataPosition[0] = int(x)
			break
		TestData[i] = float(x)
		i = i+1

# def determineWeight():
	#untuk menentukan dengan menggunakan metode yg linear
# 	totalRSSI = 0
# 	for x in range(0, totalRSSIatTestData):
# 		if(TestData[x] != 100):
# 			totalRSSI += TestData[x]
# 	init_maxWeight = 0
# 	init_minWeight = 1000
# 	for x in range(0, totalRSSIatTestData):
# 		if(TestData[x] != 100):
# 			weightData[x] = TestData[x]/totalRSSI
# 			if(weightData[x] > init_maxWeight):
# 				init_maxWeight = weightData[x]
# 			if(weightData[x] < init_minWeight):
# 				init_minWeight = weightData[x]
# 	maxWeightval = 0.9
# 	minWeightval = 0.1
# 	for x in range(0, totalRSSIatTestData):
# 		if(TestData[x] != 100):
# 			weightData[x] = (weightData[x]-init_maxWeight)/(init_minWeight - init_maxWeight) * (minWeightval - maxWeightval) + maxWeightval

def determineWeight():
 	#untuk menentukan dengan menggunakan metode yang pathloss
 	a = [-2.985, -2.092, -2.446, -2.494]
 	b = [-9.747, -5.796, -11.85, -13.76]
 	do = [65, 65, 100, 100]
 	sumWeight = 0
 	for x in range(0, totalRSSIatTestData):
 		if(TestData[x] != 100):
 			z = (-TestData[x]-b[x]+100)/(10*a[x])
 			print "var===================================="
 			print z
 			weightData[x] = (do[x]*10**z)/do[x]
 			print weightData[x]
 			sumWeight += weightData[x]
 	for x in range(0, totalRSSIatTestData):
 		if(TestData[x] != 100):
 			weightData[x] = weightData[x]/sumWeight
 	return
 		


def applyWeight(i, l, j):
	#weightData = [0.404, 0.380, 0.252, 0.800]
	print("j: " + str(j) + " " + str(weightData[j]))
	return SquaredDeltaSignalResult[i][l][j]*weightData[j]
	#return SquaredDeltaSignalResult[i][l][j]*(1-weightData[j])

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
		determineWeight()
		for i in xrange(0,MaximumXValue):
			for l in xrange(0,MaximumYValue):
				for j in item:
					if(TestData[j] != 100):
						SquaredDeltaSignalResult[i][l][j] = applyWeight(i,l,j)
						current_diftotal += SquaredDeltaSignalResult[i][l][j]
				#print("current_diftotal before sqrt: " + str(current_diftotal))
				current_diftotal = math.sqrt(current_diftotal)
				#print(str(i) + ": " + str(current_diftotal))
				if(current_diftotal<minimum_diftotal):
					minimum_diftotal = current_diftotal
					currentExpectedPosition_X = i
					currentExpectedPosition_Y = l
				current_diftotal = 0
				#if(current_diftotal==minimum_diftotal):
					#print("====================")
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
				MostLikelyPosition_Y[0] = y
				MostLikelyPosition_X[0] = x
			if(result != 0):
				textFile = open(Result_filename, "a")
				textFile.write('\n' + "(" + str(x) + "," + str(y) + ") :" + '\t' + str(result) + "%")
				textFile.close()
	textFile = open(Result_filename, "a")
	textFile.write('\n' + "Predicted Position: (" + str(MostLikelyPosition_X) + "," + str(MostLikelyPosition_Y) + ")")
	textFile.close()
	print('\n' + "Most likely Pos: (" + str(MostLikelyPosition_X) + "," + str(MostLikelyPosition_Y) + ")")

def calculatePosition():
	#for x in range(totalPosition):
	for i in range(0,MaximumXValue):
		for j in range(0,MaximumYValue):
			for k in range(totalAP):
				total_dif=0
				#print(str(i) + " " + str(j) + " " + str(k))
				dif = euclidianDistance(RefData[i][j][k], TestData[k])
				SquaredDeltaSignalResult[i][j][k] = dif
				#if(i+1 == TestDataPosition[0] and i % skipNumb == 0):
				#	SquaredDeltaSignalResult[i][j][k] = 100000

def calculateErrorPosition():
	textFile = open(errorResult_filename, "a")
	textFile.write('\n' + str(MostLikelyPosition_X[0]+1) + '\t' + str(TestDataPosition[0]))
	errorDifference = abs(MostLikelyPosition_X[0]+1 - TestDataPosition[0])
	textFile.write('\t' + str(errorDifference))

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
	readFile = open(TestData_filename, "r")
	for line in readFile:
		#remove \n from string
		a = line.rstrip()
		#split by \t
		res = a.split("\t")
		if(res[0] != '#'):
			ReadTestData(res)
			writeTimestamp()
			calculatePosition()
			calculateAllPossibleCombination()
			determinedProbabilityOfPosition()
			calculateErrorPosition()

if(len(sys.argv) > 1):
	skipNumb = int(sys.argv[1])

Routine()