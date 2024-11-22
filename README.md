# Kamervragen - which ones are about Limburg?

In this repository we scrape questions by members of the Dutch parliament (Kamervragen). We then use a LLM to define whether these are about the province of Limburg, directly or indirectly.

## Prerequisites

The code is written in python, you'll also need pip/conda to install some packages. Try and use a virtual environment for that. Install the needed packages with `pip install -r requirements.txt`.

## How it works

The script is a four-part rocket:

- First you run `python scrape-kamervragen.py` to fetch a bunch of questions, that are then saved as html files. Mind the `amount_to_scrape` parameter in this script, which will determine the amount of questions scraped.
- Then you get the actual documents mentioned in them using `python kamervragen_to_files.py`. This outputs a bunch of files to the `files/` folder.
- After that, run `python extract_questions.py` to fetch the texts from the documents. These are saved as a `questions.csv` in the home folder.
- Finally run `python label_questions.py` to loop over them with a LLM to label whether they are relevant for the province. This will output your final `labeled_questions.csv`.

## TODO:

- Maybe think of naming the output files differently so that double titles (which are fairly common) are not overwritten.
