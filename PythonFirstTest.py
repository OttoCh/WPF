#Python First Test
#Program to open file text and turn it into array
#http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

#import 

print "Hello world"

filename = "Data.txt"

#Ini hanya untuk open saja
#lengkapnya open(filename, mode) dengan mode adalah pemisahnya
#Data_text = open(filename)
#print Data_text

#untuk Read file
#ada juga .readline() (untuk 1 line), read()
#Data_text = open(filename)
#print Data_text.readlines()

#untuk read file dengan 'with' dan langsung proses data
#http://stackoverflow.com/questions/13521397/extract-data-from-lines-of-a-text-file
info = [(1,2), (3,4)]

print info[1][0]

