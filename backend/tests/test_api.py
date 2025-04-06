import requests

API_URL = "http://localhost:8000/separate-audio"

def test_separate_audio(audio_path: str, query: str):
    with open(audio_path, "rb") as f:
        files = {
            "audio_file": (audio_path, f, "audio/wav"),

        }
        data = {
            "text_query": query
        }

        resp = requests.post(API_URL, files=files, data=data)
    
    if resp.status_code != 200:
        print(f"Error {resp.status_code}: {resp.text}")
        return

    result = resp.json()
    print("Response JSON:", result)

    download_url = "http://localhost:8000/download-processed/"
    params = {"path": result["file_path"]}
    dl = requests.get(download_url, params=params)
    if dl.status_code == 200:
        out_path = "downloaded_processed.wav"
        with open(out_path, "wb") as out_f:
            out_f.write(dl.content)
        print(f"Processed file saved to {out_path}")
    else:
        print(f"Download error {dl.status_code}: {dl.text}")

if __name__ == "__main__":
    test_separate_audio("noisy_speech.wav", "speech")
