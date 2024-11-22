import requests 
import time

base_url = "https://www.tweedekamer.nl/kamerstukken/kamervragen?qry=%2A&fld_tk_categorie=Kamerstukken&fld_prl_kamerstuk=Kamervragen&srt=date%3Adesc%3Adate&page="

amount_to_scrape = 100
amount_per_page = 15
pages_to_scrape = (amount_to_scrape // amount_per_page) + 1 
check_for_doubles = False
print(pages_to_scrape)

for page_index in range(pages_to_scrape):
    page_number = page_index + 1
    page_url = f"{base_url}{page_number}"
    html_folder = "html"
    print(f"Now scraping page {page_number}/{pages_to_scrape}")

    page_response = requests.get(page_url)
    page_response.raise_for_status()
    output_file_name = f"{html_folder}/{page_number}.html"

    with open(output_file_name, "w") as output_file:
        output_file.write(page_response.text)

    time.sleep(1)
    
