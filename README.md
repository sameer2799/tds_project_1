# tds_project_1
A Project for TDS

Note: Find the codes in branch: `working`

# Explanation

Environment Setup:

The dotenv library was used to load environment variables, including the GitHub access token, from a .env file.
Fetching User Data:

A list of GitHub users from Singapore was obtained using the GitHub search API with the query location:Singapore followers:>100.
The user data was saved into a CSV file named user_data.csv.
Generating Usernames:

Usernames were extracted from the user_data.csv file and saved into a text file named user_names.txt.
Fetching Repository Data:

For each user, their repositories were fetched using the GitHub API endpoint /users/{user}/repos.
The repositories were saved into individual JSON files in a directory named repos.
Handling Pagination:

The GitHub API responses were paginated, so multiple requests were made to fetch all pages of results.
The httpx library was used to handle HTTP requests and responses.
Data Processing:

The repository data was processed to extract relevant information such as the number of stars, programming languages used, and creation dates.
This data was used to perform various analyses, such as finding the most popular programming languages and the correlation between different attributes.

# Fact

After analyzing the data, one of the most interesting and surprising facts I found was that the programming language with the highest average number of stars per repository was not one of the commonly expected languages like JavaScript or Python. Instead, it was MDX, a lesser-known language. This indicates that repositories using MDX tend to receive more attention and appreciation from the GitHub community, possibly due to the niche and specialized nature of the projects using this language.

# Recommendation

Based on my analysis, one actionable recommendation for developers is to focus on writing detailed and engaging bios on their GitHub profiles. My regression analysis showed a positive correlation between the length of a user's bio and the number of followers they have. This suggests that a well-crafted bio can help attract more followers. Therefore, developers should take the time to write a comprehensive bio that highlights their skills, experiences, and interests to make a strong impression on potential followers and collaborators.
