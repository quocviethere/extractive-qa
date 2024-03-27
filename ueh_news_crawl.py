import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# Base URL of the webpage
base_url = 'https://ueh.edu.vn/khoa-hoc/page/'

# Start with page 1
page_number = 1

with open('khoa-hoc-articles.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Title', 'URL', 'Content'])
    while page_number <= 208:
        # Construct the URL for the current page
        url = base_url + str(page_number) + '/'
        
        response = requests.get(url)
        
        if response.status_code != 200:
            break  # If the page does not exist, exit the loop
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='card short custom-short list-item')
        
        if not articles:
            break
        
        for article in articles:
            title_link = article.find('a', class_='news-title-view')
            title = title_link.text.strip()

            article_url = title_link['href']
            
            # Construct the absolute URL of the article
            absolute_article_url = urljoin(base_url, article_url)
            
            # Send a GET request to the article URL
            article_response = requests.get(absolute_article_url)
            
            # Parse the HTML content of the article page
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            # Find the content of the article within the <div class="news-content"> tag
            article_content_tag = article_soup.find('div', class_='news-content')
            
            if article_content_tag:
                article_content = article_content_tag.text.strip()
            else:
                article_content = "Content not found"
            writer.writerow([title, absolute_article_url, article_content])
        
        page_number += 1         # Move to the next page


print("Data saved to khoa-hoc-articles.csv")