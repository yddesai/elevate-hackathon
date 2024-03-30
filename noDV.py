def noDV(json):     #json is full json file for a case
    items = json.get("data")    #extracts caseEvents data from raw datafile
    events = items.get("caseEvents")
    for i in events:
        if "DV" in i.get("comment") or "domestic violence" in i.get("comment"):     #go through each event searching for keywords in the comments
            return True
    return False    #return False to indicate there are no mentions of DV
    
    


