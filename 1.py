from collections import Counter, defaultdict
import pandas as pd
import json

df = pd.read_csv('final/user_data.csv')


# Question 1:
# print("Top 5 Singaporeans with the highest number of followers")

top_singaporeans = df.sort_values('followers', ascending=False).head(10).loc[:, ['login', 'followers']]


# print(",".join(top_singaporeans['login'].values[:5]))

# yyx990803,halfrost,DIYgod,yangshun,bytedance

# Question 2:
#   Who are the 5 earliest registered GitHub users in Singapore?
#   List their login in ascending order of created_at, comma-separated.

# earliest_singaporeans = df.sort_values('created_at').head(5).loc[:, ['login', 'created_at']]
# print(",".join(earliest_singaporeans['login'].values))

# chuyeow,choonkeat,winston,cheeaun,nowa

# Question 3:

# repo_df = pd.read_csv('final/repositories.csv')

# repo_df = repo_df.dropna(subset=['license_name'])
# license_counts = repo_df['license_name'].value_counts()

# top_licenses = license_counts.head(3).index.tolist()

# print(",".join(top_licenses))

# mit,apache-2.0,other

# Question 4:
# Which company do the majority of these developers work at?

# df_4 = df.dropna(subset=['company'])

# company_counts = df_4['company'].value_counts()

# top_company = company_counts.idxmax()

# print(top_company)

# NATIONAL UNIVERSITY OF SINGAPORE

# Question 5:
# Which programming language is most popular among these users?


# language_counts = {}

# # Iterate over each user
# for user in df['login']:
#     # Load the user's repositories from the JSON file
#     try:
#         with open(f'repos/{user}.json', 'r') as f:
#             repos = json.load(f)
#             for repo in repos:
#                 language = repo.get('language')
#                 if language:
#                     if language in language_counts:
#                         language_counts[language] += 1
#                     else:
#                         language_counts[language] = 1
#     except FileNotFoundError:
#         print(f"Repos file for user {user} not found.")
#         continue

# most_popular_language = max(language_counts, key=language_counts.get)

# print(most_popular_language)

# JavaScript

# Question 6:
# Which programming language is the second most popular among users who joined after 2020?


# Filter users who joined after 2020
# df['created_at'] = pd.to_datetime(df['created_at'])
# filtered_users = df[df['created_at'] > '2020-01-01']

# # Initialize a dictionary to count languages
# language_counts = {}

# # Iterate over each filtered user
# for user in filtered_users['login']:
#     # Load the user's repositories from the JSON file
#     try:
#         with open(f'repos/{user}.json', 'r') as f:
#             repos = json.load(f)
#             for repo in repos:
#                 language = repo.get('language')
#                 if language:
#                     if language in language_counts:
#                         language_counts[language] += 1
#                     else:
#                         language_counts[language] = 1
#     except FileNotFoundError:
#         print(f"Repos file for user {user} not found.")
#         continue

# # Find the second most popular language
# sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
# second_most_popular_language = sorted_languages[1][0] if len(sorted_languages) > 1 else None

# print(second_most_popular_language)

# Rust

# Question 7:
# Which language has the highest average number of stars per repository?

# language_stars = defaultdict(int)
# language_repos = defaultdict(int)

# # Iterate over each user
# for user in df['login']:
#     # Load the user's repositories from the JSON file
#     try:
#         with open(f'repos/{user}.json', 'r') as f:
#             repos = json.load(f)
#             for repo in repos:
#                 language = repo.get('language')
#                 stars = repo.get('stargazers_count', 0)
#                 if language:
#                     language_stars[language] += stars
#                     language_repos[language] += 1
#     except FileNotFoundError:
#         print(f"Repos file for user {user} not found.")
#         continue

# # Calculate the average stars for each language
# average_stars = {language: language_stars[language] / language_repos[language] for language in language_stars}

# # Find the language with the highest average stars
# most_popular_language = max(average_stars, key=average_stars.get)

# print(most_popular_language)

# MDX

# Question 8:
# Let's define leader_strength as followers / (1 + following). Who are the top 5 in terms of leader_strength? List their login in order, comma-separated.
# df_8 = df.copy()
# df_8['leader_strength'] = df['followers'] / (1 + df['following'])

# # Sort users by leader_strength in descending order and get the top 5
# top_leaders = df_8.sort_values('leader_strength', ascending=False).head(5)

# # Get the login names of the top 5 leaders
# top_leader_logins = top_leaders['login'].values

# # Print the login names, comma-separated
# print(",".join(top_leader_logins))

# bytedance,Jinjiang,cloudflare,JamesNK,Shib-Chain


# Question 9:
# What is the correlation between the number of followers and the number of public repositories among users in Singapore?

# correlation = df['followers'].corr(df['public_repos'])

# print(f"The correlation between the number of followers and the number of public repositories is: {correlation}")

# 0.04540515165800105


# Question 10:
# Does creating more repos help users get more followers? Using regression, estimate how many additional followers a user gets per additional public repository.
# Regression slope of followers on repos

