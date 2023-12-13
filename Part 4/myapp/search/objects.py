import json


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, url, count, is_top10, queries_related, dwell_time):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count
        self.is_top10 = is_top10
        self.queries_related = queries_related
        self.dwell_time = dwell_time

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsQuery:
    """
    Query data as an object
    """

    def __init__(self, query, length, times_searched):
        self.query = query
        self.length = length
        self.times_searched = times_searched
        
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsSession:
    """
    Query data as an object
    """

    def __init__(self, browsers, OSs, ips, times, dates, num_searches, num_doc_details):
        self.browsers = browsers
        self.OSs = OSs
        self.ips = ips
        self.times = times
        self.dates = dates
        self.num_searches = num_searches
        self.num_doc_details = num_doc_details

        
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, title, description, date, url, ranking=None):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.url = url
        self.ranking = ranking