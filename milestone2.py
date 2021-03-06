import yaml
from datetime import datetime
import _thread
import time
import threading
import pandas as pd
import operator
def printlog(task,path):
    sen=str(datetime.now())+";"+path+" Entry"
    lis.append(sen)
    if(task['Type']=="Task"):
        sen=str(datetime.now())+";"+path+" Executing "+task["Function"]+" ("+task["Inputs"]["FunctionInput"]+", "+task["Inputs"]["ExecutionTime"]+")"
        lis.append(sen)
        time.sleep(int(task["Inputs"]["ExecutionTime"]))
    else:
        flow_execution(task,path,1)
    sen=str(datetime.now())+";"+path+" Exit"
    lis.append(sen)
def printlog1(task,path):
    sen=str(datetime.now())+";"+path+" Entry"
    lis.append(sen)
    if(task['Type']=="Task"):
        if("Condition" not in task):
            sen=str(datetime.now())+";"+path+" Executing "+task["Function"]+" ("+task["Inputs"]["Filename"]+")"
            lis.append(sen)
            df=pd.read_csv(task["Inputs"]["Filename"])
            pt=path+".NoOfDefects"
            dic[pt]=len(df)
        else:
            condition=task["Condition"]
            cond=condition.split(" ")
            err=int(cond[2])
            con=cond[0]
            con=con[2:-1]
            print(con)
            print(dic)
            while(con not in dic):
                time.sleep(1)
            if((cond[1]=='<' and dic[con]<err) or (cond[1]=='>' and dic[con]>err)):
                sen=str(datetime.now())+";"+path+" Executing "+task["Function"]+" ("+task["Inputs"]["Filename"]+")"
                lis.append(sen)
                df=pd.read_csv(task["Inputs"]["Filename"])
                pt=path+".NoOfDefects"
                dic[pt]=len(df)
            else:
                sen=str(datetime.now())+";"+path+" Skipped"
                lis.append(sen)
    else:
        flow_execution(task,path,1)
    sen=str(datetime.now())+";"+path+" Exit"
    lis.append(sen)

def task_execution(data,path,ex):
    li=[]
    for i in range(len(data)):
        path1=path
        data1=data
        path1=path+'.'+list(data.keys())[i]
        data1=data[list(data.keys())[i]]
        if ex=="Concurrent":
            if("Function" not in data1):
                x=threading.Thread(target=printlog,args=(data1,path1))
                x.start()
                x.join()
            elif("Condition" in data1 or "Filename" in data1["Inputs"]):
                x1=threading.Thread(target=printlog1,args=(data1,path1))
                x1.start()
                li.append(x1)   
            else:
                x1=threading.Thread(target=printlog,args=(data1,path1))
                x1.start()
                li.append(x1)
        else:
            if("Function" not in data1):
                x=threading.Thread(target=printlog,args=(data1,path1))
                x.start()
                x.join()
            elif("Condition" in data1 or "Filename" in data1["Inputs"]):
                x=threading.Thread(target=printlog1,args=(data1,path1))
                x.start()
                x.join()
            else:
                x=threading.Thread(target=printlog,args=(data1,path1))
                x.start()
                x.join()
    for i in li:
        i.join()
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
            x=threading.Thread(target=printlog,args=(data,path))
            x.start()
            x.join()
    

global dic
f1= open("m2b1.txt","w+")
lis=[]
with open('G:\College\Code\KLA\Milestone2A.yaml') as ms1a:
    data = yaml.load(ms1a, Loader=yaml.FullLoader)
path=""
dic={}
if(data[list(data.keys())[0]]["Type"]=="Flow"):
    flow_execution(data,path,0)
for element in lis:
    f1.write(element + "\n")
f1.close()
            