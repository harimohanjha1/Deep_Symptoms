import os
import sys

def createlabels(dirname):
	
	list_train=["N","H","L","T"]
	a=os.listdir(dirname)

	#condition to output labels and image names in a differnt text file
	if dirname=="train_set":
		filename  = open("train_labels.txt",'w')
		sys.stdout = filename

	if dirname=="test_set":
		filename  = open("test_labels.txt",'w')
		sys.stdout = filename

	if dirname=="valid_set":
		filename  = open("val_labels.txt",'w')
		sys.stdout = filename
	
	#printing required headerss
	
	#loop to assign differnt labels:NPDR is 1,PDR is 2,normal is 0	
	count_0=0
	count_1=0
	count_2=0

	for j in a:
		if j[0]==list_train[0]:
			#print "N",j
			#dirname.append(1)
			print j," "+"0"

		if j[0]==list_train[1]:
			#print "P",j
			#dirname.append[(2)
			print j," "+"1"

		if j[0]==list_train[2]:
			print j," "+"2"
			#print "n",j
			#dirname.append(0)
		if j[0]==list_train[3]:
			print j," "+"3"
	
list=["train_set","test_set","valid_set"]
#calling the function
for i in list :

	createlabels(i)
