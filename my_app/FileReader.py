import pandas as pd

# Load files
df_old = pd.read_csv("baseline.csv")        # new scrape
df_new = pd.read_csv("nov2.csv")  # old scrape

# Get URLs, strip spaces, lowercase
old_urls = df_old["profile_url"].str.strip().str.lower()
new_urls = df_new["profile_url"].str.strip().str.lower()

# Find differences
unfollowed = set(old_urls) - set(new_urls)  # in old but not in new
new_followed = set(new_urls) - set(old_urls)  # in new but not in old

print("Unfollowed (-):", unfollowed)
print("Newly followed (+):", new_followed)
