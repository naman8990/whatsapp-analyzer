import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    
    df=pd.DataFrame({'User_message':messages,'message_date':dates})
    df['message_date']=df['message_date'].str.replace("\u202f",'')
    
    df['message_date']=df['message_date'].str.replace(' - ','')
    df['message_date']=pd.to_datetime(df['message_date'],format="%m/%d/%y, %I:%M%p")
    
    users=[]
    messages=[]

    for message in df['User_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:#user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
            
    df['user']=users
    df['message']=messages
    
    df.drop(columns=['User_message'],inplace=True)
    
    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['day']=df['message_date'].dt.day
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute
    df['month_num']=df['message_date'].dt.month
    df['only_date']=df['message_date'].dt.date
    df['day_name']=df['message_date'].dt.day_name()
    
    period=[]
    for hour in df['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str("00")+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    
    return df