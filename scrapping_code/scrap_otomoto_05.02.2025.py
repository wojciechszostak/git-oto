import requests
from bs4 import BeautifulSoup
import csv
import time 



def scrape_car_listings(car_make, max_pages):
    scraped_data = []

    for page in range(1, max_pages + 1):
        url = f"https://www.otomoto.pl/osobowe/{car_make}?page={page}"

        # Agent sesji
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        # Poprawne połączenie
        if response.status_code == 200:
            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', {'data-id': True})



            # LOOP
            for article in articles:
                # Tytuł
                title_tag = article.find('h2', class_='e4b361b0 ooa-1jjzghu')
                title = title_tag.text if title_tag else 'N/A'

                # Link
                link_tag = title_tag.find('a') if title_tag else None
                link = link_tag['href'] if link_tag else 'N/A'

                # Opis
                description_tag = article.find('p', class_='ekpvtd0 ooa-1gjazjm')
                description = description_tag.text if description_tag else 'N/A'

                # Cena
                price_tag = article.find('h3', class_='ecit9451 ooa-1n2paoq')
                price = price_tag.text if price_tag else 'N/A'

                # Lokalizacja
                location_tag = article.find('p', class_='ooa-oj1jk2')
                location = location_tag.text if location_tag else 'N/A'

                # Dodatkowe dane
                mileage = article.find('dd', {'data-parameter': 'mileage'})
                fuel_type = article.find('dd', {'data-parameter': 'fuel_type'})
                gearbox = article.find('dd', {'data-parameter': 'gearbox'})
                year = article.find('dd', {'data-parameter': 'year'})

                # Collect data
                scraped_data.append([
                    title,
                    link,
                    description,
                    price,
                    location,
                    mileage.text if mileage else 'N/A',
                    fuel_type.text if fuel_type else 'N/A',
                    gearbox.text if gearbox else 'N/A',
                    year.text if year else 'N/A'
                ])

            print(f"Strona {page} zeskrapowana poprawnie.")

        else:
            print(f"Błąd w skrapowaniu strony {page}. Kod błędu: {response.status_code}")
            break

    # zapis do pliku CSV
    with open(f'{car_make}_aukcje.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # Nazwy kolumn
        writer.writerow(
            ['Title', 'Link','Description','Price', 'Location', 'Mileage', 'Fuel Type', 'Gearbox', 'Year'])
        # wypisanie danych
        writer.writerows(scraped_data)

    print(f"Zapisano skrap w pliku: {car_make}_aukcje.csv")

# Wywołanie funkcji
scrape_car_listings("opel", 10)
