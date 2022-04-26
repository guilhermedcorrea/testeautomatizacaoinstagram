import lxml.html as parser
import requests
import csv
from datetime import datetime
import schedule
import re
import json
import time
from urllib.parse import urlsplit, urljoin
import os.path
import ftplib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.select import Select


#https://qastack.com.br/unix/107939/how-to-restart-the-python-script-automatically-if-it-is-killed-or-dies
#https://academiahopper.com.br/como-trabalhar-com-data-e-hora-em-python/
#https://docs.python.org/pt-br/3/library/datetime.html
#https://medium.com/@felipebastosweb/agenda-de-tarefas-jobs-do-app-no-python-6a8a5d234ec8
#https://www.geeksforgeeks.org/send-direct-message-on-instagram-using-selenium-in-python/
#https://www.youtube.com/watch?v=PAnrHMQBB-Y biblioteca schedule

driver=webdriver.Chrome()

driver.get('https://www.instagram.com/?hl=pt-br')


class Product(object):
    def __init__(self):
        self.time ='10:51' #Informar data atual
        self.user = ''
        self.key = ''
        self.week = 0
        self.perfil ='' #Palavra chave a ser pesquisada.
        self.perfil_principal = set() #Url perfil principal
        self.mensagem ='hello how are you?' #guarda mensagem que quer enviar no direct
        self.data_atual = datetime.now()
        self.sugeridos = set()
        self.seguidores = set() #relação de seguidores
        self.seguindo = set() #Relação que estou seguindo
        self.nao_esta_seguindo = set() #Lista de perfils que  não esta seguindo de volta
        self.perfil_encontrado = set() #lista perfils encontrados referente a palavra chave do self.perfil


    def login(self):
        #Login tela inicial
        time.sleep(3)
        email = driver.find_element_by_xpath("//input[@class='_2hvTZ pexuQ zyHYP']")
        email.send_keys(self.user)
        senha = driver.find_element_by_xpath("//input[@name='password']")
        senha.send_keys(self.key)
        time.sleep(2)
        clica = driver.find_element_by_xpath("//button[@type='submit']").click()

        time.sleep(4)
        try:
            clica_2 = driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()
        except:
            print('Not Found')

        driver.get('https://www.instagram.com/g.d.correa')


    def envia_direct(self):

        time.sleep(10)

        try:
            clic = driver.find_element_by_xpath("//button[@class='sqdOP  L3NKy _4pI4F   _8A5w5    ']").click()
        except:
            print("NotFound")

        time.sleep(3)

        try:
            mensagem = driver.find_element_by_xpath("//textarea[@placeholder='Mensagem...']")
        except:
            print("Not Found")

        try:
            mensagem.send_keys(self.mensagem)
        except:
            print("Not Found")

        time.sleep(4)
        try:
            enviar_mensagem = driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d    y3zKF     ']")[3].click()
        except:
            print("Not Found")

    

    def desce_pagina(self):
          #rola tela seguidor/seguindo
        time.sleep(3)
        seguidores = driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll <1:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', seguidores)
            time.sleep(1)
            scroll+=1


    def busca_seguidores(self):
        time.sleep(3)
        painel_seguidores = driver.find_elements_by_xpath("//a[@class='-nal3 ']")[0].click()
        Produto = Product()
        Produto.desce_pagina()

        seg = driver.find_elements_by_xpath("//div[@class='isgrP']//li//a")
        for s in seg:
            print('SEGUIDOR ~~ >',s.get_attribute('href'))
            self.seguidores.add(s.get_attribute('href'))

        driver.get('https://www.instagram.com/g.d.correa')


    def busca_seguindo(self):
        time.sleep(3)
        painel_seguindo = driver.find_elements_by_xpath("//a[@class='-nal3 ']")[1].click()
        Produto = Product()
        Produto.desce_pagina()

        tela_seguindo = driver.find_elements_by_xpath("//div[@class='isgrP']//li//a")
        for x in tela_seguindo:
            print('SEGUINDO ~~ >',x.get_attribute('href'))
            self.seguindo.add(x.get_attribute('href'))

        driver.get('https://www.instagram.com/g.d.correa')


    def compara_listas(self):

        comparacao = [x for x in self.seguindo if x not in self.seguidores]
        for comp in comparacao:
            print('comparado ~~ >', comp)
            self.nao_esta_seguindo.add(comp)


    def descurtir(self):
        for x in self.nao_esta_seguindo:

            driver.get(x)

            time.sleep(5)
          
            try:
                button_4 = driver.find_element_by_xpath("//span[@class='glyphsSpriteFriend_Follow u-__7']").click().click()
            except:
                print("NotFound")
                time.sleep(4)

            try:
                descurti = driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']").click()
            except:
                print("NotFound")

            
            time.sleep(1)

            try:
                button_2 = driver.find_element_by_xpath("//span[@class='glyphsSpriteFriend_Follow u-__7']").click()
            except:
                pass

            try:
                deixar_seguir = driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']").click()
            except:
                pass
            print(f"deixou de seguir {x}")
            

    def lenOfPage(self):
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True


    def busca_sugeridos(self):
        driver.get('https://www.instagram.com/?hl=pt-br')

        time.sleep(3)
        agora_nao = driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()

        time.sleep(7)
        ver_tudo = driver.find_element_by_xpath("//div[@class='_7UhW9  PIoXz        qyrsm KV-D4          uL8Hv         ']").click()
        time.sleep(7)
        Produto.lenOfPage()
        time.sleep(3)
        select = driver.find_elements_by_xpath("//div[@class='         DPiy6            Igw0E     IwRSH      eGOV_         _4EzTm                                                                                             HVWg4                 ']//a")
        for s in select:
            print(s.get_attribute('href'))
            self.sugeridos.add(s.get_attribute('href'))


    def adiciona(self):
        for s in self.sugeridos:
            driver.get(s)

            time.sleep(7)
            try:
                seguir_1 = driver.find_element_by_xpath("//button[@class='_5f5mN       jIbKX  _6VtSN     yZn4P   ']").click()
            except:
                pass
            
            try:
                seguir_3 = driver.find_element_by_xpath("//button[@class='sqdOP  L3NKy   y3zKF     ']").click()
            except:
                pass
            
               
            print(f'seguindo {s}')

            Produto.envia_direct()


    def stories(self):
        
        time.sleep(4)
        driver.get("https://www.instagram.com/")
        
        time.sleep(5)
        teste = driver.find_elements_by_xpath("//img[@class='_6q-tv']")[2].click()
       
        time.sleep(2)
        cont = 1
        while cont <=20:
            time.sleep(2)

            try:
                time.sleep(2)
                clica = driver.find_element_by_xpath("//div[@class='coreSpriteRightChevron']").click()
                    
            except:
                print("NotFound")

            time.sleep(2)
            cont = cont+1
                
        driver.get("https://www.instagram.com")
   
   
    def curtir_post(self):
        driver.get("https://www.instagram.com/")

        time.sleep(5)

     
        time.sleep(4)
        cont = 0
        while cont <10:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            #t = driver.find_elements_by_xpath("//section[@class='ltpMr  Slqrh']//button[@type='button']")[1].click()
            try:
                t = driver.find_elements_by_xpath("//section[@class='ltpMr  Slqrh']//button[@type='button']")[0].click()
                
            except:
                print("NotFound")
            cont+=1


Produto = Product()
Produto.login()
#Produto.busca_seguidores()
#Produto.busca_seguindo()
#Produto.compara_listas()
#Produto.descurtir()
#Produto.busca_sugeridos()
#Produto.adiciona()
#Produto.stories()
Produto.stories()
#Produto.curtir_post()











