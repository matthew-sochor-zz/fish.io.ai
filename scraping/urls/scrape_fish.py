import pandas as pd
from subprocess import check_output
import sys

fish_df = pd.read_csv(sys.argv[1],names=['fish'])

dfs = []
for fish in fish_df.fish:
    output = check_output(['node','scrape_image_urls.js',fish + ' fish',sys.argv[2]])
    splits = str(output).replace('\\n','').split(' url: ')
    urls = [s.split(',    width')[0][1:-1] for s in splits[1:]]
    dfs.append(pd.DataFrame({'fish': fish, 'url': urls}))

out_df = pd.concat(dfs)
out_df.to_csv(sys.argv[3], sep='|', index=False)
