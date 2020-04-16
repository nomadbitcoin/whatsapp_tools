from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import platform
import bs4


class controlBrowser():
	def __init__(self, business=None):
		self.business = business

		if self.business == None:
			self.business = 'test'

		self.main_url = 'https://web.whatsapp.com/'

	# INSTANCE BROWSER
	def openNewBrowser(self):
	    '''
	        Verifica qual o sistema operacional para que use o driver e diretorio de usuarios certo
	    '''
	    
	    if platform.system() == 'Linux':
	        driver_path = os.getcwd() + '/webdriver/linux/chromedriver'
	        profile_path = os.getcwd() + '/profile_' + self.business
	        
	    elif platform.system() == 'Windows':
	        driver_path = r'C:\\Users\\Yan\\Desktop\\brisbane_bot\\webdriver\\win\\chromedriver.exe'
	        profile_path = "C:\\Users\\Yan\\Desktop\\Liziane - Avon\\" + self.business
	        print(profile_path)
	    
	    try:
	        options = webdriver.ChromeOptions()
	        options.add_argument("profile")
	        options.add_argument("user-data-dir=" + profile_path)
	        # open with saved informations in cache
	        
	        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)
	        self.driver.get(self.main_url)
	        if self.wait_connection():
	            return True, 'opened in: {}'.format(self.main_url)
	    except Exception as error:
	        print('\nERROR [openBrowser()]: {}, {}'.format(type(error), error))
	        return False
	    
	# PARA LIBERAR SOMENTE APOS TER ABERTO O WHATSAPP
	def wait_connection(self):
	    waiting = True
	    while waiting:
	        try:
	            self.driver.find_element_by_class_name('_1-iDe')
	            return True
	        except KeyboardInterrupt:
	            waiting = False
	            print('\nSopped\n')
	            return False
	        except Exception as error:
	            if 'NoSuchElementException' in str(type(error)):
	                time.sleep(3)
	                pass
	            else:
	                print('\nERROR [wait_connection()]: {}, {}'.format(type(error), error))
	                return False



class verifyNumbers():
	'''
		Verifica os numeros que possuem whatsapp
	'''

	def __init__(self, driver):
		self.driver = driver


	def newGroup(self):

	    '''*Com o botao de novas mensagens tendo sido clicado, ira clicar no botao "Novo grupo ou New group"'''
	    try:
	        for chat_element in self.driver.find_elements_by_class_name('_39pS-'):
	            if chat_element.text == 'New group' or chat_element == 'Novo grupo':
	                chat_element.click()
	                return True
	        return False
	        #nao encontrou ou nao clicou
	    except Exception as error:
	        print('\nERROR: class[controlBrowser()] --> function[newGroup() --> type: {}, \nerror: {}\n]'.format(type(error), error))
	        return False

	def clickNewMessages(self):
	    '''
	        *Clica no botao "nova mensagem"
	    '''
	    try:
	        button_new_messages = self.driver.find_element_by_xpath('//span[@data-icon="chat"]')
	        button_new_messages.click()
	        return True
	    except Exception as error:
	        print('\nERROR: class[controlBrowser()] --> function[clickNewMessages() --> type: {}, \nerror: {}\n]'.format(type(error), error))


	def saveName(self):
	    '''
	        *Pega a lista de contatos que estao em evidencia no momendo da interacao com o navegador
	        *Adiciona uma lista global
	    '''
	    htmlPage = bs4.BeautifulSoup(self.driver.page_source, features='html.parser')
	    for name in htmlPage.find_all('span', {'class':'_3TEwt'}):
	        if name.text != None:
	            self.contatos_wpp.append(name.text)

	def total_conversations(self):
	    '''
	        Pega o numero total de conversas baseado no elemento de uma div que informa isso
	    '''
	    try:
	        chat_list = self.driver.find_elements_by_class_name('_2wP_Y')
	        
	        total = 0
	        for chat in chat_list:
	            starter = chat.get_attribute('style').find(':')
	            delimiter = chat.get_attribute('style').find(';')
	            found = int(''.join(filter(str.isdigit, chat.get_attribute('style')[starter:delimiter])))
	            if found > total:
	                total = found
	        return total
	    except Exception as error:
	        print(type(error), error)
	        return None
	
	def __call__(self):
		self.clickNewMessages()
		time.sleep(1)
		self.newGroup()

		press_down = ActionChains(self.driver)
		press_down.send_keys(Keys.DOWN)
		press_down.perform()

		time.sleep(3)
		total_chats = self.total_conversations()
		
		self.contatos_wpp = []
		assert total_chats != None, 'Total chats not found'
		for i in range(int(total_chats)):
		    press_down.perform()
		    self.saveName()

		self.contatos_wpp = list(set(self.contatos_wpp))
		print('verified {} contacts with whatsapp'.format(len(self.contatos_wpp)))
		return self.contatos_wpp