# encoding=utf8
import sys,lxml,urllib
import mechanicalsoup
from importlib import reload
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit, quote
reload(sys)

def iri2uri(iri):ff
    """
    Convert an IRI to a URI (Python 3).
    """
    uri = ''
    if isinstance(iri, str):
        (scheme, netloc, path, query, fragment) = urlsplit(iri)
        scheme = quote(scheme)
        netloc = netloc.encode('idna').decode('utf-8')
        path = quote(path)
        query = quote(query)
        fragment = quote(fragment)
        uri = urlunsplit((scheme, netloc, path, query, fragment))

    return uri

class TdkBot:

    def __init__(self):
        #self.br = mechanicalsoup.StatefulBrowser()
        #self.br.open("http://tdk.org.tr/index.php?option=com_yazimkilavuzu&view=yazimkilavuzu")
        self.browser = mechanicalsoup.Browser()
        self.page = self.browser.get('http://tdk.org.tr/index.php?option=com_yazimkilavuzu&view=yazimkilavuzu')
        

    def begin(self):
        self.main()


    def main(self):
        self.harfler = ['a','b','c','ç','d','e','f','g','h','ı','i','j','k','l','m','n','o','ö','p','r','s','ş','t','u','ü','v','y','z']
        self.f = open("output.txt","w")
        for self.harf in self.harfler:
            
            self.form = self.page.soup.select("#isimAraID")[0]
            self.form.select("#kelime")[0]['value'] = self.harf
            self.page = self.browser.submit(self.form,self.page.url)
            #self.br.select_form('#isimAraID')
            #self.br['kelime']=harf
            #self.br.submit_selected()
            ffff
            self.optionlar = self.page.soup.select('option')
            del self.optionlar[0:3]
            self.sayfa_sayisi = len(self.optionlar) - 1
            print(self.sayfa_sayisi)
            self.mevcutsayfa = 1
            while self.mevcutsayfa <= self.sayfa_sayisi:
                self.kelimeler = self.page.soup.findAll("p",{"class":"thomicb"})
                print(len(self.kelimeler))
                self.i=1
                for self.kelime in self.kelimeler:
                    self.element = self.kelime.select('a')[1]
                    self.element_href = self.element.get('href')
                    self.element_adi = self.element.text
                    #print(self.element_href)
                    #print(iri2uri(self.element_href))
                    self.page_anlam = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                    self.page_anlam = self.page_anlam.open('http://tdk.org.tr'+iri2uri(self.element_href))
                    self.anlamsoup = BeautifulSoup(self.page_anlam.read(),"lxml")
                    #tablo = anlamsoup.select("table")[2]
                    self.tablo = self.anlamsoup.find("table", {"id": "hor-minimalist-a"})
                    self.tr = self.tablo.findAll("tr")
                    self.mevcut_tr = 1
                    print("işte kelime: "+self.element_adi)
                    self.f.writelines( self.element_adi + "/")

                    while self.mevcut_tr<len(self.tr):
                        self.f.writelines(self.tr[self.mevcut_tr].text)
                        self.mevcut_tr += 1
                    self.f.writelines(" - \n")
                    self.i +=1

                self.sonrakisayfa = self.page.soup.findAll("span", {"class": "comicm"})
                self.sonrakisayfa = self.sonrakisayfa[1].select('a')[0]
                self.srksyf = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                self.srksyf = self.srksyf.open('http://tdk.org.tr'+iri2uri(self.sonrakisayfa.get('href')))
                self.soup = BeautifulSoup(self.srksyf.read(),"lxml")
                self.yenikelimeler = self.soup.findAll('p', {"class": "thomicb"})
                print(self.kelimeler[0].text + " " + self.yenikelimeler[0].text)

                if self.kelimeler[0].text == self.yenikelimeler[0].text:
                    break
                else:
                    print(str(self.mevcutsayfa)+". Sayfa Bitti")
                    self.mevcutsayfa += 1
               
        self.f.close()
        self.br.close()

if __name__=="__main__":
    bot = TdkBot()
    bot.begin()
