import yaml
from datetime import datetime
import _thread
import time
def printlog(task,path):
    sen=str(datetime.now())+";"+path+" Entry"
    f1.write(sen)
    if(task['Type']=="Task"):
        sen=str(datetime.now())+";"+path+" Executing "+task["Function"]+" ("+task["Inputs"]["FunctionInput"]+", "+task["Inputs"]["ExecutionTime"]+")"
        f1.write(sen)
        time.sleep(int(task["Inputs"]["ExecutionTime"]))
    else:
        flow_execution(task,path,1)
    sen=str(datetime.now())+";"+path+" Exit"
    f1.write(sen)
def task_execution(data,path,ex):
    for i in range(len(data)):
        path1=path
        data1=data
        path1=path+'.'+list(data.keys())[i]
        data1=data[list(data.keys())[i]]
        if ex=="Concurrent":
            _thread.start_new_thread(printlog,(data1,path1))
        else:
            printlog(data1,path1)

def flow_execution(data,path,n):
    ex=""
    data1=data
    path1=path
    count=0
    if n==0:
        path=path+list(data.keys())[0]
        data=data[list(data.keys())[0]]
    else:
        ex=data["Execution"]
        data=data["Activities"]
        task_execution(data,path,ex)
        count=1
    if(count==0):
        if(data["Type"]=="Flow"):
            printlog(data,path)

f1= open("m1a.txt","w+")
with open('G:\College\Code\KLA\Milestone1A.yaml') as ms1a:
    data = yaml.load(ms1a, Loader=yaml.FullLoader)
path=""
if(data[list(data.keys())[0]]["Type"]=="Flow"):
    flow_execution(data,path,0)
f1.close()
            