#-*- coding: utf-8 -*- 
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
reload(sys)  
sys.setdefaultencoding('utf8')
driver = webdriver.PhantomJS(executable_path='/home/mehmet41650/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get("http://tdk.org.tr/index.php?option=com_yazimkilavuzu&view=yazimkilavuzu")
driver.implicitly_wait(3)
harfler = ['a','b','c','ç','d','e','f','g','ğ','h','ı','i','j','k','l','m','n','o','ö','p','r','s','ş','t','u','ü','v','y','z']
xpath = '//*[@id="hor-minimalist-a"]/tbody'
f = open('wordlistmean.txt', 'w')
fo = open('hataoldumu.txt','w')

alfabe = 1
while alfabe<29:
    textbox = driver.find_element_by_id('kelime').send_keys(harfler[alfabe])
    driver.find_element_by_id('gonderID').click()
    kelimesayisi = driver.find_elements_by_class_name('thomicb')
    print(len(kelimesayisi))
    options = driver.find_elements_by_tag_name('option')
    sayfasayisi = options[len(options)-1].text
    mevcutsayfa=1

    while mevcutsayfa < int(sayfasayisi)+1:
        i = 1
        webel = driver.find_element_by_xpath('//*[@id="sayfa2"]/p/select')
        slt1 = Select(webel)
        if mevcutsayfa != 1:
            slt1.select_by_visible_text(str(mevcutsayfa))            
        print("mevcut sayfa: " + str(mevcutsayfa))
        trler = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div/div[1]/table[2]/tbody/tr')
        while i<=len(trler):
            print("i'nin durumu: "+str(i))
            sayacsayisi = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div/div[1]/table[2]/tbody/tr['+ str(i) +']/td')
            sayac = 1
            while sayac<=len(sayacsayisi):
                print("sayac: "+str(sayac))
                aelement=driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[1]/table[2]/tbody/tr['+ str(i) +']/td['+ str(sayac) +']/p/a[2]')
                kelime = aelement.text
                aelement.click()
                try:
                    anlam = driver.find_element_by_xpath(xpath).text
                    f.write(kelime + "/" + anlam+"\n-\n")
                    print(kelime + " / " + anlam)
                except NoSuchElementException:
                    fo.write(kelime+"\n")
                    print("anlamı olmayan kelime: "+kelime)
                    pass
                driver.back()
                sayac += 1
            i +=1
        mevcutsayfa +=1
    alfabe +=1
    
    #fo.write(str(e) + "\n")
    #fo.write("!!! Mevcut Harf: "+ harfler[alfabe]+"\n")
    #fo.write("Mevcut Sayfa: "+str(mevcutsayfa)+"\n")
    #fo.write("En Son Yapılan Kelime: "+str(kelime)+"\n")
fo.close()
f.close()
driver.close()
