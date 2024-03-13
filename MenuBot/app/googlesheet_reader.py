import os

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = os.path.join('E:', '\\PycharmProjects', 'discoBot', 'MenuBot', 'app',
                                'restourant-bot-1e319b5a9fd8.json')  # Имя файла с закрытым ключом, вы должны подставить свое

spreadsheetId = "1hw9jCwa3D-d4d3eGd1bN4LFz-svTfSAo3ZiyTwI42dE"

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])


def get_menu():
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    resp = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range="A1:C999").execute()
    vals = list(resp.values())[2]
    return vals


if __name__ == "__main__":
    vals = get_menu()
    print(vals)
