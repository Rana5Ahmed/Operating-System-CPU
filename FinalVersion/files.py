# Python program to demonstrate
# writing to CSV
import csv
from process import process
	
# field names
head = ['Name', 'Arrival time', 'Running time', 'remaining time','Priorirty']


def access_file(file):
    try:
        open(file, 'r')
        file.close()
    except:
        with open(file, 'w') as csvfile:
        	# creating a csv writer object
        	csvwriter = csv.writer(csvfile,lineterminator='\n',delimiter=',',quotechar='/')
        	# writing the Header
        	csvwriter.writerow(head)
    	
 
		

def write_process(process,file):
    with open(file, 'a') as csvfile:
    	# creating a csv writer object
    	csvwriter = csv.writer(csvfile,lineterminator='\n',delimiter=',',quotechar='/')
    	csvwriter.writerow(process.get_process())
    
        