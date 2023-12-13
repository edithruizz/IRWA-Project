import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """ 
    # statistics table 1
    # statistics for queries
    fact_terms = dict([])           # count
    fact_number_terms = dict([])    # query lenght
    fact_query_times = dict([])     # count
    
    # statistics table 2
    # statistics for document results
    fact_clicks = dict([])      # click counter
    fact_rankings = dict([])    # counter
    fact_queries = dict([])     # list of queries
    fact_dwell_time = dict([])  # total time spend inside the document

    # statistics table 3
    # statistics for user contex
    fact_browser = dict([])     # count browser
    fact_OS = dict([])          # count os
    fact_time = dict([])        # count hour
    fact_date = dict([])        # count date
    fact_ip = dict([])          # count ip
    
    # statistics for sessions
    fact_num_queries = dict([]) # number of searches
    fact_num_detail = dict([])  # number of clicked documents

    
    def save_query_terms(self, terms: str) -> int:
        print(self)
        return random.randint(0, 100000)


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter
        
    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