# import statsmodels.api as sm

# X = df['public_repos']
# y = df['followers']

# # Add a constant to the independent variable (intercept)
# X = sm.add_constant(X)

# # Perform the regression
# model = sm.OLS(y, X).fit()

# # Get the regression results
# slope = model.params['public_repos']
# intercept = model.params['const']
# summary = model.summary()

# print(f"Regression slope: {slope}")
# print(f"Regression intercept: {intercept}")
# print(summary)

# Regression slope: 1.4128363052223114


# Question 11:
# Do people typically enable projects and wikis together? What is the correlation between a repo having projects enabled and having wiki enabled?
# Correlation between projects and wiki enabled

# repo_df = pd.read_csv('final/repositories.csv')

# # Calculate the correlation between has_projects and has_wiki
# correlation = repo_df['has_projects'].corr(repo_df['has_wiki'])

# print(f"The correlation between having projects enabled and having wiki enabled is: {correlation}")

# 0.2993893259478533

# Question 12:
# . Do hireable users follow more people than those who are not hireable?
# Average of following per user for hireable=true minus the average following for the rest 


# Calculate the average number of people followed by hireable users
# hireable_users = df[df['hireable'] == True]
# non_hireable_users = df[df['hireable'] == False]

# average_following_hireable = hireable_users['following'].mean()
# average_following_non_hireable = non_hireable_users['following'].mean()

# # Calculate the difference
# difference = average_following_hireable - average_following_non_hireable

# print(f"Average following for hireable users: {average_following_hireable}")
# print(f"Average following for non-hireable users: {average_following_non_hireable}")
# print(f"Difference: {difference}")



# Question 13:
# Some developers write long bios. Does that help them get more followers? What's the impact of the length of their bio (in Unicode words, split by whitespace) with followers? (Ignore people without bios)
# Regression slope of followers on bio word count

# import statsmodels.api as sm
# df_13 = df.dropna(subset=['bio'])

# # Calculate the word count of the bio
# df_13['bio_word_count'] = df_13['bio'].apply(lambda x: len(str(x).split()))

# # Prepare the data for regression
# X = df_13['bio_word_count']
# y = df_13['followers']

# # Add a constant to the independent variable (intercept)
# X = sm.add_constant(X)

# # Perform the regression
# model = sm.OLS(y, X).fit()

# # Get the regression results
# slope = model.params['bio_word_count']
# intercept = model.params['const']
# summary = model.summary()

# print(f"Regression slope: {slope}")
# print(f"Regression intercept: {intercept}")
# print(summary)

# 36.52082

# Question 14:
# Who created the most repositories on weekends (UTC)? List the top 5 users' login in order, comma-separated

# from datetime import datetime


# # Initialize a dictionary to count repositories created on weekends for each user
# weekend_repo_counts = defaultdict(int)

# # Iterate over each user
# for user in df['login']:
#     # Load the user's repositories from the JSON file
#     try:
#         with open(f'repos/{user}.json', 'r') as f:
#             repos = json.load(f)
#             for repo in repos:
#                 created_at = repo.get('created_at')
#                 if created_at:
#                     created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
#                     if created_at_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
#                         weekend_repo_counts[user] += 1
#     except FileNotFoundError:
#         print(f"Repos file for user {user} not found.")
#         continue

# # Sort users by the number of repositories created on weekends in descending order
# sorted_users = sorted(weekend_repo_counts.items(), key=lambda x: x[1], reverse=True)

# # Get the top 5 users
# top_5_users = [user for user, count in sorted_users[:5]]

# # Print the top 5 users' login names, comma-separated
# print(",".join(top_5_users))

# alextanhongpin,shantanu561993,SOF3,KennyDizi,vdt


# Question 15:
# Do people who are hireable share their email addresses more often?
# [fraction of users with email when hireable=true] minus [fraction of users with email for the rest]


# # Calculate the fraction of users with email addresses for hireable users
# hireable_users = df[df['hireable'] == True]
# non_hireable_users = df[df['hireable'] == False]

# fraction_with_email_hireable = hireable_users['email'].notna().mean()
# fraction_with_email_non_hireable = non_hireable_users['email'].notna().mean()

# # Calculate the difference
# difference = fraction_with_email_hireable - fraction_with_email_non_hireable

# print(f"Fraction of hireable users with email: {fraction_with_email_hireable}")
# print(f"Fraction of non-hireable users with email: {fraction_with_email_non_hireable}")
# print(f"Difference: {difference}")


# Question 16:

# Let's assume that the last word in a user's name is their surname (ignore missing names, trim and split by whitespace.) What's the most common surname? (If there's a tie, list them all, comma-separated, alphabetically)
# Most common surname(s)

# df = df.dropna(subset=['name'])

# surnames = df['name'].apply(lambda x: x.strip().split()[-1])

# surname_counts = Counter(surnames)

# max_count = max(surname_counts.values())

# most_common_surnames = [surname for surname, count in surname_counts.items() if count == max_count]

# most_common_surnames.sort()

# print(",".join(most_common_surnames))

# Wang