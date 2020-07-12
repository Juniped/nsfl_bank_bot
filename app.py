from __future__ import print_function
import re, os, time, sys, datetime, json, asyncio
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import discord
from config import Config
token = Config.token
client = discord.Client()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1RYS8I7xCcq-HABK_tiGsaJ5saq6KNkhFJb53C11XqpU'
SAMPLE_RANGE_NAME = 'Players!A2:D'

@client.event
async def on_ready():
    print("Weapons Online")

def get_data(search_string):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print(values)
    return_value = []
    if not values:
        print('No data found.')
    else:
        print('Username', 'Player Name','Balance')
        for row in values:
            if search_string.lower() in row[0].lower() or search_string.lower() in row[1].lower():
                return_value.append([row[0],row[1],row[2]])
                # Print columns A and E, which correspond to indices 0 and 4.
                try:
                    print('%s, %s, %s' % (row[0],row[1],row[2]))
                except:
                    print('%s, %s' % (row[0],row[2]))
    return return_value

def get_transactions(search_string):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Primary Log!A:I").execute()
    values = result.get('values', [])
    # print(values)
    return_value = []
    if not values:
        print('No data found.')
    else:
        print('Date','Username','Net','Notes')
        for row in values:
            if search_string.lower() in row[1].lower():
                try:
                    return_value.append([row[0],row[1],row[6],row[8]])
                except:
                    try:
                        return_value.append([row[0],row[1],row[6]])
                    except:
                        continue
                # Print columns A and E, which correspond to indices 0 and 4.
                try:
                    print('%s, %s, %s, %s, %s' % (row[0],row[1],row[6],row[8]))
                except:
                    pass
    return return_value

@client.event
async def on_message(message):
    # try:
    if message.author == client.user:
        return
    if message.content.startswith("$"): 
        content = message.content[1:]
        print(content)
        if content.startswith("balance"): # Set Pitcher
            # print(message.author.name)
            m = content[7:]
            m = m.strip()
            if len(m) == 0:
                m = message.author.name
            data = get_data(m)
            print_string = "Username, Player Name, Balance\n"
            for value in data:
            # random_int = random.randint(0,len(lines)-1)
                print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}" + "\n"
            await message.channel.send(f"{print_string}")

        elif content.startswith("help"):
            await message.channel.send("""
            Use `$balance` or`$balance <search string>` to query the bank\n
            Use `$invite` to get an invite link
            """)
        
        elif content.startswith("invite"):
            await message.channel.send("https://discord.com/api/oauth2/authorize?client_id=731136702474747967&permissions=0&scope=bot")

        elif content.startswith("transactions"):
            m = content[12:].strip()
            if len(m) == 0:
                m = message.author.name
            data = get_transactions(m)
            # print(data[-1])
            print_string = "Date, Username, Net Tran, Notes\n"
            for value in data[-10:]:
            # random_int = random.randint(0,len(lines)-1)
                try:
                    print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}, {value[3]}" + "\n"
                except:
                    print_string = print_string + f"{value[0]}, {value[1]}, {value[2]}" + "\n"
            # print(print_string)
            # print(len(print_string))
            await message.channel.send(f"```{print_string}```")
    # except Exception as e:
    #     print(e)

print("Starting Bank Bot")
client.run(token)