from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome()

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
driver.get("https://www.google.com/search?sxsrf=ALeKk02y8JnlfOG30UaO0mtMHsymgmv9rA%3A1606908893923&source=hp&ei=3XvHX7i7NcnYhwP2h7bgAQ&q=python&oq=python&gs_lcp=CgZwc3ktYWIQAzIECCMQJzIECCMQJzIECCMQJzIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywE6AggAOgIILlDCTlj6UWCkU2gAcAB4AIABmgGIAbsGkgEDMC42mAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwj4nbmOmq_tAhVJ7GEKHfaDDRwQ4dUDCAY&uact=5")


content = driver.page_source
soup = BeautifulSoup(content)


for a in soup.findAll('a', href=True, attrs={'class':'fl'}):
	print (a)
	break
	name=a.find('div', attrs={'class':'_4rR01T'})
	price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
	rating=a.find('div', attrs={'class':'_3LWZlK'})
	products.append(name.text)
	prices.append(price.text)
	ratings.append(rating.text) 
	
print (products)
print (prices)
print (ratings)

driver.close()