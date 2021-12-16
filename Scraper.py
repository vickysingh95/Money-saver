import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
import webbrowser 
import mysql.connector as mysql

con=mysql.connect(host="bttotienkk1dqejaut6j-mysql.services.clever-cloud.com",
            user="uamgwvzwbpd8b6kz",passwd="xCYLrsYFurFUe1T7PCrK",
            database="bttotienkk1dqejaut6j")
cursor=con.cursor()
sql="select Email,URL from main";
cursor.execute(sql);

row=cursor.fetchall();
con.close();


SMTP_SERVER="smtp.gmail.com"
PORT=587
Sender_EMAIL_ID="kumarabhimanyu630@gmail.com"

PASSWORD="ceepyqnfcfkjgxok"

def notify():
    server=SMTP(SMTP_SERVER,PORT)
    server.starttls()
    server.login(Sender_EMAIL_ID, PASSWORD)

    subject="Buy Now"
    body="price has failen. Go buy it now ." + URL
    msg=f"subject: {subject}\n\n{body}"

    server.sendmail(Sender_EMAIL_ID,Receiver_ID,msg)
    server.quit()


def find_price(URL):
    r=requests.get(URL,headers={"user-Agent":"Defined"})
    soup=BeautifulSoup(r.content,"html.parser")
    try:
        if "amazon" in URL:            
                price=soup.find(id="priceblock_ourprice")
                if(price==None):
                    price=soup.find(id="priceblock_dealprice")
                    return price
                    
                else:
                    return price         


        
        elif "flipkart" in URL:
            price=soup.find(class_="_30jeq3 _16Jk6d")
            return price
    except:
        return
    
def Ecommerce():
    for ID in row:
        global URL,Receiver_ID
        Receiver_ID=ID[0]
        Url=ID[1]

        if Url==None:
            print("Invalid Url")
        else:
            #print(Url)
            URL=Url
            Current_price=find_price(URL)
            #print(current_price)
            price=Current_price.get_text()
            
            current_price=price.replace('₹','')
            if ',' in current_price:
                current_price=current_price.replace(',','')
                current_price=int(float(current_price))
            else:
                current_price=int(float(current_price))
            print(current_price)
            con=mysql.connect(host="bttotienkk1dqejaut6j-mysql.services.clever-cloud.com",
            user="uamgwvzwbpd8b6kz",passwd="xCYLrsYFurFUe1T7PCrK",
            database="bttotienkk1dqejaut6j")
            cursor=con.cursor()
            sql="select Desirable from main where Email=%s and URL=%s";
            cursor.execute(sql,(Receiver_ID,Url));
            row1=cursor.fetchone();
            previous_price=row1[0]
            con=mysql.connect(host="bttotienkk1dqejaut6j-mysql.services.clever-cloud.com",
            user="uamgwvzwbpd8b6kz",passwd="xCYLrsYFurFUe1T7PCrK",
            database="bttotienkk1dqejaut6j")
            cursor=con.cursor()
            sql="update main set current=%s where URL=%s";
            cursor.execute(sql,(current_price,Url));
            cursor.execute("commit");
            if current_price==None:
                print("Invalid link")
                break
            else:                   
                if current_price<=previous_price:
                    notify()
Ecommerce()
