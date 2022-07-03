#! /usr/bin/python3
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError as HTTPError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIAL_FILE_PATH = ""
SHARE_DIR_ID = ""
DOC_TYPE={
    "pdf" : "application/pdf",
    "metadata" : "application/vnd.google-apps.script+json",
    "folder" : "application/vnd.google-apps.folder",
    } # mimetype ref https://developers.google.com/drive/api/guides/ref-export-formats

def upload_file(file_path, file_name, dir_name, doc_type):

    # get credentials and service object
    sa_creds = service_account.Credentials.from_service_account_file(CREDENTIAL_FILE_PATH)
    scoped_creds = sa_creds.with_scopes(SCOPES)
    drive_service = build('drive', 'v3', credentials=scoped_creds)

    dir_id = find_dir(dir_name)

    # create dir
    if dir_id is None:
        file_metadata = {
            'name': dir_name,
            'parents': [folder_id],
            "mimeType": DOC_TYPE["folder"],
        }
        media = MediaFileUpload(
            SHARE_DIR_ID,
            mimetype=DOC_TYPE["folder"],
            resumable=True
        )

        response = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        dir_id = responce.get("id")

    # upload file
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        "mimeType": DOC_TYPE[doc_type],
    }
    media = MediaFileUpload(
        file_path,
        mimetype=DOC_TYPE[doc_type],
        resumable=True
    )

    response = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()

    print(response)


def find_dir(dirname):
    # get credentials and service object
    sa_creds = service_account.Credentials.from_service_account_file(CREDENTIAL_FILE_PATH)
    scoped_creds = sa_creds.with_scopes(SCOPES)
    drive_service = build('drive', 'v3', credentials=scoped_creds)

    response = drive_service.files().list(
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        q=f"parents in '{SHARE_FOLDER_ID}' and trashed = false",
        fields="nextPageToken, files(id, name)").execute()

    dir = None
    for dir in response.get('files', []):
        if dir.get('name') == dirname:
            return dir.get("id")
            print(f"Found file: {file.get('name')} ({file.get('id')})")

    return None



