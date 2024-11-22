import os 
from bs4 import BeautifulSoup
import requests

html_folder = "html"
files_folder = "files"

content_type_map = {
    'application/pdf': '.pdf',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',  
}

for (folder, labels, files) in os.walk(html_folder):
    for index, file in enumerate(files):
        print(f"Now parsing file {index}, {file}")
        full_file_path = f"{html_folder}/{file}"

        with open(full_file_path, "r") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")

            question_containers = soup.find_all("div", {"class": "m-card__main"})

            if len(question_containers) > 0:
                print(f"{len(question_containers)} questions found on this page.")
                for question_container in question_containers:
                    question_title_element = question_container.find("h4")
                    if question_title_element is not None:
                        question_title = question_title_element.text.strip()
                        print(question_title)
                    
                    download_element = question_container.find("a", {"class": "m-button--only-icon"})
                    if download_element is not None:
                        download_link_relative = download_element.get("href")
                        download_link = f"https://www.tweedekamer.nl{download_link_relative}"
                        
                        if download_link and question_title:
                            download_response = requests.get(download_link)
                            download_response.raise_for_status()
                            content_type = download_response.headers.get('Content-Type')
                            file_extension = content_type_map.get(content_type, '')

                            file_output_path = f"{files_folder}/{question_title[:40].replace(" ", "_")}{file_extension}"
                            print(f"Downloading file to {file_output_path}")

                            with open(file_output_path, 'wb') as output_file:
                                output_file.write(download_response.content)

