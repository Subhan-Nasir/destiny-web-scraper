import os
from dotenv import load_dotenv, find_dotenv
import requests
from pprint import pprint
import json
import time

load_dotenv(find_dotenv())



# Bungie membership types:
"""
None: 0
TigerXbox: 1
TigerPsn: 2
TigerSteam: 3
TigerBlizzard: 4
TigerStadia: 5
TigerEgs: 6
TigerDemon: 10
BungieNext: 254
All: -1

"""

start = time.time()

base_url = "https://www.bungie.net/Platform/"
headers = {

    "x-api-key": os.getenv("x-api-key")
}

def write_json_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json_file(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
    
    return data


def get_platform(membership_type):
    memberships_dict = {
        1: "Xbox",
        2: "Playstation",
        3: "Steam",
        4: "Blizzard",
        5: "Stadia",
        6: "Epic Games Store",
        10: "TigerDemon",
        254: "BungieNext",
        -1: "All"
    }

    return memberships_dict[membership_type]

def get_linked_profiles():
    membership_type = os.getenv("membership_type")
    membership_id = os.getenv("membership_id")

    endpoint = f"Destiny2/{membership_type}/Profile/{membership_id}/LinkedProfiles/"
    url = base_url + endpoint
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    pprint(response.json())


def get_user_profiles(username, bungie_num=False):
    
    endpoint = f"User/Search/GlobalName/{0}/"
    url = base_url + endpoint

    payload = json.dumps({
    "displayNamePrefix": username
    })
    
    response = requests.post(url, headers=headers, data=payload).json()
    
    if bungie_num:
        filtered_results = next(item for item in response["Response"]["searchResults"] if item["bungieGlobalDisplayNameCode"] == bungie_num)
        response["Response"]["searchResults"] = [filtered_results]


    # print("-"*150)
    # print("API RESPONSE:")
    # pprint(response)
    # print("-"*150)


    return response

def get_user_memberships(username, bungie_num= False):
    memberships = []
    api_response = get_user_profiles(username, bungie_num)
    # pprint(api_response)

    for item in api_response["Response"]["searchResults"][0]["destinyMemberships"]:
        id = item["membershipId"]
        membership_type = item["membershipType"]
        memberships.append({"id": id, "type": membership_type})

    return memberships


def get_account_stats(membership_id, membership_type):
    endpoint = f"Destiny2/{membership_type}/Account/{membership_id}/Stats/"
    url = base_url + endpoint

    payload = ""
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response
    

def get_clan_members(roster = 1):
    clan_id = 1903302 # Lord of fallen light
    if(roster == 2):
        clan_id == 4312074 # Lord of rising darkness
    

    endpoint = f"GroupV2/{clan_id}/Members"
    url = base_url + endpoint
    payload = ""

    response = requests.request("GET", url, headers=headers, data=payload).json()
    # pprint(response)
    
   
    clan_members = []
    for item in response["Response"]["results"]:

        destiny_info = item["destinyUserInfo"]

        bungie_name = destiny_info["bungieGlobalDisplayName"]
        bungie_num = destiny_info["bungieGlobalDisplayNameCode"]

        membership_id = destiny_info["membershipId"]
        membership_type = destiny_info["membershipType"]

        clan_members.append({
            "bungie_name": bungie_name,
            "bungie_num": bungie_num,
            "membership": {
                "membership_id": membership_id,
                "membership_type": membership_type
            }
        })

    with open('clan_members.json', 'w', encoding='utf-8') as f:
        json.dump(clan_members, f, ensure_ascii=False, indent=4)

    return clan_members




if __name__ == "__main__":

    # memberships = get_user_memberships("Spectre_561", 5179)
    # steam_membership = next(item for item in memberships if item["type"] == 3)
    # account_stats = get_account_stats(steam_membership["id"], steam_membership["type"])
    
    

    # with open('account_stats.json', 'w', encoding='utf-8') as f:
    #     json.dump(account_stats, f, ensure_ascii=False, indent=4)

    get_clan_members()



    end = time.time()
    print(f"RUNTIME = {round(end-start, 2)}seconds")



