import requests
import json
from pprint import pprint
from flask import Flask

# variable declaration
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}

def retrieve_chess_data(username: str, archived=False, url='') -> list | bool:
  if archived == True:
    response = requests.get(f'https://api.chess.com/pub/player/{username}/games/archives', headers=HEADERS)
  else:
    response = requests.get(url, headers=HEADERS)

  if str(response) == '<Response [404]>':     # fixed random username typed by the client or an error 404 from Chess.com
    return False

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
  with open(f'{USERNAME}.txt', 'a') as f:
        f.write(f'\nThe analysis for {color} openings by frequency:\n')
  for k, v in rankTheOpenings.items():
    for indivOpeningURL in v:
      indivOpeningList = indivOpeningURL.split('/')
      frequencyOfThisOpening = ecoDictFrequency[indivOpeningURL]
      print(f'{k}. {indivOpeningList[-1]} - played {frequencyOfThisOpening} time(s)!')
      with open(f'{USERNAME}.txt', 'a') as f:
        f.write(f'{k}. {indivOpeningList[-1]} - played {frequencyOfThisOpening} time(s)!\n')

def analysis_for_sideColors(listOfGames, username:str) -> tuple[dict, dict]:
  whiteEcoDictFrequency = {}
  BLACKEcoDictFrequency = {}
  for indivGame in listOfGames:
    if 'eco' not in indivGame: # prevents key value error
      continue
    if indivGame["eco"].split('/')[-1] == 'Undefined': # prevents the display of "Undefined"
      continue
    if determine_color_played(indivGame, username=username) == 'White':
      keyEcoSplitIndexNeg1 = indivGame["eco"].split('/')[-1]
      whiteEcoDictFrequency[keyEcoSplitIndexNeg1] = whiteEcoDictFrequency.get(keyEcoSplitIndexNeg1, 0) + 1
    if determine_color_played(indivGame, username=username) == 'Black':
          keyEcoSplitIndexNeg1 = indivGame["eco"].split('/')[-1]
          BLACKEcoDictFrequency[keyEcoSplitIndexNeg1] = BLACKEcoDictFrequency.get(keyEcoSplitIndexNeg1, 0) + 1   
    
  whiteRANKEDDictTallyColorEco =  dict(sorted(whiteEcoDictFrequency.items(), key=lambda item: item[1], reverse=True))
  blackRANKEDDictTallyColorEco =  dict(sorted(BLACKEcoDictFrequency.items(), key=lambda item: item[1], reverse=True))

  return whiteRANKEDDictTallyColorEco, blackRANKEDDictTallyColorEco

def analysis_for_black(listOfGamesBlack, username:str) -> dict:
  ecoDictFrequency = {}
  for indivGame in listOfGamesBlack:
    if 'eco' not in indivGame: # prevents key value error
        continue
    if determine_color_played(indivGame, username=username) == "Black":
      ecoDictFrequency[indivGame["eco"]] = ecoDictFrequency.get(indivGame["eco"], 0) + 1

  RANKEDDictTallyColorEco =  dict(sorted(ecoDictFrequency.items(), key=lambda item: item[1], reverse=True))

  return RANKEDDictTallyColorEco 

def determine_color_played(oneGame, username: str):
  usernamePlayedWhite = oneGame["white"]["username"]
  usernamePlayedWhite = usernamePlayedWhite.lower()
  #print(usernamePlayedWhite)
  if username == usernamePlayedWhite:
    return "White"
  else:
    return "Black"
  
def ranking(ecoFreq) -> dict:
  rankingDict = {}
  for opening in ecoFreq:
    frequencyOfOpening = ecoFreq[opening]
    rankingDict[frequencyOfOpening] = rankingDict.get(frequencyOfOpening, []) + [opening]
  rankingDictSorted = {k: v for k, v in sorted(rankingDict.items(), key=lambda item: item[0], reverse=True)}
  
  # reverse the key, example: 3 will be 1, 1 will be 3, to show ranking or priority

  rankingDescending = {}

  rankNumber = 1
  for key in rankingDictSorted:
    rankingDescending[rankNumber] = rankingDictSorted[key]
    rankNumber = rankNumber + 1  

  return rankingDescending

def compile_the_games(a_games: list, u_n: str):
  compilation_of_games = []

  for monthPlayedUrl in a_games:
    games = retrieve_chess_data(url=monthPlayedUrl, username=u_n)
    compilation_of_games = compilation_of_games + games

  return compilation_of_games


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
  archived_games = retrieve_chess_data(username=USERNAME, archived=True)

  compilation_of_games = compile_the_games(archived_games)

  print("""Which side of your games would you like to analyze?
        (1) White
        (2) Black
        (3) Both
  """)
  choice = input()

  if choice == '1':
    analysis_for_sideColors(compilation_of_games)
  if choice == '2':
    analysis_for_black(compilation_of_games)
  if choice == '3': 
    analysis_for_sideColors(compilation_of_games)
    analysis_for_black(compilation_of_games)
  else:
    exit()
  
  print(f"\nResults saved inside {f'{USERNAME}.txt'}")


  
  