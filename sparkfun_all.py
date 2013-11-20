import requests
from BeautifulSoup import BeautifulSoup 
import re
import json
from pprint import pprint
import ntplib
from time import ctime
import datetime

last_read=0
try:
  start=datetime.datetime.now()
  #NTP for file storage
  c = ntplib.NTPClient()
  response = c.request('europe.pool.ntp.org', version=3)
  curr_time=ctime(response.tx_time)

  #Fetch the main page
  main='https://www.sparkfun.com/products.json'
  print 'Fetching Main Page'
  raw = requests.get(main,timeout=20)
  raw_json=json.loads(raw.text)

  #for item in raw_json:
  length=len(raw_json)
  for i in range(0,length):

    item=raw_json[i]
    #Decode product data from JSON
    pdt_url=item['url_json']
    pdt_id=item['id']
    pdt_name=item['name']
    pdt_link=item['url']
    print i+1,"of",length,":",pdt_id,pdt_name
    
    #Fetch product's JSON Page
    pdt_page=requests.get(pdt_url,timeout=5)
    pdt_json=json.loads(pdt_page.text)
    pdt_qty=pdt_json['quantity']
    
    #Store it in a file
    f_name=str(pdt_id)+".csv"
    f=open(f_name,"a")
    f.write(str(pdt_qty)+';'+str(curr_time)+'\n')
    f.close()
    last_read=pdt_id
except ValueError:	#Handle for wrong product
  print "No JSON found"
except requests.exceptions.SSLError:	#ConnectionError for requests
  print "SSL Error"
except requests.exceptions.ConnectionError:#ConnectionError for requests
  print "ConnectionError"
except ntplib.socket.gaierror:
  print "Problem connecting to timeserver"
  #Do someting to inform the dev
print "Time Taken:",datetime.datetime.now()-start
print "Last Product:",last_read