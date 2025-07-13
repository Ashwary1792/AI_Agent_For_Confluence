# import os
# import requests
# from requests.auth import HTTPBasicAuth
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup

# load_dotenv()

# CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
# CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
# BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
# PAGE_ID = os.getenv("CONFLUENCE_PAGE_ID")
# TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# def fetch_confluence_content(page_id):
#     url = f"{BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
#     response = requests.get(
#         url,
#         auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN),
#         headers={"Accept": "application/json"}
#     )
#     response.raise_for_status()
#     html_content = response.json()['body']['storage']['value']
#     soup = BeautifulSoup(html_content, "html.parser")
#     return soup.get_text()

# def ask_together_ai(question, context):
#     endpoint = "https://api.together.xyz/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {TOGETHER_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#         "messages": [
#             {"role": "system", "content": f"You are a helpful assistant based on this documentation:\n{context}"},
#             {"role": "user", "content": question}
#         ],
#         "temperature": 0.3,
#         "max_tokens": 300
#     }

#     response = requests.post(endpoint, json=data, headers=headers)
#     response.raise_for_status()
#     return response.json()["choices"][0]["message"]["content"].strip()

# def chat_with_docs(docs):
#     print("Start chatting with Together.ai! Type 'exit' to quit.")
#     while True:
#         question = input("You: ")
#         if question.lower() in ["exit", "quit"]:
#             break
#         try:
#             answer = ask_together_ai(question, docs)
#             print(f"AI: {answer}\n")
#         except Exception as e:
#             print(f"❌ Error getting response: {e}")

# if __name__ == "__main__":
#     try:
#         print("Fetching content from your Confluence page...")
#         docs = fetch_confluence_content(PAGE_ID)
#         print("✅ Content fetched successfully!\n")
#         chat_with_docs(docs)
#     except Exception as e:
#         print("❌ Error:", e)

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")  # e.g. https://yourdomain.atlassian.net/wiki
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


def fetch_all_pages_from_space(space_key):
    all_docs = []
    start = 0
    limit = 50  # max pages per request

    while True:
        url = f"{BASE_URL}/rest/api/content"
        params = {
            "type": "page",
            "spaceKey": space_key,
            "limit": limit,
            "start": start,
            "expand": "body.storage"
        }
        response = requests.get(
            url,
            auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_TOKEN),
            headers={"Accept": "application/json"},
            params=params
        )
        response.raise_for_status()
        data = response.json()
        pages = data.get("results", [])

        if not pages:
            break

        for page in pages:
            title = page.get("title", "No Title")
            html_content = page["body"]["storage"]["value"]
            soup = BeautifulSoup(html_content, "html.parser")
            text_content = soup.get_text(separator="\n", strip=True)
            all_docs.append(f"\n\n## {title}\n{text_content}")

        # Pagination: if there are more pages, increment start offset
        if len(pages) < limit:
            break
        start += limit

    return "\n".join(all_docs)


def ask_together_ai(question, context):
    import json
    endpoint = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant based on this documentation:\n{context}"},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    response = requests.post(endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def chat_with_docs(docs):
    print("Start chatting with Together.ai! Type 'exit' to quit.")
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            break
        try:
            answer = ask_together_ai(question, docs)
            print(f"AI: {answer}\n")
        except Exception as e:
            print(f"❌ Error getting response: {e}")


if __name__ == "__main__":
    try:
        print("Fetching all pages content from your Confluence space...")
        docs = fetch_all_pages_from_space(SPACE_KEY)
        print("✅ Successfully fetched all pages!\n")
        # Optional: print snippet of fetched content
        print(docs[:1000], "\n---\n")
        chat_with_docs(docs)
    except Exception as e:
        print("❌ Error:", e)
