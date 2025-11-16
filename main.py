import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time


def web_scrape(url, file_name):
    print("Starting web scraping...")

    # Delay for 5 seconds
    time.sleep(3)  

    response = requests.get(url, headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'})

    if response.status_code == 200:
        print("Webpage fetched successfully!")
        html_content = response.text
        
        #creating soup object
        soup = BeautifulSoup(html_content, 'lxml')
        
        #main container for hotel listings
        hotel_divs = soup.find_all('div', role='listitem')

        #writing to CSV file
        with open(file_name, 'w', encoding='utf-8',newline='') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['Hotel_Name', 'Location', 'Price', 'Reviews', 'Number_of_Reviews', 'Rating', 'Hotel_Link'])

            #extracting hotel info
            for hotel in hotel_divs:
                hotel_name = hotel.find('div', class_="b87c397a13 a3e0b4ffd1").text.strip()
                hotel_location = hotel.find('span', class_="d823fbbeed f9b3563dd4").text.strip()
                hotel_price = hotel.find('span', class_="b87c397a13 f2f358d1de ab607752a2").text.strip()
                hotel_reviews = hotel.find('div', class_="f63b14ab7a f546354b44 becbee2f63").text.strip() if hotel.find('div', class_="f63b14ab7a f546354b44 becbee2f63") else "No reviews"
                if hotel_reviews != "No reviews":
                    Number_of_reviews = hotel.find('div', class_="fff1944c52 fb14de7f14 eaa8455879").text.strip()

                hotel_rating = hotel.find('div', class_="f63b14ab7a dff2e52086").text.strip() if hotel.find('div', class_="f63b14ab7a dff2e52086") else "No rating"
                link = hotel.find('a', class_="bd77474a8e")['href']

                #saving to CSV
                writer.writerow([hotel_name, hotel_location, hotel_price, hotel_reviews, Number_of_reviews, hotel_rating, link])
            
                #print(f"Hotel Name: {hotel_name}")
                #print(f"Location: {hotel_location}")
                #print(f"Price: {hotel_price}")
                #print(f"Reviews: {hotel_reviews}")
                #print(f"Number of Reviews: {Number_of_reviews}")
                #print(f"Rating: {hotel_rating}")
                #print(f"Link: {link}")
                #print("-" * 40)



    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        exit()

if __name__ == "__main__":
    url = input("Enter the URL of the page: ")
    file_name = input("Enter the desired file name (with .csv extension): ")
    web_scrape(url, file_name)