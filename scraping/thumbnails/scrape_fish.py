import pandas as pd
import sys
from scrape import scrape

fish_df = pd.read_csv(sys.argv[1], names=['fish'])
query_suffix = sys.argv[2] # For adding extra data to the search like "fish" or "lake erie"
count = int(sys.argv[3])
img_path = sys.argv[4]
dfs = []
for fish in fish_df.fish:
	scrape(img_path, fish.replace(' ','_'), fish + ' ' + query_suffix, count)
