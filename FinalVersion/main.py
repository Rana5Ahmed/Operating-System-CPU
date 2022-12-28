from Scheduling import *
import sys
p1 = process('A',1,5,5,3,4,2)  
p2 = process('B',3,2,2,3,2,1)
p3 = process('C',3,6,6,3,3,4)
p4 = process('D',2,4,4,3,3,3)
# p4 = process('D',1,1,1,3,3,3)
processes = [p1,p2,p3,p4]
def gantt_nonpre(p):
    counter=0
    print("========================================")
    for i in range(len(p)):
        # print(f"process: {p[i]}")
        for j in range(len(p[i])-1):
            print(p[i][j],end='')
            time.sleep(1)
        counter += p[i][-1]
        print("\n"+' '*counter,end='')
    print("\n========================================")





def gantt_RR(data):
    print("========================================")
    counter =0
    # print(data)
    last_p=data[0]
    # print(last_p)
    for i in data:
        # print(i)
        if i[0] == last_p:
            print(i[0],end='')
            time.sleep(1)
            counter +=1
        else:
            print("\n"+' '*counter,end='')
            last_p=i[0]
            print(last_p,end='')
            counter +=1
    # print(f"data = {data}")
    print("\n========================================")

def main():
    while True:
        
        print('\033[94m' + '-'*75)
        print('FCFS = 1 | SJF = 2 | STCF = 3 | RR = 4 | MLFQ = 5 | Quit = 0')
        print('-'*75 + '\033[0m')
        
        try:
            pass
            mode = int(input('Enter: '))
        except Exception as error:
            print('\033[93m' + 'Error: Wrong Input!')
            sys.exit(-1)
        if mode==1:
            print("FIFO:")
            time.sleep(1)
            gantt_nonpre(FIFO(processes))
        elif mode==2:
            print("SJF:")
            time.sleep(1)
            gantt_nonpre(SJF(processes))
        elif mode==3:
            print("STCF:")
            time.sleep(1)
            for i in STCF(processes):
                if(i.running_time - i.remaining_time) == i.IO_start:
                    print(i.name,'i'*i.IO_time,end=' ')
                else:
                    print(i.name,end=' ')
        elif mode==4:
            n=int(input("Enter time slice size: "))
            print("RR:")
            time.sleep(1)
            # for i in newRR(processes):
                # print(i,end=" ")
            processescpy=processes.copy()
            data = newRR(processescpy,n)
            gantt_RR(data.copy())
        elif mode==5:
            for i in MLFQ(processes):
                print(i,end=" ") 
        elif mode ==0:
            sys.exit()
        else:
            print("Wrong option ya sahby !")
        time.sleep(1)



main()