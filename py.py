import requests, zipfile, io
from pathlib import Path

# looks something like this "D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels\"
customLevelPath = "D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels\"

headers = {
    'authority': 'beatsaver.com',
    'sec-ch-ua': '^\\^Google',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://beatsaver.com/browse/rating',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cookie': '__cfduid=da26c6b84036f95c844c426ca478fd5011615003665',
    'if-none-match': 'W/^\\^8c43-iI98SlXuPW+hx69o7E4IpAxPseI^\\^',
}

params = (
    ('automapper', '1'),
)

for i in range(41):
    r = requests.get(f"https://beatsaver.com/api/maps/rating/{i}", headers=headers, params=params).json()["docs"]
    for s in r:
        key = s["key"]
        songName = s["metadata"]["songName"]
        author = s["metadata"]["levelAuthorName"]
        fileName = f"{key} ({songName} - {author})"
        my_file = Path(f"{customLevelPath}{fileName}")
        try:
            if not my_file.exists():
                print(f"downloading {fileName}")
                download = requests.get("https://beatsaver.com" + s["directDownload"], headers=headers)
                z = zipfile.ZipFile(io.BytesIO(download.content))
                z.extractall(f"{customLevelPath}{fileName}")
            else:
                print(f"already have {fileName} downloaded")
        except:
            print("error so skipping")
