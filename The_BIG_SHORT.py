import bs4, requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request

my_url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield"
with requests.get(my_url) as r:
    page_html = r.text
    page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll("td",{"class":"text_view_data"})

#Finding 2 yr and 10 yr yields and applying ratio

try:
    twoYr = containers[-7].get_text()
    tenYr = containers[-3].get_text()
    yesterday2YR = containers[-19].get_text()
    yesterday10yr = containers[-15].get_text()
    ratio = float(twoYr) / float(tenYr)
    ratio = round(ratio,5)
    ratio = str(ratio)
    yratio = float(yesterday2YR) / float(yesterday10yr)
    yratio = round(yratio,5)
    yratio = str(yratio)
    today = containers[-12].get_text()

    #Packaging Message
    msg = "\n" + 'Yesterday - 2yr Yld: ' + yesterday2YR + '\n' + 'Yesterday - 10yr Yld: ' + yesterday10yr + '\n' + "Yesterday - Yld: " + yratio
    msg += '\n\nThe 2yr Yld today: ' + twoYr + '\n' + 'The 10yr Yld today is: ' + tenYr + '\n' + "Today current Yld: " + ratio + '\n'
    visit = 'Visit US treasury portal for details:\nhttps://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    warning = 'WARNING the apex has been hit! Current Ratio is now: ' + ratio
    print(msg)

except IndexError:
    msg = "Error -500: Unable to index"
    ratio = -500

#Send Message
import smtplib
SendEmail = "4088575781@vtext.com"
FromEmail = "Tran@Adobe.com"
#pw = 'cexyvrzpjosnifju'
server = smtplib.SMTP('namail.corp.adobe.com', 25)
#server.starttls()
#server.login(FromEmail,pw)
server.ehlo()
if ratio == -500:
    server.sendmail(FromEmail, SendEmail, msg)
    print("Error -500: Unable to index")

elif float(ratio) < 1:
    server.sendmail(FromEmail, SendEmail, msg)
    server.sendmail(FromEmail, SendEmail, visit)
else:
    server.sendmail(FromEmail, SendEmail, warning)
    server.sendmail(FromEmail, SendEmail, visit)
server.quit()
