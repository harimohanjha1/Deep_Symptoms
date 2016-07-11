import shutil
import os

#a function to ckeck if directory exists
def mk_dir(directory):
	#print "yes"
	if os.path.isdir(directory):
		print (directory+" exists")
		return
	else: 
		os.makedirs(directory)
		return

#function  to copy images 

def copy(list,source):
	destination=["train_set","valid_set","test_set"]
	print destination

	for k in destination:
		#print k
		mk_dir(k)

		if k=="train_set":
			for i in range(int(0.75*len(a))):
				shutil.copy(str(source)+"/"+str(list[i]),k)


		if k=="valid_set":
			for i in range(int(0.75*len(a)),int(.9*len(a))):
				shutil.copy(str(source)+"/"+str(list[i]),k)

		if k=="test_set":
			#print int(0.85*len(a)),len(a)

			for i in range(int(0.9*len(a)),len(a)):
				shutil.copy(str(source)+"/"+str(list[i]),k)

		
	return

print "program is on"

list=["Normal","Hemorrhage","Lesion","Tesselated"]
print list

for i in list:
	print i
	a=os.listdir(i)
	#print a
	#print len(a)
	copy(a,i)
