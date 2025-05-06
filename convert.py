import os
import shutil
import json
import requests
import time
import csv
from collections import defaultdict

keys_to_delete = """Date Purchased
Purchased From
Performance Info
Last Performance Date
Comments
Barcode Number
"""


def get_scores_from_file():
    music_records = []
    keys = keys_to_delete.strip().split("\n")
    file_path = '/Users/jalexander/Downloads/musiclibrary (12).csv'
    with open(file_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            del row['']
            for key in keys:
                if key in row:
                    del row[key]

            music_records.append(row)
        # music_records = []
        # for line in f:
        #     data = line.strip().split('\t')
        #     record = dict(zip(headers, data))
        #     music_records.append(record)
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
    # request_export = "https://secure-prod.mymusicoffice.com/db/musiclibrarydownloadajaxinsert.php?titlecheck=yes&composercheck=yes&arrangercheck=yes&publishercheck=yes&copiescheck=yes&costcheck=yes&gradelevelcheck=yes&statelistcheck=yes&medialinkcheck=yes&medialink2check=yes&musictypecheck=yes&voicingcheck=yes&libraryidcheck=yes&datepurchasedcheck=yes&purchasedfromcheck=yes&performanceinfocheck=yes&lastperformancecheck=yes&commentscheck=yes"
    download_url = "https://secure-prod.mymusicoffice.com/db/musiclibrarydownload.php"
    data_export_url = "https://secure-prod.mymusicoffice.com/db/exports/bzmanagermusiclibraryexport.txt"

    download_payload = {
        "titlecheck": True,
        "composercheck": True,
        "arrangercheck": True,
        "publishercheck": True,
        "copiescheck": True,
        "costcheck": True,
        "gradelevelcheck": True,
        "statelistcheck": True,
        "medialinkcheck": True,
        "medialink2check": True,
        "musictypecheck": True,
        "voicingcheck": True,
        "libraryidcheck": True,
        "button": "Click Here to Download CSV File",
    }

    login_payload = {
        "familyusername": os.environ["USER_NAME"],
        "familypass": os.environ["PASSWORD"]
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "secure-prod.mymusicoffice.com",
        "Origin": "https://secure-prod.mymusicoffice.com",
        "Referer": "https://secure-prod.mymusicoffice.com/db/musiclibrarydownload.php",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": '?0',
        "Sec-Ch-Ua-Platform": "macOS",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }
    with requests.Session() as session:
        session.headers.update(headers)
        post = session.post(login_url, data=login_payload)
        print("Login Response", post.status_code)
        session.get("https://secure-prod.mymusicoffice.com/db/musiclibrarydownload.php")
        r = session.post(download_url, timeout=30, data=download_payload)
        print("Export Request Response", r.status_code, json.dumps(dict(r.headers), sort_keys=True, indent=2))
        # breakpoint()
        # print("Request Headers", json.dumps(dict(r.request.headers), indent=2, sort_keys=True))

        # with open('test.html', 'w') as out_file:
        #     out_file.write(r.text)
        # print("sleeping for 2 seconds")
        # time.sleep(2)
        # export_resp = session.get(data_export_url, stream=True)
        # # print("Export Response", export_resp.status_code)
        # with open('library_export.txt', 'wb') as out_file:
        #     shutil.copyfileobj(export_resp.raw, out_file)
        # print(export_resp.status_code, export_resp.text)


def find_max_per_letter():
    data = get_scores_from_file()
    scores = data['scores']
    library_ids = [score['Library ID'] for score in scores]
    library_letters = set([score['Library ID'].split("-")[0] for score in scores])

    max_ids = defaultdict(int)
    # for l in sorted(library_letters):
    for l_id in library_ids:
        letter, num = l_id.split("-")
        num = int(num)
        if num > max_ids[letter]:
            # print(f"setting num {letter} to {num}")
            max_ids[letter] = num

    print(max_ids)


def find_gaps():
    data = get_scores_from_file()
    scores = data['scores']
    library_ids = [score['Library ID'] for score in scores]
    library_letters = set([score['Library ID'].split("-")[0] for score in scores])

    gaps = []

    for l in sorted(library_letters):
        for i in range(1, 999):
            expected = f"{l}-{i}"
            if expected not in library_ids:
                print(expected)
    print(gaps)


def get_score_by_id(library_id):
    data = get_scores_from_file()
    scores = data['scores']
    found_scores = [
        score
        for score in scores
        if score['Library ID'] == library_id
    ]
    return found_scores


def find_duplicates():

    data = get_scores_from_file()
    scores = data['scores']
    titles = [score['Library ID'] for score in scores]
    duplicates = set([x for x in titles if titles.count(x) > 1])
    with open("duplicates.csv", "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=scores[0].keys())
        csv_writer.writeheader()
        for duplicate in duplicates:
            found_scores = get_score_by_id(duplicate)
            csv_writer.writerows(found_scores)
        # for duplicate in duplicates:
        #     found_scores = get_score_by_id(duplicate)
        #     s = "\n".join(
        #         [
        #             f"{score['Library ID']} - {score['Title']} - {score['Composer']} - {score['Arranger']}"
        #             for score in found_scores
        #         ])
        #     print(s)
    # print(duplicates)


if __name__ == "__main__":

    # find_duplicates()
    # find_gaps()
    # find_max_per_letter()

    # parse_csv_to_json()

    # print("Script DOES NOT automatically download from MyMusicOffice. The CSV download has not be automated yet. An attempt is made in the get_library_from_my_music_office function.")

    get_scores_from_file()
    update_json_music_library()
    # get_library_from_my_music_office()
    # get_bulk_youtube_searches()
