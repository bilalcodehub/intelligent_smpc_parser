import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.medicines.org.uk/emc/browse-medicines"

def makeSoup(limit, offset, alphabet):
    URL = "https://www.medicines.org.uk/emc/browse-medicines?prefix="+ alphabet[0] +"&offset="+str(offset)+"&limit="+str(limit)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

# get all data on page with data_row class
def getPageData(content):
    data_rows = content.find_all("div", {"class": "data-row"})
    page_dataset = []

    for row in data_rows:
        drug_name = row.div.h2.a.string
        company_name = row.div.h4.a.string
        smcp_link = "https://www.medicines.org.uk" + row.div.h2.a.get('href')
        page_dataset.append({
            "drug_name": drug_name,
            "company_name": company_name,
            "smcp_link": smcp_link
        })
    return page_dataset


def getAllDrugs():
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    dataset = []

    for alphabet in alphabets:
        offset = 1
        limit = 200
        highest_page_number = 1
        number_of_pages = 1
        page_data = []
        # get pagination data
        soup = makeSoup(offset=offset, limit=limit, alphabet=alphabet)
        pagination = soup.find("ul", {"class": "search-panel-paging"})
        pagination_string = pagination.li.string
        page_numbers = re.findall('[0-9]+', pagination_string)
        highest_page_number += int(page_numbers[1]) - 1;

        # get first page data
        content = soup.find("main", {"class": "main-home"})
        page_dataset = getPageData(content);
        page_data.extend(page_dataset);
        # dataset.append({alphabet: page_dataset})
        print(alphabet, number_of_pages, offset, limit)

        # get data from next pages
        if(highest_page_number > 1):
            while (number_of_pages < highest_page_number):
                offset+=limit
                soup = makeSoup(offset=offset, limit=limit, alphabet=alphabet)
                number_of_pages = number_of_pages + 1
                content = soup.find("main", {"class": "main-home"})
                page_dataset = getPageData(content);
                page_data.extend(page_dataset);
                # .append({alphabet: page_dataset})
                print(alphabet, number_of_pages, offset, limit)
        dataset.append({alphabet: page_data})

    # write dataset to file
    with open('smcp_drugs_list3.json', 'wt') as outfile:
        json.dump(dataset, outfile)

   
getAllDrugs()


# step 1: Read all drug names and data and store in json file
# step 2: visit the smcp link for each drug to get data
# step 3: format the smcp data and categorize it
# step 4: process this data for machine learning.
