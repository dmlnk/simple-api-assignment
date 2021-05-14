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
  if (MIN_QUOTES_NUMBER > MAX_QUOTES_NUMBER):
    print("Wrong min and max quotes number is set. Min must be lower than max!")
    return -1
  
  number = int(input("Type number of Kanye West's quotes you'd like to pull (from %d to %d inclusive): " % (MIN_QUOTES_NUMBER, MAX_QUOTES_NUMBER)))
    
  if not (MIN_QUOTES_NUMBER <= number <= MAX_QUOTES_NUMBER):
    print("Number must be between %d and %d inclusive" % (MIN_QUOTES_NUMBER, MAX_QUOTES_NUMBER))
    return -1
  
  return number


def collect_kw_quotes(number):
  quotes = set()
  
  while(len(quotes) < number):
    quotes.add(get_kw_quote())
    
  return quotes
  

def get_sentiment(sentence):
  text = {"text" : sentence}
  response = requests.post(SENTIM_API_LINK,data=json.dumps(text), headers=SENTIM_PARAMS)
  data = json.loads(response.text)

  return data["result"]["polarity"]


def separate_sentiment(quotes):
  sentiment_dict = {"Positive": {}, "Negative": {}, "Neutral": {}}

  for quote in quotes:
    polarity = get_sentiment(quote)
    if polarity > 0:
      sentiment_dict["Positive"][quote] = polarity

    elif polarity < 0:
      sentiment_dict["Negative"][quote] = polarity

    elif polarity == 0:
      sentiment_dict["Neutral"][quote] = polarity

  return sentiment_dict
  

def display_result(sentiment_dict):
  for sent_str, dict in sentiment_dict.items():
    print(sent_str + " sentences count - %d:" % (len(sentiment_dict[sent_str])))

    for sentence, polarity in dict.items():
      print(sentence + " (polarity - %s)" % (polarity))
    print()

  if len(sentiment_dict["Negative"]) > 0:
    print("The most negative quote is - '%s' (polarity - %s)" % (min(sentiment_dict["Negative"].items(), key=lambda x: x[1])))

  if len(sentiment_dict["Positive"]) > 0:
    print("The most positive quote is - '%s' (polarity - %s)" % (max(sentiment_dict["Positive"].items(), key=lambda x: x[1])))



if __name__ == "__main__":
  number = get_user_input()
  quotes = set()

  if (number != -1):
    quotes = collect_kw_quotes(number)
    sentiment_dict = separate_sentiment(quotes)
    display_result(sentiment_dict)
  else:
    print("An error has occured.")
    sys.exit(-1)
    