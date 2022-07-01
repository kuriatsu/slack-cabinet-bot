from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError as HTTPError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SHARE_FOLDER_ID = ''

sa_creds = service_account.Credentials.from_service_account_file(
    '')
scoped_creds = sa_creds.with_scopes(SCOPES)
drive_service = build('drive', 'v3', credentials=scoped_creds)


file_metadata = {
    'name': "test",
    'parents': [SHARE_FOLDER_ID],
    "mimeType": 'image/png',
}
media = MediaFileUpload(
    "",
    mimetype='image/png',
    resumable=True
)

response = drive_service.files().create(
    body=file_metadata, media_body=media, fields='id'
).execute()

print(response)

file = None
response = drive_service.files().list(
    supportsAllDrives=True,
    includeItemsFromAllDrives=True,
    q=f"parents in '{SHARE_FOLDER_ID}' and trashed = false",
    fields="nextPageToken, files(id, name)").execute()

for file in response.get('files', []):
    print(f"Found file: {file.get('name')} ({file.get('id')})")
