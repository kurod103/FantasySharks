import requests
import os
import requests
from bs4 import BeautifulSoup
#TESTTTEST

# headers is needed so fantasysharks knows what browser we claim to be using.
headers = {'User-Agent': 'Chrome/39.0.2171.95'}

# Defensive Lineman (DL) stats from week 3
segment=692
segcap=708
starpos=1
poscap=15
pos=1
os.mkdir("fftoday")

for seg in range(1+segcap-segment):
    os.mkdir(str(seg+segment))

    for pos in range(1+poscap-starpos):
        url = 'https://www.fantasysharks.com/apps/bert/forecasts/projections.php?csv=1&Sort=&Segment='+str(segment)+'&Position='+str(pos)+'&scoring=2&League=&uid=4&uid2=&printable='
    
        # use the requests library to download the resource addressed by the url.
        r = requests.get(url, headers=headers)
        title=r.text.split(',')
        
        for i in range (2,25):
            if title[-i][-1].isdigit()==False:
                document=str(seg+segment)+'/'+title[-i]+'.csv'
                break
        # Write the contents into a csv.
        open(document, 'wb').write(r.content)


posdict={10:"QB",20:"RB",30:"WR",40:"TE",50:"DL",60:"LB",70:"DB",80:"K"}
for pos in range(8):
    position=(pos+1)*10
    file="fftoday/"+posdict[position]+".csv"
    print(file)
    document=""
    for pg in range (5):
        url='https://fftoday.com/rankings/playerproj.php?Season=2020&PosID='+str(position)+'&LeagueID=&order_by=FFPts&sort_order=DESC&cur_page='+str(pg)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        entries = soup.find_all("table")[7].find_all(class_="smallbody")
        
        for entry in entries:
            if entry.get_text().isspace() or entry.get_text()=="":
                document=document+"\n"
            else:
                document=document+(entry.get_text().replace(u'\xa0', u''))
                document=document+","
        
    document="Player,Team,Bye,Att,Yard,TD,Rec,Yard,ReceivingTD,FPts"+document
    open(file, 'w').write(document)
