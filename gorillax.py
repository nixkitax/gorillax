import requests
import csv
from datetime import datetime, timedelta
import time
import json
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt



def logo():
    clear_terminal
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
    time.sleep(0.2)
    print("  __ _  ___  _ __(_) | | __ ___  __")
    time.sleep(0.2)
    print(" / _` |/ _ \| '__| | | |/ _` \ \/ /")
    time.sleep(0.2)
    print("| (_| | (_) | |  | | | | (_| |>  < ")
    time.sleep(0.2)
    print(" \__, |\___/|_|  |_|_|_|\__,_/_/\_\ ")
    time.sleep(0.2)
    print(" |___/                              ")
    time.sleep(0.2)
    print(" ")
    time.sleep(0.2)
    print("1. Save in a csv timestamp-viewers of a streamer;")
    print("2. View statistics of a streamer (graphic viewers)")


def get_key():
    if os.name == 'nt':  # Windows
        import msvcrt
        key = msvcrt.getch()
    else:  # Unix-based systems (Linux, macOS)
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

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

def loadingscreen(channel_name, path):
    clear_terminal()
    logo()
    printStatus(channel_name, path)
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap.")
    time.sleep(0.1)
    clear_terminal()
    logo()
    printStatus(channel_name, path)
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap..")
    time.sleep(0.1)
    clear_terminal()
    logo()
    printStatus(channel_name, path)
    print("[", datetime.now().strftime("%H:%M:%S"), "]: waiting to take a snap...")
    time.sleep(0.1)


def obtainPathCsv(channel_name):
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

def obtainPath():
    # Ottieni il percorso assoluto della cartella corrente
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))

    # Crea il percorso completo per la cartella csv
    percorso_csv = os.path.join(cartella_corrente, 'csv')
        
    if not os.path.exists(percorso_csv):
        os.makedirs(percorso_csv)
    
    return str(percorso_csv)

def countdown(seconds):
    while seconds > 0:
        clear_terminal()
        logo()
        print(f"Countdown: {seconds // 3600:02d}:{(seconds // 60) % 60:02d}:{seconds % 60:02d}")
        time.sleep(1)  # Pause for 1 second
        seconds -= 1
    print("Countdown complete!")
    
def get_last_id_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
        if last_row is not None:
            last_id = int(last_row[0])+1  # Assumendo che l'ID sia nella prima colonna
            return last_id
        else:
            return 1
        
def get_last_timestamp_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
        if last_row is not None:
            last_id = last_row[1]  # Assumendo che l'ID sia nella prima colonna
            return last_id
        else:
            return "NaN "
def get_last_numViewers_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
        if last_row is not None:
            last_id = last_row[2]  # Assumendo che l'ID sia nella prima colonna
            return last_id
        else:
            return "NaN"

def printStatus(channel_name, path):
    print("---------------------------------\n")
    print("Last timestamp taken status of ",channel_name,":\n- ID:        ", get_last_id_from_csv(path), "\n- Timestamp: ", get_last_timestamp_from_csv(path),
              "\n- Viewers:   ", get_last_numViewers_from_csv(path), "\n")
    print("---------------------------------\n")


def signViews():
    clear_terminal()
    logo()
    # Esempio di utilizzo
    client_id = "0t9es7292m951nq659ahaz80yv2qsc"
    channel_name = input("Inserisci uno streamer che ti piace de: ")
    with open('config.json') as f:
        config = json.load(f)
    token = config['api_token'] 
    path = obtainPathCsv(channel_name)
    clear_terminal()
    logo()
    print("- Opening " + path + ".")
    time.sleep(0.5)
    clear_terminal()
    logo()
    print("- Opening " + path + "..")
    time.sleep(0.5)
    clear_terminal()
    logo()
    print("- Opening " + path + "...")
    time.sleep(0.5)
    
    if not os.path.exists(path):
        with open(path, 'w') as file:
            # Puoi anche scrivere del contenuto predefinito nel file se necessario
            pass
        cnt = get_last_id_from_csv(path)   
        print("- new CSV created..")
        time.sleep(0.5)

    else: 
        cnt = get_last_id_from_csv(path)  
        print("- opening indicated CSV..") 
        time.sleep(0.5)


    while True:
        now = datetime.now()
        viewers = get_channel_viewers(client_id, token, channel_name)
        if viewers == 0:
            printStatus(channel_name, path)
            print(channel_name, " could be offline.. :()")
            countdown(3600)
        if now.minute % 10 == 0 and now.second == 0 and viewers > 0:
            with open(path, 'a', newline='') as csvfile:
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                new_data = (cnt, timestamp, viewers)
                cnt = cnt + 1 
                writer = csv.writer(csvfile)
                writer.writerow(new_data)
                clear_terminal()
                logo()
                printStatus(channel_name, path)
                print("Printed in csv:", new_data, "-", channel_name)
                time.sleep(5)
                
        else:
            loadingscreen(channel_name, path)

def showFiles():
    
    clear_terminal()
    logo()

    current_path = os.getcwd()

   # Ottieni la lista dei file CSV nella cartella corrente
    csv_files = [file for file in os.listdir(current_path + "/csv") if file.endswith('.csv')]

    # Mostra la lista dei file CSV disponibili
    print("File CSV disponibili:")
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {file}")

    # Fai selezionare un numero di file all'utente
    selection = input("Seleziona un numero di file: ")


    # Verifica la selezione dell'utente
    if selection.isdigit() and int(selection) <= len(csv_files):
        selected_file = csv_files[int(selection) - 1]
        clear_terminal()
        logo()
        print(f"Hai selezionato: {selected_file}")
        time.sleep(1)
        
        path = current_path + f"/csv/{selected_file}"
        print(path)
        
        df = pd.read_csv(path)
        print(df)
        
        x = df['X'].astype(datetime)
        y = df['Y'].astype(int)
        
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Grafico {selected_file}')
        plt.show()
        
    else:
        clear_terminal()
        logo()
        print("item selected not valid, press a key to back in the menu.")
        get_key()
        main()
        time.sleep(3)

def create_config_file(api_key):
    config = {
        "api_key": api_key
    }
    with open("config.json", "w") as f:
        json.dump(config, f)
    print("Il file 'config.json' è stato creato con successo.")

def get_api_key():
    return input("Inserisci la tua chiave API: ")

def check_config_file():
    if not os.path.exists("config.json"):
        api_key = get_api_key()
        create_config_file(api_key)
    else:
        print("Il file 'config.json' esiste già.")

def main():
    check_config_file()
    startup()
    #logo()
    term = input("Insert a value: ")
    match term: 
        case "1": 
            signViews()
        case "2":
            showFiles()
        case _:
            print("if you cannot understand this menu you are probably a gorillax")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("You typed CTRL + C, which is the keyboard interrupt exception")