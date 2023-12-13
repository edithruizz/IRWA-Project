import pandas as pd

from myapp.core.utils import load_json_file
from myapp.search.objects import Document


_corpus = {}


def load_corpus(path) -> [Document]:
    """
    Load file and transform to dictionary with each document as an object for easier treatment when needed for displaying
     in results, stats, etc.
    :param path:
    :return:
    """
    df = _load_corpus_as_dataframe(path)
    df.apply(_row_to_doc_dict, axis=1)
    return _corpus


def _load_corpus_as_dataframe(path):
    """
    Load documents corpus from file in 'path'
    :return:
    """
    json_data = load_json_file(path)
    tweets_df = _load_tweets_as_dataframe(json_data)
    _clean_hashtags_and_urls(tweets_df)
    # Rename columns to obtain: Tweet | Username | Date | Hashtags | Likes | Retweets | Url | Language
    corpus = tweets_df.rename(
        columns={"id": "Id", "full_text": "Tweet", "screen_name": "Username", "created_at": "Date",
                 "favorite_count": "Likes",
                 "retweet_count": "Retweets", "lang": "Language"})

    # select only interesting columns
    filter_columns = ["Id", "Tweet", "Username", "Date", "Hashtags", "Likes", "Retweets", "Url", "Language",
                      "Title"]
    corpus = corpus[filter_columns]
    return corpus


def _load_tweets_as_dataframe(json_data):
    data = pd.DataFrame(json_data)
    # parse entities as new columns
    data['Url'] = data['entities'].apply(lambda x: x['urls'][0]['url'] if 'urls' in x and x['urls'] else '')

    data['Title'] = data['full_text'].apply(lambda x: x[:25])

    data = pd.concat([data.drop(['entities'], axis=1), data['entities'].apply(pd.Series)], axis=1)

    # parse user data as new columns and rename some columns to prevent duplicate column names
    data = pd.concat([data.drop(['user'], axis=1), data['user'].apply(pd.Series).rename(
        columns={"created_at": "user_created_at", "id": "user_id", "id_str": "user_id_str",
                 "lang": "user_lang"})], axis=1)
    return data


def _build_tags(row):
    tags = []

    for ht in row:
        tags.append(ht["text"])
    return tags	   	
																											   			   					

def _clean_hashtags_and_urls(df):
    df["Hashtags"] = df["hashtags"].apply(_build_tags)							   
    df.drop(columns=["entities"], axis=1, inplace=True)


def _row_to_doc_dict(row: pd.Series):
    _corpus[row['Id']] = Document(row['Id'], row["Title"], row['Tweet'], row['Date'], row['Likes'],
                                  row['Retweets'], row["Url"], row['Hashtags'])
    

def to_df(corpus):
    data_list = []

    for tweet_id, document in corpus.items():
        article_id = document.id
        tweet_text = document.description
        date = document.doc_date
        likes = document.likes
        retweets = document.retweets
        url = document.url
        hashtags = document.hashtags
        title = document.title

        data_list.append({ 'Tweet_Id': tweet_id, 'Tweet_Text': tweet_text, 'Date': date, 'Likes': likes,
            'Retweets': retweets, 'Url': url, 'Hashtags': hashtags, "Title" : title})

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)
    df["Title"] = df["Tweet_Text"].apply(lambda x: x[:50])
    return df