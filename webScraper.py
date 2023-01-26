import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.cars.com/for-sale/searchresults.action/?localVehicles=true&mdId=35363&mkId=20017&page=1&perPage=20&rd=500&searchSource=GN_SELECT&showMore=false&sort=relevance&trId=23667&transTypeId=28112&yrId=56007&yrId=51683&yrId=47272&zc=95132"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll("div",{"class":"shop-srp-listings__listing"})
#f = open("C://Users//tran//Desktop//WebScraping//CRZ Listings.csv", "a")
#headers = "Description, Cost, Mileage, Distance, URL\n"
#f.write(headers)
msg = ''

#Extract data and prep CSV and SMS messages
for container in containers:
    description = container.find("h2",{"class":"cui-delta listing-row__title"}).get_text().strip().replace(',','')
    Cost = container.find("span",{"class":"listing-row__price"}).get_text().strip().replace(',','')
    Mileage = container.find("span",{"class":"listing-row__mileage"}).get_text().strip().replace(',','')
    Distance = container.find("div",{"class":"listing-row__distance-mobile"}).get_text().strip().replace(',','')
    url = container.find("a",{"class":"listing-row__link"})['href']
    phone = container.find("div",{"class":"listing-row__dealer-info"}).get_text().strip().replace(' ','').replace('\n', '')
    phone = phone[17:30]
    print(description + '\n' + Cost + '\n' + Mileage + '\n' + Distance  + '\n' + phone +'\n\n')
    #f.write(description + ',' + Cost + ',' + Mileage + ',' + Distance + ',' + url + '\n')
    msg += (description + '\n' + Cost + '\n' + Mileage + '\n' + Distance  + '\n' + phone +'\n\n')
#f.close()
msg += my_url

# Send Txt Msg
from twilio.rest import Client
account_sid = 'ACdc5b06226e683ccf847ef573ce5766b7' #Twilio Console Dashboard
auth_token = '61446e40b534c497d934290871b06d15' #Twilio Console Dashboard
myPhone = '4088575781' # Phone number
TwilioNumber = '8312788850' # Phone number - Twilio
client = Client(account_sid, auth_token)
client.messages.create(
  to=myPhone,
  from_=TwilioNumber,
  body=msg)

"""
#Insert into Postgresql DB
#Postgresql - Honda@1989
import psycopg2
connection = "host='' dbname='' user='postgres' password=''"
conn = psycopg2.connect(connection)
cursor = conn.cursor()
id = 0

for container in containers:
    id = id+1  
    description = container.find("h2",{"class":"cui-delta listing-row__title"}).get_text().strip().replace(',','')
    Cost = container.find("span",{"class":"listing-row__price"}).get_text().strip().replace(',','')
    Mileage = container.find("span",{"class":"listing-row__mileage"}).get_text().strip().replace(',','')
    Distance = container.find("div",{"class":"listing-row__distance-mobile"}).get_text().strip().replace(',','')
    url = container.find("a",{"class":"listing-row__link"})['href']
    
    query =  "INSERT INTO listings (id, description, Cost, Mileage, Distance, url) VALUES (%s, %s, %s, %s, %s, %s);"
    data = (id, description, Cost, Mileage, Distance, url)
    cursor.execute(query, data)
conn.commit()
"""
#Added comment
