import pandas as pd

def format_data(data):
    # replace all boolean values to small letters
    data = data.replace({True: 'true', False: 'false'})
    
    return data


def main():
    users = pd.read_csv('users.csv')
    users = format_data(users)
    users.to_csv('users.csv')

    repos = pd.read_csv('repositories.csv')
    repos = format_data(repos)
    repos.to_csv('repositories.csv')


if __name__ == '__main__':
    main()

