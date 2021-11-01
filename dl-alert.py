import urllib.request
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from playsound import playsound

location_arr = ['101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123']
locationname_arr = ['Lawrenceville','Bayonne','North Cape May','Camden','Cardiff','Salem','Delanco','Eatontown','SouthPlainfield','Edison','Flemington','Toms River','Freehold','Lodi','Vineland','Newark','North Bergen','Wayne','Oakland','Paterson','Thorofare','Rahway','Randolph']
base_url_link='https://telegov.njportal.com/njmvc/AppointmentWizard/11/'
required_months = ['October','November', 'December', 'January']

def beep():
    playsound('audio.mp3')

def job():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("\n\n\nDate Time: ", dt_string, "\n\n")
    i=0
    found=0
    
    for location in location_arr:
        print(location + locationname_arr[i])
        with urllib.request.urlopen(base_url_link + location) as response:
            page_html = response.read()
        soup = BeautifulSoup(page_html ,'lxml')
        unavailable = soup.find('div',attrs={'class': 'alert-danger'})

        if unavailable is not None :
            print('No appointments are available in '+locationname_arr[i])
            dt_string=""
        else:
            dates_html = soup.find('div',attrs={'class': 'col-md-8'})
            if dates_html is not None :
                date_string = dates_html.find('label',attrs={'class': 'control-label'})
                if set(required_months) & set(date_string.text.split()):
                    date_string=re.sub('Time of Appointment for ', '', date_string.text)
                    date_string=re.sub(':', '', date_string)
                    message = 'Knowledge test date: '+locationname_arr[i]+' / ('+location+') : '+date_string
                    print(message)
                    found=1
        i=i+1
    
    if found:
        print('Appointment found')
        beep()
        
while True :
    try:
        job()
    except Exception as e: 
        print(e)
        print("Something went wrong")
        time.sleep(60)
    else:
        time.sleep(60)
    