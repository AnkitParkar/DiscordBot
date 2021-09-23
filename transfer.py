import csv
import datetime

mega_list=[]

def current_datetime():
    x = datetime.datetime.now()
    date=x.strftime("%d")+"/"+x.strftime("%m")
    return date

name="count.csv"

def read_csv():
    print("reading")
    with open(name,'r') as file:
        r=csv.reader(file)
        for row in r:
            mega_list.append(row)
            

def write_csv():
    print("Writing")
    with open(name,'w',newline='') as file:
        wr=csv.writer(file)
        for i in mega_list:
            wr.writerow(i.copy())
        

def add_name(channel,user):
    print(f"Add_name {channel} {user}")
    for i in range(0,len(mega_list)):
        if mega_list[i][0]==channel:
            print(mega_list[i])
            mega_list[i].append(user)
            print(mega_list[i])
            
    
def recieve_from_discord(channel,user):
    #dt=current_datetime()
    #print(dt)
    read_csv()
    add_name(channel,user)
    write_csv()
    mega_list.clear()
    
#recieve_from_discord('publicity','Ankit')

    