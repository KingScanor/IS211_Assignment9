# Assignment 9 Part 1
import requests
from bs4 import BeautifulSoup


def football_stats(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='TableBase-table')
    body = table.find('tbody')
    rows = body.find_all('tr')

    top_players = []
    for row in rows[:20]:
        cols = row.find_all('td')
        try:
            player_info = cols[0].text.strip().replace("\n", "").replace(" ", "")
            name = player_info.split("QB")[0]
            position = "QB"
            team =  player_info.split("QB")[1]
            team_code = team[:3] if len(team) > 2 else team

            player_data = {
                'position': position,
                'player': name,
                'team': team_code,
                'touchdowns': int(float(cols[8].text.strip()))
            }
            top_players.append(player_data)
        except (IndexError, ValueError) as e:
            print (f"Error processing the following row: {row.text.strip()} - {e}")

    return top_players

if __name__ == "__main__":
    url = "https://www.cbssports.com/nfl/stats/player/passing/nfl/regular/qualifiers/?sortcol=td&sortdir=descending"
    top_20_touchdowns = football_stats(url)

    print ("NFL top 20 passing TDs Season 24-25\n")

    for i, player in enumerate(top_20_touchdowns):
        print (f"{i + 1}. {player['player']} / {player['position']} / {player['team']} / {player['touchdowns']} TDs")

