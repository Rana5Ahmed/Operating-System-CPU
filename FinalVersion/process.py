class process:
    def __init__(self,name, arrival_time, running_time,remaining_time, priority, IO_time,IO_start):
        self.name=name
        self.arrival_time=arrival_time
        self.running_time=running_time
        self.remaining_time=remaining_time
        self.priority=priority
        self.IO_time = IO_time
        self.IO_start = IO_start
    def display(self):
        print(f'''Process name: {self.name}\tArrival time: {self.arrival_time}\tRunning time: {self.running_time}\tRemaining time: {self.remaining_time}\tPriority: {self.priority}\t''')
    def get_process(self):
        return [self.name, self.arrival_time, self.running_time,
                self.remaining_time,self.priority]
    
        

