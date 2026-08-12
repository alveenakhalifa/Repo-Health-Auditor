import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"
EXA_API_KEY = os.getenv("EXA_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {}

if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def extract_repo(repo_url):
    """
    Converts:
    https://github.com/owner/repo
    into:
    owner, repo
    """
    repo_url = repo_url.rstrip("/")
    parts = repo_url.split("/")

    if len(parts) < 5:
        raise ValueError("Invalid GitHub Repository URL")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def get_repo_metadata(repo_url):
    owner, repo = extract_repo(repo_url)

    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("watchers_count"),
        "open_issues": data.get("open_issues_count"),
        "language": data.get("language"),
        "license": data.get("license", {}).get("name") if data.get("license") else "None",
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "default_branch": data.get("default_branch")
    }


def get_recent_issues(repo_url, limit=10):
    owner, repo = extract_repo(repo_url)

    url = f"{GITHUB_API}/repos/{owner}/{repo}/issues"

    response = requests.get(
        url,
        headers=headers,
        params={"state": "open", "per_page": limit}
    )

    if response.status_code != 200:
        return []

    issues = []

    for issue in response.json():

        if "pull_request" in issue:
            continue

        issues.append({
            "title": issue["title"],
            "state": issue["state"],
            "comments": issue["comments"],
            "created_at": issue["created_at"],
            "url": issue["html_url"]
        })

    return issues


def get_contributors(repo_url):
    owner, repo = extract_repo(repo_url)

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contributors"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    contributors = []

    for user in response.json():

        contributors.append({
            "login": user["login"],
            "contributions": user["contributions"]
        })

    return contributors


def search_community(repo_url):
    """
    Placeholder for Exa search.
    Replace with Exa API call if desired.
    """

    return {
        "summary": "Community search not implemented.",
        "mentions": []
    }


def save_report(report, filename="task_outputs/health_report.md"):
    os.makedirs("task_outputs", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    return filename