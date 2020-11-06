'''
    Find out the current latest release, and updates at the users requests.
'''


import requests, zipfile, io
import json
import os, shutil
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory

BOT_FOLDER_PREFIX = 'MyBot-'

release_url = 'https://api.github.com/repos/MyBotRun/MyBot/releases/latest'
release = json.loads(requests.get(url=release_url).text)
#print(release['tag_name'])
#print(release['assets'][0]['browser_download_url'])
#print(json.dumps(release, indent=2))
#exit()

root = tk.Tk()
root.withdraw() # hide the background window

userChoice = tk.messagebox.askquestion(message = 'Latest Version of MyBot is ' + release['tag_name'] + '\n' + 'Would you like to update your bot?')
if userChoice != 'yes': # exit if no need to update
    exit()
    
# get users my bot folder
path = askdirectory(title='Select Folder') # shows dialog box and return the path
if not((BOT_FOLDER_PREFIX + 'MBR_') in path.split('/')[-1]): # check to see if we are looking at an existing bot directory
    tk.messagebox.showinfo(message="Folder not an existing bot folder.")
    exit()
#print(path.split('/')[-1])  

# make copies of the CSV folder and the profiles folder
csvFolder = os.path.join(path, 'CSV/')
profilesFolder = os.path.join(path, 'Profiles/')
shutil.copytree(csvFolder, os.path.join(os.path.split(path)[0], 'CSV/')) if not(os.path.exists(os.path.join(os.path.split(path)[0], 'CSV/'))) else None # copy backwards one directory
shutil.copytree(profilesFolder, os.path.join(os.path.split(path)[0], 'Profiles/')) if os.path.exists(profilesFolder) and not(os.path.exists(os.path.join(os.path.split(path)[0], 'Profiles/'))) else None

shutil.rmtree(path) # delete old bot

# download and unzip bot
latestBotReq = requests.get(release['assets'][0]['browser_download_url']) # download bot
latestBotZip = zipfile.ZipFile(io.BytesIO(latestBotReq.content)) # convert to zip file
latestBotZip.extractall(os.path.join(os.path.split(path)[0], BOT_FOLDER_PREFIX + release['tag_name'])) # extract zip

# move profiles and CSV copies into new bot
shutil.move(os.path.join(os.path.split(path)[0], 'CSV/'), os.path.join(os.path.join(os.path.split(path)[0], BOT_FOLDER_PREFIX + release['tag_name']), 'CSV/'))
shutil.move(os.path.join(os.path.split(path)[0], 'Profiles/'), os.path.join(os.path.join(os.path.split(path)[0], BOT_FOLDER_PREFIX + release['tag_name']), 'Profiles/'))

tk.messagebox.showinfo(message="Bot Updated!")