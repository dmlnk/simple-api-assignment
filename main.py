import requests
import json
import sys

KANYE_WEST_API_LINK = "https://api.kanye.rest/"
SENTIM_API_LINK = "https://sentim-api.herokuapp.com/api/v1/"
SENTIM_PARAMS = {"Accept": "application/json", "Content-Type": "application/json"}
MIN_QUOTES_NUMBER = 5
MAX_QUOTES_NUMBER = 20

def get_kw_quote():
  try:
    response = requests.get(KANYE_WEST_API_LINK)
  except:
    print("Connection error.")
    sys.exit(-1)

  data = json.loads(response.text)
  quote_str = data["quote"]
  status = response.status_code

  # basic error checking - there are way more errors tbh:()
  if status == 301:
    print("The URL of the requested resource has been changed permanently.")
    sys.exit(-1)
  elif status == 400:
    print("The server could not understand the request due to invalid syntax.")
    sys.exit(-1)
  elif status == 403:
    print("The client does not have access rights to the content.")
    sys.exit(-1)
  elif status == 404:
    print("Requested resource cannot be found.")
    sys.exit(-1)
  elif status == 503:
    print("The server is not ready to handle the request.")
    sys.exit(-1)

  return quote_str


def get_user_input():
  pass


def collect_kw_quotes(number):
  pass
  

def get_sentiment(sentence):
  pass


def separate_sentiment(quotes):
  pass
  

def display_result(sentiment_dict):
  pass


if __name__ == "__main__":
  pass
    