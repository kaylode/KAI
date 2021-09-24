import os
import json
import requests
import base64
from io import BytesIO
import pandas as pd

from .base import API
import discord

def pretty_format(dict, mapping_dict=None, index=False):
    if mapping_dict is None:
        mapping_dict = {key:key for key in list(dict.keys())}

    new_dict = {mapping_dict[key]:[value] for key, value in dict.items() if key in mapping_dict.keys()}

    df = pd.DataFrame(new_dict)

    pd.set_option('display.max_columns', None)  # or 1000
    pd.set_option('display.max_rows', None)  # or 1000
    pd.set_option('display.max_colwidth', None)  # or 199
    return df.to_string(index=index)

class CovidAPI(API):
    """
    Covid19 Information API
    https://documenter.getpostman.com/view/10808728/SzS8rjbc
    """
    def __init__(self) -> None:
        super().__init__()
        self.triggers = ["$covid"]
        self.url = "https://api.covid19api.com/"
        # 'https://api.covid19api.com/country/vietnam/status/{confirmed, recovered, deaths}'

    def do_command(self, command, trigger):
        """
        Execute command
        """
        response = None
        reply = False

        # After set url, start predicting on image url
        # Example call: $food predict https://xxxx/food.png
        if command.startswith('summary'):
            country_name = command.split('summary')[-1].lstrip().rstrip()
            # Construct discord File from buffer and filename
            response = self.get_summary(country_name)
            reply = False

        return response, reply

    def send_request(self, url, data, type, headers, **kwargs):
        """
        Send request API call
        """
        return super().send_request(url, data, type, headers=headers, **kwargs)
    
    def process_response(self, response, country_name):
        """
        Process response from server
        """
        try:
            data = response.json()  
            if 'message' not in data.keys():

                if country_name == 'global':
                    covid_info = data["Global"] # a dict

                    """
                    "NewConfirmed": 100282,
                    "TotalConfirmed": 1162857,
                    "NewDeaths": 5658,
                    "TotalDeaths": 63263,
                    "NewRecovered": 15405,
                    "TotalRecovered": 230845
                    """

                    extracted_keys = {
                      "TotalConfirmed": "Confirmed",
                      "TotalDeaths": "Deaths",
                      "TotalRecovered": "Recovered"
                    }
                else:
                    countries_info = data["Countries"] # a list of dict

                    """
                    "Country": "Viet Nam",
                    "CountryCode": "VN",
                    "Slug": "vietnam",
                    "NewConfirmed": 3,
                    "TotalConfirmed": 240,
                    "NewDeaths": 0,
                    "TotalDeaths": 0,
                    "NewRecovered": 5,
                    "TotalRecovered": 90,
                    "Date": "2020-04-05T06:37:00Z"
                    """

                    extracted_keys = {
                      "Country": "Country",
                      "TotalConfirmed": "Confirmed",
                      "TotalDeaths": "Deaths",
                      "TotalRecovered": "Recovered",
                      "Date": "Date"
                    }

                    covid_info = {}
                    for country in countries_info:
                        if country['Slug'] == country_name:
                            covid_info = country
                            break
                
                response = pretty_format(covid_info, extracted_keys)           
            else:
                response = f"[Error] Request code {data['code']}"
                return               
        except Exception as e:
            response = "[Error] " + str(e)

        return response

    def get_summary(self, country_name):
        """
        Main method to send request and return buffer of result image
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        url = os.path.join(self.url, 'summary')

        if country_name == '':
            country_name = 'global'

        payload = {}

        # Send request
        response = self.send_request(url, payload, type='get', headers=headers, country_name=country_name)
        
        return response
            
    def get_case_by_date(self, country_name):
        """
        Main method to send request and return buffer of result image
        """
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        if country_name == '':
            pass

        payload = {}

        # Send request
        response = self.send_request(self.url, payload, type='get', headers=headers)
        
        return response