import os
import json
import httpx
import dotenv
import pandas as pd
from tqdm import tqdm

dotenv.load_dotenv()

def generate_user_names(user_data_csv_file='final/user_data.csv'):
    
    user_data = pd.read_csv(user_data_csv_file)
    filename = 'user_names.txt'
    with open(filename, 'w') as f:
        for user in user_data['login']:
            f.write(user + '\n')
    print(f"User names written to {filename}")
    return filename

user_names_file = generate_user_names()

def get_user_repos(user_id):
    folder = 'repos'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f'{user_id}.json')

    repos_per_page = 100
    page = 1
    all_repos = []
    max_repos = 500
    while len(all_repos) < max_repos:
        response = httpx.get(f'https://api.github.com/users/{user_id}/repos',
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Sameer Singh',
                'Authorization': 'Bearer ' + os.getenv('GITHUB_ACCESS_TOKEN'),
                "X-Github-Api-Version": "2022-11-28"},
            params={
                'per_page': repos_per_page,
                'sort': 'pushed',
                'direction': 'desc',
                'page': page},
            timeout=30)
    
        if response.status_code != 200:
            print(f"Error fetching user repos: {response.status_code}")
            return None
        
        data = response.json()
        if len(data) < repos_per_page:
            break
        page += 1

        all_repos.extend(data)

    with open(filename, 'w') as f:
        json.dump(all_repos, f, indent=2)
    return all_repos


repo_archive = []

for user in open(user_names_file):
    user = user.strip()
    print(f"Fetching repos for user: {user}")
    repos = get_user_repos(user)
    if repos:
        filtered_repos = []
        for repo in tqdm(repos):
            filtered_repos.append({
                'login': user,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'] if repo['language'] else "",
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': repo['license']['key'] if repo['license'] else "",
            })
        repo_archive.extend(filtered_repos)

repos_df = pd.DataFrame(repo_archive)

print("Saving repo data to final/repositories.csv ....")
repos_df.to_csv('final/repositories.csv', index=False)

print("********** Done! **********")
print(f"Total repos fetched: {len(repo_archive)}")

