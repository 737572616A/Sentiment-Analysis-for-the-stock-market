import requests
from classify import classifyIt
import yaml


def create_twitter_url():
    max_results = 100
    mrf = "max_results={}".format(max_results)
    q = "query=%23marketupdate+%23nifty"
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        mrf, q
    )
    return url


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]


def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def main():
    url = create_twitter_url()
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    print(res_json)
    netsent = dict()
    stuff = res_json['data']
    for x in stuff:
        # print(x['text'])
        vals = classifyIt(x['text'])
        # print(vals)
        for sent in vals:
            netsent[sent['sentiment']] = netsent.get(sent['sentiment'], 0) + 1
    #print(netsent)
    neutral_percent = netsent['neutral']/3
    neutral_percent = float("{:.2f}".format(neutral_percent))
    bull_percent = netsent['bullish']/3
    bull_percent = float("{:.2f}".format(bull_percent))
    bear_percent = netsent['bearish']/3
    bear_percent = float("{:.2f}".format(bear_percent))
    print("percent of neutral sentiment on twitter: ", neutral_percent, "\npercent of bullish sentiment on twitter: ", bull_percent, "\npercent of bearish sentiment on twitter: ", bear_percent)

if __name__ == '__main__':
    main()
