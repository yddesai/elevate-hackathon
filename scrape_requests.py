import requests
import time
import google.generativeai as genai
import logging 
from noDV import noDV
base_url = 'https://portal.scscourt.org/api/case/validate/'

bearer = os.environ['bearer_token']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    f'Authorization': 'Bearer {bearer}',
    'Connection': 'keep-alive',
    'Referer': 'https://portal.scscourt.org/case/NDc2MDcyOA==',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'If-Modified-Since': 'Wed, 10 Jan 2024 00:26:19 GMT',
    'If-None-Match': '"2ee97a15b43da1:0"',
    'TE': 'trailers'
}

restraining_order_keywords = {
    "Order: Restraining Order After Hearing",
    "Order: ROAH",
    "Restraining Order After Hearing",
    "ROAH", 
    "DV-130"
}

def extract_filter_data():
    for i in range(1, 4254):
        case_number = f'23DV{str(i).zfill(6)}'
        url = base_url + case_number
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            print(f"Case {case_number} validated successfully.")
            # Do something with the response if needed
            data = response.json()
            
            try:
                id_number = data['data'][0]['id']
            except IndexError as e:
                msg = data["message"]
                logging.warning(f"Error {msg}")
                continue
            url = f"https://portal.scscourt.org/api/case/{id_number}"
            try:
                response = requests.get(url, headers=HEADERS)
                data = response.json()
            except Exception as e:
                print(f"Error {e} for case {case_number}")
                continue
            
            # Check if the case is a restraining order case
            try:
                if data:   
                    try:
                        parsed_data = data['data']
                    except KeyError as e:
                        parsed_data = data  
                    try:
                        party1, party2 = parsed_data['caseParties'][0], parsed_data['caseParties'][1]
                    except Exception as e:
                        print(f"Failed to parse data for case {case_number}. Error: {e}")
                        continue
                    
                    if party1['type'] == 'Petitioner':
                        petitioner_name = party1['firstName'] + '  ' + party1['lastName']
                        respondent_name = party2['firstName'] + '  ' + party2['lastName']
                    else:
                        petitioner_name = party2['firstName'] + party2['lastName']
                        respondent_name = party1['firstName'] + party1['lastName']

                    case_number = parsed_data['caseNumber']
                    case_attornies = parsed_data['caseAttornies']
                    print(case_attornies)
                    if not case_attornies:
                        case_attorny1, case_attorny2 = '', ''
                        petitioner_rep, respondent_rep = '', ''
                    elif len(case_attornies) == 1:
                        case_attorny1 = case_attornies[0]
                        case_attorny2 = ''
                        petitioner_rep, respondent_rep = '', ''
                    else:
                        case_attorny1, case_attorny2 = case_attornies[0], case_attornies[1]
                        if case_attorny1['representing'] == petitioner_name:
                            petitioner_rep = case_attorny1['firstName'] + '  ' + case_attorny1['lastName']
                            respondent_rep = case_attorny2['firstName'] + '  ' + case_attorny2['lastName']
                        else:
                            petitioner_rep = case_attorny2['firstName'] + case_attorny2['lastName']
                            respondent_rep = case_attorny1['firstName'] + case_attorny1['lastName']
                        
                    petitioner_rep_val = 'Y' if case_attorny1 != '' else 'N'
                    respondent_rep_val = 'Y' if case_attorny2 != '' else 'N'

                    case_events = parsed_data['caseEvents']
                    n = len(case_events)
                    
                    if is_restraining_order(case_events):
                        restraing_order_val = 'Y'
                    else:
                        restraing_order_val = 'N'
                    # write to csv 
                    with open("cases.csv", "a") as f:
                        # if not noDV(data):
                        f.write(f"{case_number},{petitioner_rep_val},{respondent_rep_val},{restraing_order_val}\n")
                
            except Exception as e:
                    print(f"Error {e} for case {case_number}")


def is_restraining_order(events):
    for event in events:
        if event['type'] in restraining_order_keywords or event['comment'] in restraining_order_keywords:
            return True 
    return False

# 23fl004253
# 23dv001069
if __name__ == "__main__":
    extract_filter_data()