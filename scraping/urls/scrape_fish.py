import pandas as pd
from subprocess import check_output
import sys

fish_df = pd.read_csv(sys.argv[1],names=['fish'])

url_dict = {}
for fish in fish_df.fish:
    output = check_output(['node','scrape_image_urls.js',fish,sys.argv[2]])
    splits = str(output).replace('\\n','').split(' url: ')
    urls = [s.split(',    width')[0][1:-1] for s in splits[1:]]
    url_dict[fish] = urls

url_df = pd.DataFrame(url_dict)
url_df.to_csv(sys.argv[3], sep='|', index=False)