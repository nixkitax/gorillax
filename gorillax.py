import requests
import csv
from datetime import datetime, timedelta
import time
import json
import os

def get_channel_viewers(client_id, token, channel_name):
    url = f"https://api.twitch.tv/helix/streams?user_login={channel_name}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            viewers = data["data"][0]["viewer_count"]
            return viewers
        else:
            return 0
    else:
        raise Exception(f"Failed to retrieve channel viewers. Error: {response.text}")
    
def clear_terminal():
    # Check the operating system
    if os.name == 'posix':  # For Unix/Linux/Mac OS
        os.system('clear')
    elif os.name == 'nt':  # For    Windows
        os.system('cls')

def loadingscreen():
    clear_terminal()
    logo()
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap.")
    time.sleep(0.3)
    clear_terminal()
    logo()
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap..")
    time.sleep(0.3)
    clear_terminal()
    logo()
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap...")
    time.sleep(0.3)


def obtainPath(channel_name):
    # Ottieni il percorso assoluto della cartella corrente
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))

    # Crea il percorso completo per la cartella csv
    percorso_csv = os.path.join(cartella_corrente, 'csv')
        
    if not os.path.exists(percorso_csv):
        os.makedirs(percorso_csv)

    # Crea il percorso completo per il file CSV
    nome_file = channel_name + ".csv"
    percorso_file_csv = os.path.join(percorso_csv, nome_file)
    
    return str(percorso_file_csv)

def countdown(seconds):
    while seconds > 0:
        clear_terminal()
        logo()
        print(f"Countdown: {seconds // 3600:02d}:{(seconds // 60) % 60:02d}:{seconds % 60:02d}")
        time.sleep(1)  # Pause for 1 second
        seconds -= 1
    print("Countdown complete!")

    

def signViews():
    
    clear_terminal()
    logo()
    # Esempio di utilizzo
    client_id = "0t9es7292m951nq659ahaz80yv2qsc"
    channel_name = input("Inserisci uno streamer che ti piace de: ")
    with open('config.json') as f:
        config = json.load(f)
    token = config['api_token'] 
    path = obtainPath(channel_name)
    clear_terminal()
    logo()
    print("Opening " + path + ".")
    time.sleep(1)
    clear_terminal()
    logo()
    print("Opening " + path + "..")
    time.sleep(1)
    clear_terminal()
    logo()
    print("Opening " + path + "...")
    time.sleep(1)

    while True:
        now = datetime.now()
        viewers = get_channel_viewers(client_id, token, channel_name)
        
        if viewers == 0:
            print(channel_name, " could be offline.. :()")
            countdown(3600)
            
            
        if now.minute % 2 == 0 and now.second == 0 and viewers > 0:
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            new_data = (timestamp, viewers)

            with open(path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_data)
                clear_terminal()
                logo()
                print("Printed in csv:", new_data, "-", channel_name)
                time.sleep(10)
        else:
            loadingscreen()

def logo():
    print("                  _ _ _            ")
    print("  __ _  ___  _ __(_) | | __ ___  __")
    print(" / _` |/ _ \| '__| | | |/ _` \ \/ /")
    print("| (_| | (_) | |  | | | | (_| |>  < ")
    print(" \__, |\___/|_|  |_|_|_|\__,_/_/\_\ ")
    print(" |___/                              ")
    print(" ")
        
def startup():
    clear_terminal()
    print("                  _ _ _            ")
    time.sleep(0.5)
    print("  __ _  ___  _ __(_) | | __ ___  __")
    time.sleep(0.5)
    print(" / _` |/ _ \| '__| | | |/ _` \ \/ /")
    time.sleep(0.5)
    print("| (_| | (_) | |  | | | | (_| |>  < ")
    time.sleep(0.5)
    print(" \__, |\___/|_|  |_|_|_|\__,_/_/\_\ ")
    time.sleep(0.5)
    print(" |___/                              ")
    time.sleep(0.5)
    print(" ")
    time.sleep(2)
    print("1. Save in a csv timestamp-viewers of a streamer;")
    print("2. View statistics of a streamer (graphic viewers)")
    print("3. Try to insert in a regression line one csv")

def showGraphic():
    print("not implemented yet...")
    
def main():
    startup()
    term = input()
    match term: 
        case "1": 
            signViews()
        case "2":
            showGraphic()
        case _:
            print("if you cannot understand this menu you are probably a gorillax")
    
        
if __name__ == "__main__":
    try:
        main()
        clear_terminal()
    except KeyboardInterrupt:
        print("You typed CTRL + C, which is the keyboard interrupt exception")