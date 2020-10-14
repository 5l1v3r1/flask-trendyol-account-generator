import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import choices
from threading import Thread

__version__ = "1.0"

class creater:
    #bu trendyolda hesap oluşturacak. işlem bitince databaseden işlem durumunu değiştirecek
    def __init__(self,username,password,id):
        self.username = username
        self.password = password
        self.id = id
        Thread(target=self.create).start()


    def create(self):
        myoptions = Options()
        myoptions.add_argument('window-size=1366x768')
        myoptions.add_argument("headless")
        driver = webdriver.Chrome(options=myoptions)
        connection = mysql.connector.connect(host="localhost",password="notrustly1",username="root",database="trendyolbot")
        cursor = connection.cursor()
        mails = []
        for i in range(10):
            try:
                driver.get("https://www.trendyol.com/uyelik")
                sleep(3)
                emailarea = driver.find_element_by_id("register-email")
                registeredemail = self.username+"".join(choices(["1","2","3","4","5","6","7","8","9"],k=5))
                emailarea.send_keys(f'{registeredemail}@gmail.com')
                passwordarea = driver.find_element_by_id("register-password-input")
                passwordarea.send_keys(self.password)
                driver.execute_script('document.getElementsByName("marketing-email")[0].click()')
                driver.find_element_by_xpath('//*[@id="login-register"]/div[3]/div[1]/form/button').click()
                sleep(3)
                driver.get("https://www.trendyol.com/Hesabim/KullaniciBilgileri")
                sleep(3)
                driver.execute_script('document.getElementById("UserModel_FirstName").value="{}"'.format(self.username))
                driver.execute_script('document.getElementById("UserModel_LastName").value="{}"'.format(self.username[len(self.username)//2:]))
                driver.find_element_by_xpath('//*[@id="UpdateUserInfoForm"]/section[7]/a').click()
                driver.get("https://www.trendyol.com/authentication/logout")
                driver.delete_all_cookies()
                mails.append((registeredemail+"@gmail.com",self.id))
                sleep(1)
            except Exception as e:
                mails.append(("Burada hata oldu: "+str(e),self.id))
        try:
            cursor.executemany("INSERT INTO mails (Mail,OwnerID) values (%s,%s)",mails)
            cursor.execute("update accounts set can_process = 1 where ID = %s",(int(self.id),))
            connection.commit()
            cursor.close()
            connection.close()
            driver.close()
        except Exception as e:
            print("Databaseye veri gönderirken hatya oldu: "+str(e))

if __name__=="__main__":
    creater(username="ertu1ertu",password="ertuertu27",id="6")