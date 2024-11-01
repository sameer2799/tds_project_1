import pandas as pd
import json
import httpx
import os
from dotenv import load_dotenv
from tqdm import tqdm


load_dotenv()

def get_search_results():
    
    if os.path.exists('singapore_users.json'):
        with open('singapore_users.json', 'r') as f:
            content = f.read()
        return json.loads(content)
    else:
        per_page = 100
        page = 1
        all_users = []

        while True:
            response = httpx.get('https://api.github.com/search/users',
                headers={
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'Sameer Singh',
                    'Authorization': 'Bearer ' + os.getenv('GITHUB_ACCESS_TOKEN'),
                    "X-Github-Api-Version": "2022-11-28"},
                params={
                    "q": "location:Singapore followers:>=100",
                    "per_page": per_page,
                    "page": page
                },
                timeout=30)
            
            if response.status_code != 200:
                print(f"Fetch maybe completed or some error occured: {response.status_code}")
                break
            
            data = response.json()
            all_users.extend(data['items'])

            print(f"Page {page} done")

            if len(data['items']) < per_page:
                break
            page += 1

        with open('singapore_users.json', 'w') as f:
            json.dump(all_users, f)
        return all_users

users = get_search_results()

user_ids = [user['id'] for user in users]
with open('user_ids.txt', 'w') as f:
    f.write('\n'.join(map(str, user_ids)))

print("Number of User ids extracted based on search query: ", len(user_ids))


def get_user_data(id):
    folder = 'users'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f'{id}.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        return json.loads(content)
    else:
        response = httpx.get(f'https://api.github.com/user/{id}',
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Sameer Singh',
                'Authorization': 'Bearer ' + os.getenv('GITHUB_ACCESS_TOKEN'),
                "X-Github-Api-Version": "2022-11-28"},
            timeout=30)
        
        if response.status_code != 200:
            print(f"Error fetching user data: {response.status_code}")
            return None
        
        data = response.json()
        with open(filename, 'w') as f:
            json.dump(data, f)
        return data

def get_all_user_data(all_ids):
    user_data = []
    for user_id in tqdm(all_ids):
        data = get_user_data(user_id)
        if data:
            user_data.append(data)
    return user_data

print("Fetching user data...")
raw_user_data = get_all_user_data(user_ids)

print("\nNumber of users fetched: ", len(raw_user_data))

fields_to_extract = ['login', 
                     'name', 
                     'company',
                     'location',
                     'email',
                     'hireable',
                     'bio',
                     'public_repos',
                     'followers',
                     'following',
                     'created_at']

output_folder_name = 'final'

if not os.path.exists(output_folder_name):
    os.makedirs(output_folder_name)

output_file = os.path.join(output_folder_name, 'user_data.csv')

print("Extracting fields...")
user_data = []
for user in raw_user_data:
    filtered_user = {}
    for field in fields_to_extract:
        if field == 'company':
            filtered_user[field] = user.get('company').strip().lstrip('@').upper() if user.get('company') else ''
        else:
            filtered_user[field] = user.get(field, '')
    user_data.append(filtered_user)

print("Creating DataFrame...")
df = pd.DataFrame(user_data, columns=fields_to_extract)

print(f"\nShape of dataframe: {df.shape} \n")


print("Saving to CSV...")
df.to_csv(output_file, index=False)

print("********* user_data.csv saved successfully in final folder ********* \n")

def print_user_data(user_data):
    print(f"Login: {user_data['login']}")
    print(f"Name: {user_data['name'] if user_data['name'] else ''}")
    print(f"Company: {user_data['company'].strip().lstrip('@').upper() if user_data['company'] else ''}")
    print(f"Location: {user_data['location'] if user_data['location'] else ''}")
    print(f"Email: {user_data['email'] if user_data['email'] else ''}")
    print(f"Hireable: {user_data['hireable'] if user_data['hireable'] else ''}")
    print(f"Bio: {user_data['bio'] if user_data['bio'] else ''}")
    print(f"Public Repos: {user_data['public_repos'] if user_data['public_repos'] else ''}")
    print(f"Followers: {user_data['followers'] if user_data['followers'] else ''}")
    print(f"Following: {user_data['following'] if user_data['following'] else ''}")
    print(f"Created At: {user_data['created_at'] if user_data['created_at'] else ''}")

print()
