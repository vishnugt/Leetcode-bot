import requests
import json
import time


headers = {
    'authority': 'leetcode.com',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://leetcode.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9',
}


def getUserSubmissions(user):
    data = '{"operationName":"getRecentSubmissionList","variables":{"username":' + f'"{user}"' + '},"query":"query getRecentSubmissionList($username: String!, $limit: Int) {\\n  recentSubmissionList(username: $username, limit: $limit) {\\n    title\\n    titleSlug\\n    timestamp\\n    statusDisplay\\n    lang\\n  }\\n  languageList {\\n    id\\n    name\\n    verboseName\\n }\\n}\\n"}'
    response = requests.post('https://leetcode.com/graphql', headers=headers, data=data)
    submissions = json.loads(response.content)['data']['recentSubmissionList']
    for submission in submissions:
        if submission["statusDisplay"] == "Accepted":
            continue
        titleSlug = submission["titleSlug"]
        title = submission["title"]
        timestamp = submission["timestamp"]
        print(titleSlug, title)