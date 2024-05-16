import json
import re

# Load the JSON data
with open("lookup_info.json", "r") as json_file:
    data = json.load(json_file)

# Categories and their corresponding keywords
categories = {
    "sports": ["sports", "game", "football", "basketball", "tennis", "cricket"],
    "politics": ["politics", "government", "election", "minister", "assembly", "govt"],
    "entertainment": ["entertainment", "celebrity", "movie", "music", "arts", "actor", "actress", "box office", "song", "dance"],
    "business": ["business", "economy", "finance", "market", "industry", "stock", "company"],
    "crime": ["crime", "law enforcement", "offense", "criminal", "felony", "justice", "investigation"],
    "education": ["education", "school", "college", "university", "student", "teacher", "learning"],
    "tech": ["technology", "tech", "innovation", "science", "computer", "internet", "software", "hardware"]
}
# Initialize counts for each category
category_counts = {category: 0 for category in categories}

# Function to check if a pattern related to a category is present in text


def check_pattern(text, patterns):
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


# Iterate through articles and count the number of articles in each category
for title, body in zip(data["article-title"], data["article-body"]):
    # Flag to indicate if a match has been found for any category
    match_found = False
    for category, patterns in categories.items():
        if check_pattern(title, patterns) or check_pattern(body, patterns):
            category_counts[category] += 1
            # Set match_found to True to avoid counting the article in multiple categories
            match_found = True
            # Break out of the loop once a match is found for a category
            break
    # If no match is found for any category, print a message for debugging
    if not match_found:
        print(f"No match found for article: {title}")

# Print the counts for each category
for category, count in category_counts.items():
    print(f"{category}: {count}")
