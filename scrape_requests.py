import requests

base_url = 'https://portal.scscourt.org/api/case/validate/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6IjY0NXN4eHVhbiIsInN1YiI6ImluZm9AZWxldmF0ZWNvbW11bml0eWNlbnRlci5vcmciLCJyb2xlIjpbIkFETUlOIiwiTm9uZSJdLCJlbWFpbCI6ImluZm9AZWxldmF0ZWNvbW11bml0eWNlbnRlci5vcmciLCJncm91cHNpZCI6IjY0NSIsImpwYXdyb2xlIjoiQURNSU4iLCJqcGF3dHlwZSI6Ik5vbmUiLCJwYXNzd29yZCI6IkZhbHNlIiwicG9saWN5IjoiRmFsc2UiLCJmZWF0dXJlcyI6IltdIiwiaXNzIjoibXNjb3VydHMiLCJhdWQiOiIwOTkxNTNjMjYyNTE0OWJjOGVjYjNlODVlMDNmMDAyMiIsImV4cCI6MTcxMTg0MTkzNSwibmJmIjoxNzExODIzOTM1fQ.OeHB1b9VkQNir6CUrfWvtA0j-hhBpE9TxY4p-4a-1F4',
    'Connection': 'keep-alive',
    'Referer': 'https://portal.scscourt.org/case/NDc2MDcyOA==',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'If-Modified-Since': 'Wed, 10 Jan 2024 00:26:19 GMT',
    'If-None-Match': '"2ee97a15b43da1:0"',
    'TE': 'trailers'
}

for i in range(1, 2102):
    case_number = f'23FL{str(i).zfill(6)}'
    url = base_url + case_number
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            print(f"Case {case_number} validated successfully.")
            # Do something with the response if needed
            data = response.json()
            id_number = data['data'][0]['id']
            url = f"https://portal.scscourt.org/api/case/{id_number}"
            response = requests.get(url, headers=headers)
            data = response.json()
            if data:   
                parsed_data = data['data']
                party1, party2 = parsed_data['caseParties'][0], parsed_data['caseParties'][1]
                if party1['type'] == 'Petitioner':
                    petitioner_name = party1['firstName'] + '  ' + party1['lastName']
                    respondent_name = party2['firstName'] + '  ' + party2['lastName']
                else:
                    petitioner_name = party2['firstName'] + party2['lastName']
                    respondent_name = party1['firstName'] + party1['lastName']
                
                case_number = parsed_data['caseNumber']
                case_attornies = parsed_data['caseAttornies']
                case_attorny1, case_attorny2 = case_attornies[0], case_attornies[1]
                if case_attorny1['representing'] == petitioner_name:
                    petitioner_rep = case_attorny1['attorneyName']
                    respondent_rep = case_attorny2['attorneyName']
                else:
                    petitioner_rep = case_attorny2['attorneyName']
                    respondent_rep = case_attorny1['attorneyName']
          
                petitioner_rep_val = 'Y' if case_attorny1 != '' else 'N'
                respondent_rep_val = 'Y' if case_attorny2 != '' else 'N'

                # write to csv 
                with open("cases.csv", "a") as f:
                    f.write(f"{case_number},{petitioner_rep},{respondent_rep}\n")
           
        except Exception as e:
            print(f"Failed to validate case {case_number}. Error: {e}")
            # Log the case number where exception occurred
            with open("exception_log.txt", "a") as f:
                f.write(f"{case_number}\n")
            continue
    else:
        print(f"Failed to validate case {case_number}. Status code: {response.status_code}")
