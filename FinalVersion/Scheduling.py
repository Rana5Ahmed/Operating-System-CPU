from process import *
import time
#Scheduling algorithms:

#First Come First Served => queue
# Job FCFS(List of Jobs):
#Sort them ascendingly by arrival time
#Run one by one through completion
#We don't need actual queues if we implement in python
def FIFO(processes):
    executing_order = []
    processes.sort(key=lambda process: (process.arrival_time))
    for i in processes:
        executing_order.append([i.name*i.IO_start,'i'*i.IO_time,i.name*(
            i.running_time - i.IO_start),i.IO_time+i.running_time])
    return executing_order #executing order here is a list of lists, every inner list contains the executing scenario of one project


#Shortest Job First => 
# Job SJF(List of Jobs):
#Sort them ascendinlgy based on 2 keys, arrival time then running time
#Run one by one through completion
def SJF(processes):
    executing_order = []
    processes.sort(key=lambda process: (process.arrival_time,process.running_time))
    for i in processes:
        executing_order.append([i.name*i.IO_start,'i'*i.IO_time,i.name*(
            i.running_time - i.IO_start),i.IO_time+i.running_time])
    return executing_order


#Shortest Remaining Time First => SJF with preemption
# Job STCF(List of Jobs):
#it's triggered anytime a new job enters the system
#Since the jobs are a preset dataset
#we need a variable that incremnts every second to check time so we can activate preemption
def STCF(processes):
    t = 0
    executing_order = []
    #executing_order_names = []
    jobs_Total_Runtime = sum([i.running_time for i in processes])
    jobs_total_IO_time = sum([i.IO_time for i in processes])
    while t <= (jobs_Total_Runtime):
        available_to_run = []
        for i in processes:
            if (i.arrival_time <= t) and (i.remaining_time > 0): #the job has started but not yet finished
                    available_to_run.append(i)
        if available_to_run:
            to_be_executed = min(available_to_run,key=lambda process:process.remaining_time)
            to_be_executed.remaining_time -= 1
            toBeExecuted = process(to_be_executed.name,to_be_executed.arrival_time,to_be_executed.running_time,to_be_executed.remaining_time,to_be_executed.priority,to_be_executed.IO_time,to_be_executed.IO_start)
            executing_order.append(toBeExecuted)
            #executing_order_names.append(to_be_executed.name)
        t += 1
    
    return executing_order


#Round Robin => Time slices
'''def oldRR(processes,quantum=2):
    t = 0
    executing_order = []
    jobs_Total_Runtime = sum([i.running_time for i in processes])
    while t <= jobs_Total_Runtime: # might need modification
        available_to_run = []
        for i in processes:
            if (i.arrival_time <= t) and (i.remaining_time > 0):
                available_to_run.append(i)
        if available_to_run:
            available_to_run.sort(key=lambda process:(process.arrival_time))
            for i in available_to_run:
                if i.remaining_time >= quantum:
                    i.remaining_time -= quantum
                    t += quantum
                else:
                    i.remaining_time -= 1
                    t += 1
                to_be_executed = process(i.name,i.arrival_time,i.running_time,i.remaining_time,i.priority,i.IO_time,i.IO_start)
                executing_order.append(to_be_executed)
        else:
            t += 1
    return executing_order'''

def newRR(processes,quantum=2):
    t = 0
    executing_order = []
    jobs_Total_Runtime = sum([i.running_time for i in processes])
    while t <= jobs_Total_Runtime: # might need modification
        available_to_run = []
        for i in processes: 
            if (i.arrival_time <= t) and (i.remaining_time > 0): #the job has started but not yet finished
                available_to_run.append(i)
        if available_to_run:
            available_to_run.sort(key=lambda process:(process.arrival_time))
            for i in available_to_run:
                quantum_count = 0
                while (i.remaining_time > 0) and (quantum_count < quantum):
                    if ((i.running_time - i.remaining_time) == i.IO_start):
                        executing_order.append('i'*i.IO_time)
                        i.IO_start = -1
                        break
                    else:
                        i.remaining_time -= 1
                        t += 1
                        executing_order.append(i.name)
                        quantum_count += 1
                        if ((i.running_time - i.remaining_time) == i.IO_start):# and (ran_time < (i.IO_start+i.IO_time)): #the job is performing I/O
                            executing_order.append('i'*i.IO_time)
                            i.IO_start = -1
                            break
                        
        else:
            t += 1
    return executing_order
