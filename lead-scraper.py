import urllib
import time
from bs4 import BeautifulSoup
import pandas as pd

apartmentList = []
apartments = {}
    
def scrape_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
    response = urllib.request.urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup

def get_links(html):
    nav_links = []
    find_nav_links = html.find('nav', attrs={'class': 'paging'}).find_all('li')
    for nav in find_nav_links:
        if nav.find('a', href=True):
            if nav.find('a').get('href') != "javascript:void(0)":
                nav_links.append(nav.find('a').get('href'))
    nav_links.pop(-1)
    return nav_links

def get_page_data(html):
    time.sleep(10)
    articles = html.find('div', attrs={'class': 'placardContainer'}).find_all('article', attrs={'class': 'placard'})
    for article in articles:
    
        if (article.find('span', attrs={'class': 'altRentDisplay'})):
            rent_span = article.find('span', attrs={'class': 'altRentDisplay'}).get_text()

        if rent_span != 'Call for Rent':
            if len(rent_span) > 6:
                rent_low, rent_high = rent_span.split('-')     
                rent_low = rent_low.strip().replace('$', '').replace(',','')
                rent_high = rent_high.strip().replace('$', '').replace(',','')
                
        apartments = {
                'name': article.find('a', attrs={'class': 'placardTitle'}).get_text().strip(),
                'address': article.find('div', attrs={'class': 'location'}).get_text().strip(),
                'phone': article.find('div', attrs={'class': 'phone'}).get_text().strip(),
                'rent_low': rent_low,
                'rent_high': rent_high,
                'link': article.find('header', attrs={'class': 'placardHeader'}).find('a', href=True).get('href').strip()
            }
        page2_req = urllib.request.Request(apartments['link'])
        page2_req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
        resp = urllib.request.urlopen(page2_req)
        content = resp.read()
        soup = BeautifulSoup(content, 'lxml')
        
        
        if (soup.find('div', attrs={'class': 'linkWrapper'})):
            propertyLink = soup.find('div', attrs={'class': 'linkWrapper'}).find('a').get('href')
            apartments['websiteLink'] = propertyLink
        else:
            apartments['websiteLink'] = 'No website link'
    
        propertyFeatures = soup.find('div', attrs={'class': 'propertyFeatures'}).select('li')
        
        if len(propertyFeatures) == 2:
            apartments['built'] = propertyFeatures[0]
            apartments['renovated'] = 'not renovated'
            apartments['units'] = propertyFeatures[1]
            
        elif len(propertyFeatures) == 3:
            apartments['built'] = propertyFeatures[0]
            apartments['renovated'] = propertyFeatures[1]
            apartments['units'] = propertyFeatures[2]
        elif len(propertyFeatures) == 4:
            apartments['built'] = propertyFeatures[0]
            apartments['renovated'] = propertyFeatures[1]
            apartments['units'] = propertyFeatures[2]
            
        apartmentList.append(apartments)
    return apartmentList

def get_apartment_info(url):
    pass

def export_to_csv(data):
    df = pd.DataFrame(data)
    with open('apartment_leads_1.csv', 'w') as f:
        df.to_csv(f)    

def main():
   
    counter = 0
    page_html = scrape_url('https://www.apartments.com/canton-mi/?bb=orkmy9w4gJ672irwE')
    page_links = get_links(page_html)
    page_data = get_page_data(page_html)
    
    time.sleep(10)
    
    for url in page_links[0:2]:
        time.sleep(3)
        #print(url)
        page_html_2 = scrape_url(url)
        page_data_2 = get_page_data(page_html_2)
        counter += 1
        #print(counter)
        
    export_to_csv(page_data)
    
    
if __name__ == "__main__":
    main()


