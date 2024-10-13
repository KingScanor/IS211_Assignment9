# Assignment 9 Part 2

import requests
from bs4 import BeautifulSoup


def nba_stats(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="TableBase-table")
    body = table.find("tbody")
    rows = body.find_all("tr")

    top_players = []
    for row in rows[:20]:
        cols = row.find_all("td")
        try:

            player_info = cols[0].text.strip().replace("\n", "")

            info_parts = player_info.split()
            name = " ".join(info_parts[:-6])
            position = info_parts[-2]
            team = info_parts[-1]

            ppg = float(cols[4].text.strip())

            player_data = {
                "player": name,
                "position": position,
                "team": team,
                "ppg": ppg,
            }
            top_players.append(player_data)
        except (IndexError, ValueError) as e:
            print (f"Error processing the following row: {row.text.strip()} - {e}")

    return top_players

if __name__ == "__main__":
    url = "https://www.cbssports.com/nba/stats/player/scoring/nba/regular/all-pos/qualifiers/?sortdir=descending&sortcol=ppg"
    top_20_ppg = nba_stats(url)

    print("NBA top 20 PPG season 24-25 \n")

    for i, player in enumerate(top_20_ppg):
        print (f"{i + 1}. {player['player']} / {player['position']} / {player['team']} / {player['ppg']} PPG")
