import yaml
from datetime import datetime
import _thread
import time
def printlog(task,path):
    print(datetime.now(),";",path," Entry",sep='')
    if(task['Type']=="Task"):
        print(datetime.now(),";",path," Executing ",task["Function"]," (",task["Inputs"]["FunctionInput"],", ",task["Inputs"]["ExecutionTime"],")",sep='')
        time.sleep(int(task["Inputs"]["ExecutionTime"]))
    else:
        flow_execution(task,path,1)
    print(datetime.now(),";",path," Exit",sep='')
def task_execution(data,path,ex):
    for i in range(len(data)):
        path1=path
        data1=data
        path1=path+'.'+list(data.keys())[i]
        data1=data[list(data.keys())[i]]
        if ex=="Concurrent":
            _thread.start_new_thread(printlog(data1,path1))
        else:
            printlog(data1,path1)

def flow_execution(data,path,n):
    ex=""
    if n==0:
        path=path+list(data.keys())[0]
        data=data[list(data.keys())[0]]
    else:
        ex=data["Execution"]
        data=data["Activities"]
        task_execution(data,path,ex)
    if(data["Type"]=="Flow"):
        printlog(data,path)

with open('G:\College\Code\KLA\Milestone1A.yaml') as ms1a:
    data = yaml.load(ms1a, Loader=yaml.FullLoader)
path=""
if(data[list(data.keys())[0]]["Type"]=="Flow"):
    flow_execution(data,path,0)
            