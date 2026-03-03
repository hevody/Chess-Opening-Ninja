import requests
import json
from pprint import pprint
from flask import Flask

# variable declaration
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}
USERNAME = ''
RESULTS_FILE = 'results.txt'

def retrieve_chess_data(archived=False, url=''):
  print(url)
  if archived == True:
    response = requests.get(f'https://api.chess.com/pub/player/{USERNAME}/games/archives', headers=HEADERS)
  else:
    response = requests.get(url, headers=HEADERS)
  
  response.encoding = "utf-8"
  retrieved_games = response.json()
  if archived == False:
    retrieved_games = retrieved_games["games"]
  else:
    retrieved_games = retrieved_games["archives"]
  return retrieved_games

# proof of concept, functions as parser of all chess data, get all what is inside the games key such that [value] + [value] + [value] = [values with dictionaries inside]
# def save_chess_data():
#   list_of_games = archived_games['archives']
#   for individual_gamesURL in list_of_games:
#     response = requests.get(individual_gamesURL, headers=HEADERS)
#     with open(LOCAL_FILENAME, 'ab') as f:
#       for chunk in response.iter_content(chunk_size=8192):
#         f.write(chunk)

def presentationOfData(ecoDictFrequency, color=''):
  rankTheOpenings = ranking(ecoDictFrequency)  

  # print the results
  print(f"\nThe analysis for {color} openings by frequency:")
  with open(RESULTS_FILE, 'a') as f:
        f.write(f'\nThe analysis for {color} openings by frequency:\n')
  for k, v in rankTheOpenings.items():
    for indivOpeningURL in v:
      indivOpeningList = indivOpeningURL.split('/')
      frequencyOfThisOpening = ecoDictFrequency[indivOpeningURL]
      print(f'{k}. {indivOpeningList[-1]} - played {frequencyOfThisOpening} time(s)!')
      with open(RESULTS_FILE, 'a') as f:
        f.write(f'{k}. {indivOpeningList[-1]} - played {frequencyOfThisOpening} time(s)!\n')

def analysis_for_white(listOfGamesWhite):
  #  determine if the player is White
  ecoDictFrequency = {}
  for indivGame in listOfGamesWhite:
    if 'eco' not in indivGame: # prevents key value error
        continue
    if determine_color_played(indivGame) == "White":
      ecoDictFrequency[indivGame["eco"]] = ecoDictFrequency.get(indivGame["eco"], 0) + 1

  presentationOfData(ecoDictFrequency, color='White')

def analysis_for_black(listOfGamesBlack):
  # determine if the player is Black
  ecoDictFrequency = {}
  for indivGame in listOfGamesBlack:
    if 'eco' not in indivGame: # prevents key value error
        continue
    if determine_color_played(indivGame) == "Black":
      ecoDictFrequency[indivGame["eco"]] = ecoDictFrequency.get(indivGame["eco"], 0) + 1

  presentationOfData(ecoDictFrequency, color='Black')

def determine_color_played(oneGame):
  usernamePlayedWhite = oneGame["white"]["username"]
  usernamePlayedWhite = usernamePlayedWhite.lower()
  #print(usernamePlayedWhite)
  if USERNAME == usernamePlayedWhite:
    return "White"
  else:
    return "Black"
  
def ranking(ecoFreq):
  rankingDict = {}
  for opening in ecoFreq:
    frequencyOfOpening = ecoFreq[opening]
    rankingDict[frequencyOfOpening] = rankingDict.get(frequencyOfOpening, []) + [opening]
  rankingDictSorted = {k: v for k, v in sorted(rankingDict.items(), key=lambda item: item[0], reverse=True)}
  
  # reverse the key, example: 3 will be 1, 1 will be 3, to show ranking or priority

  rankingAscending = {}

  rankNumber = 1
  for key in rankingDictSorted:
    rankingAscending[rankNumber] = rankingDictSorted[key]
    rankNumber = rankNumber + 1  

  return rankingAscending


if __name__ == '__main__':
  
  print("\nAnalyze the openings you play the most!")
  print("Improve your attacks and counterattacks by the frequency of replies your opponents made\n")

  print("What is your username?")
  USERNAME = input()
  USERNAME = USERNAME.lower()
  print("\nPlease wait while we're calling the Chess.com API...\n")

  # games = retrieve_chess_data(url='https://api.chess.com/pub/player/hevory/games/2026/02')
  # print(games)
  # ANALYZE_FOR_MONTH
  # analysis_for_black(games)

  # ANALYZE FOR YEAR
  archived_games = retrieve_chess_data(archived=True)

  compilation_of_games = []

  for monthPlayedUrl in archived_games:
    games = retrieve_chess_data(url=monthPlayedUrl)
    compilation_of_games = compilation_of_games + games

  print("""Which side of your games would you like to analyze?
        (1) White
        (2) Black
        (3) Both
  """)
  choice = input()

  if choice == '1':
    analysis_for_white(compilation_of_games)
  if choice == '2':
    analysis_for_black(compilation_of_games)
  if choice == '3': 
    analysis_for_white(compilation_of_games)
    analysis_for_black(compilation_of_games)
  else:
    exit()
  
  print(f"\nResults saved inside {RESULTS_FILE}")


  
  