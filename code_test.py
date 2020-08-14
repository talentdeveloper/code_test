import mysql.connector
import requests
from bs4 import BeautifulSoup
import time
import threading
flag=False
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="http_status"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("SELECT * FROM status where status='NEW'")
myresult = mycursor.fetchall()
def get_url(url):
    global flag    
    t_url=url[1]
    print(t_url)
    while flag:
        time.sleep(0.05)
    flag=True
    sql = 'UPDATE status SET status="PROCESSING" WHERE id="'+str(url[0])+'"'     
    update=mycursor.execute(sql)
    mydb.commit()
    flag=False
    status=""
    code=""
    try:
        page = requests.get(t_url)
        code=str(page.status_code)
        status="DONE"
    except:
        code="ERROR"
        status="ERROR"
    while flag:
        time.sleep(0.05)
    flag=True
    sql = 'UPDATE status SET status="'+status+'", http_code="'+code+'" WHERE id="'+str(url[0])+'"' 
    update=mycursor.execute(sql)
    mydb.commit()
    flag=False
def thread_function():
    global myresult
    threads = [threading.Thread(target=get_url, args=(url, )) for url in myresult]
    for thread in threads:
        thread.start()
        if threading.active_count() == 10:
            thread.join()
thread_function()

    


