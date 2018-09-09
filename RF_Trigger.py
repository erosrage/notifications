import bs4
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup


searchURL = 'https://www.redfin.com/city/13654/CA/Oakland/filter/property-type=house,max-price=500k'
req = Request(searchURL, headers={'User-Agent': 'Mozilla/5.0'})
webpage = uReq(req).read()
page_soup = soup(webpage,'html.parser')
containers = page_soup.findAll("div",{"class":"HomeCardContainer"})
msg = '\n\n'
StreetAddy = ''
CityZip = ''

#Extract data and prep CSV and SMS messages
for container in containers:
    Cost = container.find("span",{"class":"homecardPrice font-size-small font-weight-bold"}).get_text().strip().replace(',','')
    StreetAddy = container.find("span",{"data-rf-test-id":"abp-streetLine"}).get_text().strip()
    CityZip = container.find("span",{"class":"cityStateZip"}).get_text().strip()
    sqft = container.findAll("div",{"class":"value"})
    sqft = sqft[2].get_text()
    print(Cost + '\n' + StreetAddy + '\n' + CityZip + '\n' + sqft + ' SqFt' + '\n\n')
    msg += (Cost + '\n' + StreetAddy + '\n' + CityZip +'\n' + sqft + ' SqFt' + '\n\n')
msg += (searchURL)

# Send Txt Msg
from twilio.rest import Client
account_sid = '' #Twilio Console Dashboard
auth_token = '' #Twilio Console Dashboard
myPhone = '' # Phone number
TwilioNumber = '' # Phone number - Twilio
client = Client(account_sid, auth_token)
client.messages.create(
  to=myPhone,
  from_=TwilioNumber,
  body=msg)
