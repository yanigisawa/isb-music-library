import os
import uuid

import anvil.server
from anvil.tables import app_tables

anvil.server.connect(os.environ["ANVIL_API_KEY"])

def get_scores_from_file():
    with open('library_export.txt') as f:
        headers = f.readline().lower().replace(" ", "_").strip().split('\t')
        music_records = []
        for line in f:
            data = line.strip().split('\t')
            record = {
                    k:v
                for k,v in
                dict(zip(headers, data)).items()
                if k in [
                "title", "composer", "arranger",
                "library_id", "voicing", "media_link"
                ]
            }
            music_records.append(record)
    return {
        "scores": music_records
    }

def main():
    scores = get_scores_from_file()
    for i, score in enumerate(scores["scores"]):
        # print("Would add ", score)
        if i % 100 == 0:
            print(f"Added {i} scores")
        score["uuid"] = str(uuid.uuid4())
        app_tables.library.add_row(**score)

if __name__ == "__main__":
    main()