from process import *
import time
p1 = process('p1',1,5,5,3)  
p2 = process('p2',3,1,1,3)
p3 = process('p3',3,6,6,3)
p4 = process('p4',1,4,4,3)
processes = [p1,p2,p3,p4]
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


def MLFQ(processes,s=15):
    t = 0
    executing_order = []
    jobs_Total_Runtime = sum([i.running_time for i in processes])
    while t <= jobs_Total_Runtime:
        #######################-Filling the Queues-##############################################
        #priority1_Q is the highest priority queue
        #Only available to run jobs will be in priority queues
        priority1_Q = []
        priority2_Q = []
        priority3_Q = []
        if t % s == 0: #Rule No. 5 in MLFQ: after some time period S, move all the jobs in the system to the topmost queue
            for i in processes:
                if (i.arrival_time <= t) and (i.remaining_time > 0):
                    priority1_Q.append(i)
        else:
            for i in processes:
                if (i.arrival_time <= t) and (i.remaining_time > 0): #The job has started but not yet finished
                    if (i.priority == 1):
                        priority1_Q.append(i)
                    elif (i.priority == 2):
                        priority2_Q.append(i)
                    elif (i.priority == 3):
                        priority3_Q.append(i)
        ##########################################################################################
        ##########################-Executing the queues-##########################################
        if priority1_Q: #we might not need this, still pending a test
            #############################--RR-ing Q1--##############################
            y = executeQ(priority1_Q,priority2_Q,processes)
            executing_order.extend(y[0])
            t += y[1]
            ######################################################################
        if priority2_Q:
            #################--RR-ing Q2--############################
            priority2_Q.sort(key= lambda process:(process.arrival_time)) #for the list to actually be a queue
            for i in priority2_Q:
                if i.remaining_time > 0: #to be extra sure that the function has not yet finished to avoid negative remaining time values
                    if i.remaining_time == 1:
                        i.remaining_time -= 1
                        t += 1
                        #Since the process had only one second left, then, it must've finished 
                        priority2_Q.remove(i)
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if j.arrival_time == t: #the job has just entered the system, so logically it still has remaining time
                                priority1_Q.append(j)
                    else:
                        i.remaining_time -= 2
                        if i.remaining_time == 0:
                            #the job has finished, so it must be removed from the queue,
                            #this happens in one case where the remaining_time was exactly 2
                            priority2_Q.remove(i)
                        else: #the job has finished the time slice, but not yet has it finished
                            i.priority -= 1 #Rule 4 in MLFQ
                            priority3_Q.append(i)
                            priority2_Q.remove(i)
                        t +=2 #where 2 is the time slice value
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if (j.arrival_time == t) or (j.arrival_time == t-1): #the job has just entered the system, so logically it still has remaining time
                                priority1_Q.append(j)
                    if priority1_Q:
                        continue
                    to_be_executed = process(i.name,i.arrival_time,i.running_time,i.remaining_time,i.priority)
                    print(to_be_executed.name,"from part 2")
                    executing_order.append(to_be_executed)
            ###########################################################
        if priority3_Q:
            ###################--RR-ing Q3--###########################
            priority3_Q.sort(key= lambda process:(process.arrival_time)) #for the list to actually be a queue
            for i in priority3_Q:
                if i.remaining_time > 0: #to be extra sure that the function has not yet finished to avoid negative remaining time values
                    if i.remaining_time == 1:
                        i.remaining_time -= 1
                        t += 1
                        #Since the process had only one second left, then, it must've finished 
                        priority3_Q.remove(i)
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if j.arrival_time == t: #the job has just entered the system, so logically it still has remaining time
                                priority1_Q.append(j)
                    else:
                        i.remaining_time -= 2
                        if i.remaining_time == 0:
                            #the job has finished, so it must be removed from the queue,
                            #this happens in one case where the remaining_time was exactly 2
                            #print(i.name,priority2_Q)
                            priority3_Q.remove(i)
                        t +=2
                        #After incrementing time we need to check if a new job entered the system so we can append it to priority1_Q,
                        #due to rule 3 in MLFQ
                        for j in processes:
                            if (j.arrival_time == t) or (j.arrival_time == t-1): #the job has just entered the system, so logically it still has remaining time
                                priority1_Q.append(j)
                        if priority1_Q:
                            continue
                        to_be_executed = process(i.name,i.arrival_time,i.running_time,i.remaining_time,i.priority)
                        print(to_be_executed.name,"from part 3")
                        executing_order.append(to_be_executed)
            ###########################################################
        ########################################################################################
        else:
            t += 1
    print([i.name for i in executing_order])
    return executing_order

for i in MLFQ(processes):
    time.sleep(1)
    i.display()