from requests_html import HTMLSession
from pprint import pprint
from bs4 import BeautifulSoup
import json
from api_test import write_json_file

def get_pvp_stats(memberID):
    '''
    Each 'segment' is an activity, e.g. Rumble
    There is a 'segment' called 'Lifetime' and it's tags are:

    {'abilityKills', 'activitiesEntered', 'activitiesWon', 'assists', 'assistsPga', 'averageLifeSpan', 'avgKillDistance', 'avgScorePerKill', 'avgScorePerLife', 
    'bestSingleGameKills', 'bestSingleGameScore', 'combatRating', 'competitiveLevel', 'competitiveRating', 'deaths', 'defensiveKills', 'dominationKills', 
    'efficiency', 'gloryLevel', 'gloryRating', 'infamyLevel', 'infamyRating', 'kad', 'kd', 'kills', 'killsPga', 'longestKillSpree', 'longestSingleLife', 
    'minutesPlayedTotal', 'mostPrecisionKills', 'objectivesCompleted', 'offensiveKills', 'orbsDropped', 'orbsDroppedPerGame', 'orbsGathered', 'orbsGatheredPerGame', 
    'precisionKills', 'relicsCaptured', 'relicsCapturedPerGame', 'resurrectionsPerformed', 'resurrectionsReceived', 'score', 'scorePga', 'secondsPlayed', 
    'siteScore', 'suicides', 'superKills', 'totalKillDistance', 'trialsFlawless', 'valorLevel', 'valorRating', 'wl', 'zonesCaptured', 'zonesNeutralized'}

    All the rest have these tags but if player has not played activity, some, like 'elo' might be missing.

    {'abilityKills', 'activitiesCleared', 'activitiesEntered', 'activitiesWon', 'assists', 'assistsPga', 'averageLifeSpan', 'avgKillDistance', 'avgScorePerKill', 
    'avgScorePerLife', 'bestSingleGameKills', 'bestSingleGameScore', 'combatRating', 'deaths', 'defensiveKills', 'dominationKills', 'efficiency', 'elo', 
    'grenadeKills', 'kad', 'kd', 'kills', 'killsPga', 'longestKillSpree', 'longestSingleLife', 'meleeKills', 'milestonesCompleted', 'minutesPlayedTotal', 
    'mostPrecisionKills', 'objectivesCompleted', 'offensiveKills', 'orbsDropped', 'orbsDroppedPerGame', 'orbsGathered', 'orbsGatheredPerGame', 'precisionKills', 
    'publicEventsCompleted', 'rank', 'relicsCaptured', 'relicsCapturedPerGame', 'resurrectionsPerformed', 'resurrectionsReceived', 'score', 'scorePga', 'secondsPlayed', 
    'siteScore', 'suicides', 'superKills', 'totalKillDistance', 'winloss', 'wl', 'zonesCaptured', 'zonesNeutralized'}
    '''
    
    session = HTMLSession()

    r = session.get(f"https://destinytracker.com/destiny-2/profile/steam/{memberID}/overview")
    r.html.render()

    soup = BeautifulSoup(r.html.html, 'html.parser')
    writing = str(soup.find_all('script')[5])[35:-9]
    converted = json.loads(writing)
    pvp_stats = []
    for segment in converted['stats']['standardProfiles'][0]['segments']:
        if segment['metadata']['name'] != 'Lifetime' and 'elo' in [*segment['stats'].keys()]:

            # print(segment['metadata']['name'])

            # pprint(segment['stats']['elo'])

            pvp_stats.append({
                "playlist": segment['metadata']['name'],
                "elo": segment['stats']['elo']['value'],
                "global_rank": segment['stats']['elo']['rank'],
                "global_percentile": segment['stats']['elo']['percentile'],
                "rank_name": segment['stats']['elo']['metadata']['rankName'],
                "rank_colour": segment['stats']['elo']['metadata']['rankColor'],
                "rank_icon": segment['stats']['elo']['metadata']['iconUrl']
            })
    

    return pvp_stats
    

if __name__ == '__main__':
    player_pvp_stats = get_pvp_stats(4611686018489941615)