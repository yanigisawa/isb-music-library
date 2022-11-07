import os
import shutil
import json
import requests
import time

def get_scores_from_file():
    with open('library_export.txt') as f:
        headers = f.readline().strip().split('\t')
        music_records = []
        for line in f:
            data = line.strip().split('\t')
            record = dict(zip(headers, data))
            music_records.append(record)
    return {
        "scores": music_records
    }

def update_json_music_library():
    scores = get_scores_from_file()
    with open('isb_music_library.js', 'w') as f:
        f.write("const isb_library =")
        json.dump(scores, f, indent=2)


def get_bulk_youtube_searches():
    scores = get_scores_from_file()
    for score in scores['scores']:
        print(f"{score['Title']} - {score['Composer']} - {score['Arranger']}")


def get_library_from_my_music_office():
    # Family login:
    # https://secure-prod.mymusicoffice.com/db/familylogin.php
    # family user name field: familyusername
    # Password field: familypass
    # URL to Post to create .txt file:
    # POST to https://secure-prod.mymusicoffice.com/db/musiclibrarydownloadajaxinsert.php?titlecheck=yes&composercheck=yes&arrangercheck=yes&publishercheck=yes&copiescheck=yes&costcheck=yes&gradelevelcheck=yes&statelistcheck=yes&medialinkcheck=yes&medialink2check=yes&musictypecheck=yes&voicingcheck=yes&libraryidcheck=yes&datepurchasedcheck=yes&purchasedfromcheck=yes&performanceinfocheck=yes&lastperformancecheck=yes&commentscheck=yes
    # Resulting text file at URL:
    # GET: https://secure-prod.mymusicoffice.com/exports/bzmanagermusiclibraryexport.txt
    login_url = "https://secure-prod.mymusicoffice.com/db/familylogin.php"
    request_export = "https://secure-prod.mymusicoffice.com/db/musiclibrarydownloadajaxinsert.php?titlecheck=yes&composercheck=yes&arrangercheck=yes&publishercheck=yes&copiescheck=yes&costcheck=yes&gradelevelcheck=yes&statelistcheck=yes&medialinkcheck=yes&medialink2check=yes&musictypecheck=yes&voicingcheck=yes&libraryidcheck=yes&datepurchasedcheck=yes&purchasedfromcheck=yes&performanceinfocheck=yes&lastperformancecheck=yes&commentscheck=yes"
    data_export_url = "https://secure-prod.mymusicoffice.com/db/exports/bzmanagermusiclibraryexport.txt"
    payload = {
        "familyusername": os.environ["USER_NAME"],
        "familypass": os.environ["PASSWORD"]
    }
    with requests.Session() as session:
        post = session.post(login_url, data=payload)
        print("Login Response", post.status_code)
        r = session.post(request_export)
        print("Export Request Response", r.status_code, r.text)
        print("sleeping for 2 seconds")
        time.sleep(2)
        export_resp = session.get(data_export_url, stream=True)
        # print("Export Response", export_resp.status_code)
        with open('library_export.txt', 'wb') as out_file:
            shutil.copyfileobj(export_resp.raw, out_file)
        # print(export_resp.status_code, export_resp.text)


if __name__ == "__main__":
    get_library_from_my_music_office()
    update_json_music_library()
    # get_bulk_youtube_searches()