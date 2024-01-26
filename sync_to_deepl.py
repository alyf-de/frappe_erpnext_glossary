from pathlib import Path
import requests
from dotenv import dotenv_values

API_URL = "https://api-free.deepl.com/v2/glossaries"
LANGUAGE_PAIRS = (("en", "de"),)


def main():
    config = dotenv_values(".env")
    api_key = config.get("API_KEY")

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"DeepL-Auth-Key {api_key}",
        }
    )

    delete_existing(session)

    for source_lang, target_lang in LANGUAGE_PAIRS:
        data = Path(f"{source_lang}-{target_lang}.csv").read_text().strip("\n")
        deepl_response = session.post(
            API_URL,
            json={
                "name": "Frappe + ERPNext",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "entries": data,
                "entries_format": "csv",
            },
        )
        print(deepl_response.status_code)
        print(deepl_response.text)


def delete_existing(session: requests.Session) -> None:
    request_list = session.get(API_URL)
    for item in request_list.json().get("glossaries", []):
        if item["name"] == "Frappe + ERPNext":
            glossary_id = item["glossary_id"]
            print(f"Deleting {glossary_id}")
            session.delete(f"{API_URL}/{glossary_id}")


if __name__ == "__main__":
    main()
