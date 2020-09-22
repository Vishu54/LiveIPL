import requests
import time
from plyer import notification

#global variables
title=''
lastScore=''
currentScore=''
def getUrl():
    global title,lastScore
    try:
        resp=requests.get('http://mapps.cricbuzz.com/cbzios/match/livematches')
        data=resp.json()
    except Exception as e:
        title ="Cannot Connect!!"
    return data

def sys_notify(title,message):
    try:
        notification.notify(title,message,timeout=5)
    except:
        print('error')


def getData(data):
    global title,lastScore,currentScore
    team1=''
    team2=''
    result=''
    status=''

    team={'Chennai Super Kings':'CSK','Mumbai Indians':'MI','Kolkata Knight Riders':'KKR','Sunrisers Hyderabad':'SR',
    'Rajasthan Royals':'RR','Kings XI Punjab':'KXIP','Royal Challengers Bangalore':'RCB','Delhi Capitals':'DC'}

    for i in range(0,10):
        result=data['matches'][i]['header']['status']
        #Checking the match is ipl or not and has started or not
        if data['matches'][i]['series_name'] == 'Indian Premier League 2020' and 'Starts' not in result:
            break
        # else:
        #     return 'Invalid'

    if 'won' or 'loss' in result:
       return result
    
    #Getting teams names

    team1=data['matches'][i]['team1']['name']
    if team1 in team.keys():
        team1=team[team1]
    team2=data['matches'][i]['team2']['name']
    if team2 in team.keys():
        team2=team[team2]

    #Checking if there any problem
    if "Cannot Connect!!" in title:
        pass
    else:
        title=team1 + " VS "+ team2

    print(title)

    #Getting current score

    try:
        score = data['matches'][i]['bat_team']['innings'][0]['score']
        wicket= data['matches'][i]['bat_team']['innings'][0]['wkts']
        over = data['matches'][i]['bat_team']['innings'][0]['overs']

        currentStatus = ' | ' + score + '/' + wicket + ' ( ' + over + ' )'
    except:
        print("hello")

    status = data['matches'][i]['bowler'][0]['name'] + ' To '

    if data['matches'][i]['batsman'][0]['strike'] == '1':
        status = status + (data['matches'][i]['batsman'][0]['name'])
    else:
        status = status + data['matches'][i]['batsman'][1]['name']

    # print(status)
    #Getting Batsman and Bowler Details

    try:
        batman1 = data['matches'][i]['batsman'][0]['name'] + ' * -> | r: ' + data['matches'][i]['batsman'][0]['r'] + ' | b:' + data['matches'][i]['batsman'][0]['b'] + ' | 4s:' + data['matches'][i]['batsman'][0]['4s'] + ' | 6s:' + data['matches'][i]['batsman'][0]['6s']
        batman2 = data['matches'][i]['batsman'][1]['name'] + ' -> | r: ' + data['matches'][i]['batsman'][1]['r'] + ' | b:' + data['matches'][i]['batsman'][1]['b'] + ' | 4s:' + data['matches'][i]['batsman'][1]['4s'] + ' | 6s:' + data['matches'][i]['batsman'][1]['6s']
        bowler = data['matches'][i]['bowler'][0]['name'] + ' -> | o: ' + data['matches'][i]['bowler'][0]['o'] + ' -> | r: ' + data['matches'][i]['bowler'][0]['r'] + ' -> | w: ' + data['matches'][i]['bowler'][0]['w']
        currentScore = status + " " +  currentStatus + '\n' + batman1 + '\n' + batman2 +  '\n' + bowler
    except:
        currentScore='No Detail'

    # print(batman1)
    # print(batman2)

    #combining all the details
    
    if currentScore != lastScore:
        lastScore = currentScore
        return lastScore
    else:
        return currentScore

    #Checking who has won the match and returning the result else return current position


#Driver Function

if __name__ == "__main__":
    while(True):
        Data = getUrl()
        crnt=getData(Data)
        sys_notify(title,crnt)
        time.sleep(60)
