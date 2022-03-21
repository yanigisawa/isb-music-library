import json

def main():
    with open('library_export.txt') as f:
        headers = f.readline().strip().split('\t')
        music_records = []
        for line in f:
            data = line.strip().split('\t')
            record = dict(zip(headers, data))
            music_records.append(record)
    scores = {
        "scores": music_records
    }
    with open('isb_music_library.js', 'w') as f:
        f.write("const isb_library =")
        json.dump(scores, f, indent=2)

if __name__ == "__main__":
    main()