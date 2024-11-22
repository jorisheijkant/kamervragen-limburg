# Kamervragen - which ones are about Limburg?

In this repository we scrape questions by members of the Dutch parliament (Kamervragen). We then use a LLM to define whether these are about the province of Limburg, directly or indirectly.

## Prerequisites

The code is written in python, you'll also need pip/conda to install some packages. Try and use a virtual environment for that. Install the needed packages with `pip install -r requirements.txt`.

For the labeling part, [AIMLAPI](https://aimlapi.com/) is used. This allows quickly switching between models. You can easily swap this with Open AI or any other provider that uses OpenAI's python library for communication with LLM's. Note: this library and AIMLAPI do not communicate with OpenAI's server unless you choose one of their models.

You should create a `secrets.json` file with your API key or load it in some other way where you do not commit it to the repo directly.

## How it works

The script is a four-part rocket:

- First you run `python scrape-kamervragen.py` to fetch a bunch of questions, that are then saved as html files. Mind the `amount_to_scrape` parameter in this script, which will determine the amount of questions scraped.
- Then you get the actual documents mentioned in them using `python kamervragen_to_files.py`. This outputs a bunch of files to the `files/` folder.
- After that, run `python extract_questions.py` to fetch the texts from the documents. These are saved as a `questions.csv` in the home folder.
- Finally run `python label_questions.py` to loop over them with a LLM to label whether they are relevant for the province. This will output your final `labeled_questions.csv`.

## TODO:

- Maybe think of naming the output files differently so that double titles (which are fairly common) are not overwritten.
- In general save something of a map of sorts, where more info about the question (kamervraag) is saved than just the title and text.
