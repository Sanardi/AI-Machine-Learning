import requests
import pandas as pd
import regex as re
import random
#from collections import OrderedDict
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse, urllib.error
import time;
from random import randint
import os
import os.path

def write_df_to_mongoDB(  my_df,\
                          database_name = 'ZED' ,\
                          collection_name = 'horses',\
                          server = '0.0.0.0',\
                          mongodb_port = 27017,\
                          chunk_size = 100):


    #To connect
    import os
    import pandas as pd
    import pymongo
    from pymongo import MongoClient

    client = MongoClient('localhost',int(mongodb_port))
    db = client[database_name]
    collection = db[collection_name]
    # To write
    my_df.reset_index(inplace=True)
    my_list = my_df.to_dict('records')


    collection.insert_many(my_list)
    return


import regex as re
import random
#from collections import OrderedDict
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse, urllib.error
import time;
from random import randint
import pandas as pd
import requests
from datetime import date, timedelta, datetime

import json
from datetime import date, timedelta, datetime







class ScrapeZed:
    def __init__(self, url = "https://zed-ql.zed.run/graphql" ):

        self.url = url
        self.key = "<Some_keys>"
        #self.localtime = datetime.strftime(self.today, '%Y-%m-%d')





    def __str__(self):
        return '''This Class lets you scrape a GRAPHQL database,
        and can be used for AI and Machine Learning Clssification and Prediction Tasks'''

    def get_date_range(self):
        today = date.today()
        dates = []

        time_delta = 1
        today_q = datetime.strftime(today, '%Y-%m-%d')

        date_range = today - timedelta(days=int(time_delta))
        start_date= datetime.strftime(date_range, '%Y-%m-%d')

        dates.append(start_date + " 00:00:00")
        dates.append(today_q + " 23:59:00")
        return dates


    def _make_request(self, url):
        key = self.key
        dates = self.get_date_range()

        body = """query ($input: GetRaceResultsInput, $before: String, $after: String, $first: Int, $last: Int) {
  getRaceResults(before: $before, after: $after, first: $first, last: $last, input: $input) {
    edges {
      cursor
      node {
        country
        city
        name
        length
        startTime
        fee
        raceId
        weather
        status
        class
        prizePool {
          first
          second
          third
        }
        horses {
          horseId
          finishTime
          finalPosition
          name
          gate
          ownerAddress
          bloodline
          gender
          breedType
          gen
          coat
          hexColor
          imgUrl
          class
          stableName
        }
      }
    }
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
  }
}"""

        variables = """{
	"first": 100,
	"input": {
		"onlyMyRacehorses": false,
		"location": {
			"country": "Canada"

		},
		"dates": {
			"from":  \"""" + str(dates[0]) + """", "to": \"""" + str(dates[1]) + """"
		},
		"distance": {
			"from": 1000,
			"to": 2400
		},
		"classes": [
			1,
			2,
			3,
			4
		]
	}
}"""



        try:


            #acessing the website:
            #user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
            headers={'User-Agent':user_agent,}

            #response = make_good_request(url)

            r = requests.post(url, json={'query': body, 'variables' : variables}, headers={"content-type":"application/json", "x-developer-secret" : key})
            print(r.status_code)

            asjson = r.text
            time.sleep(randint(1,5))
            return asjson



        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(e)
            #time.sleep(10)





    def _get_df(self):

        all_data= []

        count = 0
        try:
            asjson = self._make_request(self.url)
            #print(offer.prettify)
            asdict = json.loads(asjson)
            print(asdict)
            asdict = asdict["data"]["getRaceResults"]["edges"]
            race_count = 0
            while len(asdict[race_count]) > 0:
                justins_horses = asdict[race_count]

                horses = justins_horses['node']['horses']
                df = pd.DataFrame(horses)

                df["city"] = justins_horses['node']['city']
                df["country"] = justins_horses['node']['country']
                df["fee"] = justins_horses['node']['fee']
                df["weather"] = justins_horses['node']['weather']
                df["length"] = justins_horses['node']['length']
                df["status"] = justins_horses['node']['status']
                df["startTime"] = justins_horses['node']['startTime']
                df["raceId"] = justins_horses['node']['raceId']
                df["raceName"] = justins_horses['node']['name']
                df["first_price "]= justins_horses['node']['prizePool']["first"]
                df["second_price"] = justins_horses['node']['prizePool']["second"]
                df["third_prize"] = justins_horses['node']['prizePool']["third"]
                print(df.head())
                #needs to go into mongo here

                write_df_to_mongoDB(df, database_name = 'ZED' ,
                collection_name = 'races',)
                print("*****************************************************************************************")
                race_count += 1
                print("way to go")


        except Exception as e:
            print(e)





    def run(self):
        print("I will now scrape ZED")
        self._get_df()
        return "races inserted sucessfully into collection horses"





if __name__ == "__main__":
    ScrapeZed().run()
