import requests
from bs4 import BeautifulSoup
# import {BeautifulSoup} from  bs4

URL = "https://bnf.nice.org.uk/drug/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

drugs = soup.find_all('a')
drug_links = []
drug_link_soups = []

for link in drugs:
    drug_links.append(link.get('href'))
    
    
   
drug_page = requests.get("https://bnf.nice.org.uk/drug/"+ drug_links[0])
drug_soup = BeautifulSoup(drug_page.content, "html.parser")
drug_nav =  drug_soup.find('body').find('ul')

