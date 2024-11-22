import sys
import json
import csv
from openai import OpenAI

api_key = ""
rows_to_label = []
csv_path = "questions.csv"

try:
    with open("secrets.json", "r") as secrets_file:
        secrets_json = json.load(secrets_file)
        print(secrets_json)
        if secrets_json["aimlapi_key"]:
            api_key = secrets_json["aimlapi_key"]
except Exception as e:
    print(f"Key could not be loaded. Are you sure you created your secrets.json file correctly? {e}")
    sys.exit()

base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=api_key, base_url=base_url)

try:
    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for index, row in enumerate(csv_reader):
            if index > 0:
                rows_to_label.append(row)
except Exception as e:
    print(f"Could not read the csv file. Did you scrape and extract all the files correctly? See README for instructions. {e}")
    sys.exit()


total_rows = len(rows_to_label)
labeled_rows = []
limit = 100 # Adjust this to include all rows but test with a low amount
print_labeled_rows = True
print(f"Total rows: {total_rows}")

system_prompt = """
Ik ga je een tekst sturen waarvan ik wil dat je duidelijk aangeeft of het gaat over een situatie die speelt in de Nederlandse provincie Limburg. Het is heel belangrijk voor me en je bent er echt heel goed in. Je geeft alleen True of False terug, met een kapitaal zodat Python het begrijpt. Je geeft alleen de boolean terug, geen uitleg. Alleen de boolean, geen opmaak. Alleen True of False.
"""

def limit_text_by_word_count(text, max_words):
    words = text.split()
    limited_text = ' '.join(words[:max_words])
    return limited_text

for index, row in enumerate(rows_to_label):
    parsed_row = row
    print(f"Now labeling row {index}/{len(rows_to_label)}")
    if index < limit:
        question_text = row[1]
        limited_text = limit_text_by_word_count(question_text, 1000) # Just so we don't go over the token limit

        try:
            completion = api.chat.completions.create(
                model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": limited_text},
                ],
                temperature=0.2,
                max_tokens=12,
                stop = [" "]
            )

            response = completion.choices[0].message.content

            parsed_row.append(response)
            labeled_rows.append(parsed_row)
        except Exception as e:
            print(f"Labeling row {index} failed: {e}")

with open("labeled_questions.csv", "w") as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerow(["name", "text", "about_limburg"])
    for row in labeled_rows:
        csv_writer.writerow([row[0], row[1], row[2]])