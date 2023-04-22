import json
from pprint import pprint
from webscraper_test import get_pvp_stats
from api_test import get_platform, read_json_file, write_json_file


    

if __name__ == "__main__":
    clan_members = read_json_file("clan_members.json")

    pvp_leaderboard = []

    

    for item in clan_members:
        print(f"Trying to read for {item['bungie_name']}#{str(item['bungie_num']).zfill(4)}")
        try:
            pvp_stats = get_pvp_stats(item["membership"]["membership_id"])
        except:
            pvp_stats = "Error"

        pvp_leaderboard.append({
            "player":{
                "username": item["bungie_name"],
                "bungie_num": item["bungie_num"],
            },
            "pvp_stats": pvp_stats
        })

    write_json_file("pvp_leaderboard.json", pvp_leaderboard)

    # pprint(clan_members)