def MLFQ(processes,s=15):
    global executing_order,t
    quantum1,quantum2,quantum3 = 2,3,4
    jobs_Total_Runtime = sum([i.running_time for i in processes])
    priority1_Q = []
    priority2_Q = []
    priority3_Q = []
    while t <= jobs_Total_Runtime:
        #######################-Filling the Queues-##############################################
        #priority1_Q is the highest priority queue
        #Only available to run jobs will be in priority queues
        if t % s == 0: #Rule No. 5 in MLFQ: after some time period S, move all the jobs in the system to the topmost queue
            for i in processes:
                if (i.arrival_time <= t) and (i.remaining_time > 0):
                    priority1_Q.append(i)
       
        for process in processes:
            #print(process.arrival_time,t)
            #print(process.remaining_time,process.running_time)
            if (process.arrival_time <= t) and (process.remaining_time == process.running_time):
                priority1_Q.append(process)
        
        def RR(processes,quantum):
            global t,executing_order
            available_to_run = []
            for i in processes: 
                if (i.arrival_time <= t) and (i.remaining_time > 0): #the job has started but not yet finished
                    available_to_run.append(i)
            if available_to_run:
                available_to_run.sort(key=lambda process:(process.arrival_time))
                for i in available_to_run:
                    quantum_count = 0
                    while (i.remaining_time > 0) and (quantum_count < quantum):
                        if ((i.running_time - i.remaining_time) == i.IO_start):
                            executing_order.append('i'*i.IO_time)
                            i.IO_start = -1
                            break
                        else:
                            i.remaining_time -= 1
                            t += 1
                            executing_order.append(i.name)
                            quantum_count += 1
                            if quantum != 2:
                                for process in processes:
                                    if (process.arrival_time <= t) and (process.remaining_time == process.running_time):
                                        priority1_Q.append(process)
                            if ((i.running_time - i.remaining_time) == i.IO_start):# and (ran_time < (i.IO_start+i.IO_time)): #the job is performing I/O
                                executing_order.append('i'*i.IO_time)
                                i.IO_start = -1
                                break
                    else:
                        if i.remaining_time != 0:
                            if quantum == 2:
                                priority2_Q.append(i)
                            elif quantum == 3:
                                priority3_Q.append(i)
                            processes.remove(i)
                    if priority1_Q and quantum != 2:
                        RR(priority1_Q,quantum1)
        if priority1_Q:
            RR(priority1_Q,quantum1)
        if priority2_Q:
            RR(priority2_Q,quantum2)
        if priority3_Q:
            RR(priority3_Q,quantum3)
        else:
            t += 1
            
                        
    return executing_order
#######################################################################################
# Main()
p1 = process('A',1,5,5,3,4,2)  
p2 = process('B',3,2,2,3,2,1)
p3 = process('C',3,6,6,3,3,4)
p4 = process('D',1,4,4,3,3,3)
processes = [p1,p2,p3,p4]

# for i in newRR(processes):
    # print(i,end=" ")
############################################################################



#MLFQ(processes)
#• Rule 1: If Priority(A) > Priority(B), A runs (B doesn’t). 
#• Rule 2: If Priority(A) = Priority(B), A & B run in RR. 
#• Rule 3: When a job enters the system, it is placed at the highest priority (the topmost queue). 
#• Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times it has given up the CPU), 
# its priority is reduced (i.e., it moves down one queue). 
#• Rule 5: After some time period S, move all the jobs in the system to the topmost queue

def executeQ(theQueue,the_Other_Queue,processes):
    t = 0
    executing_order = []
    for i in theQueue:
                theQueue.sort(key= lambda process:(process.arrival_time)) #for the list to actually be a queue
                if i.remaining_time > 0: #to be extra sure that the job has not yet finished to avoid negative remaining_time values
                    if i.remaining_time == 1:
                        i.remaining_time -= 1
                        t += 1
                        #Since the process had only one second left, then, it must've finished 
                        theQueue.remove(i)
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if j.arrival_time == t: #the job has just entered the system, so logically it still has remaining time
                                theQueue.append(j)
                    else:
                        i.remaining_time -= 2
                        if i.remaining_time == 0:
                            #the job has finished, so it must be removed from the queue,
                            #this happens in one case where the remaining_time was exactly 2
                            theQueue.remove(i)
                        else: #the job has finished the time slice, but not yet has it finished
                            i.priority -= 1 #Rule 4 in MLFQ
                            the_Other_Queue.append(i)
                            theQueue.remove(i)
                        t +=2 #where 2 is the time slice value
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if (j.arrival_time == t) or (j.arrival_time == t-1): #the job has just entered the system, so logically it still has remaining time
                                theQueue.append(j)
                    to_be_executed = process(i.name,i.arrival_time,i.running_time,i.remaining_time,i.priority)
                    print(to_be_executed.name,"from part 1")
                    executing_order.append(to_be_executed)
    return executing_order,t

executing_order = []
t = 0

'''for i in MLFQ(processes):
        time.sleep(1)
        i.display()'''
#The process object must have the following fields:
#Arrival time
#Running time needed by CPU
#remaining time
#Priorirty

#files will be in csv not text