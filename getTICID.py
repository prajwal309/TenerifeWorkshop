import pandas as pd
import lightkurve as lk
import requests
from bs4 import BeautifulSoup


database = pd.read_csv('database/speculoosList.csv', delimiter='\t')
AlltargetGAIA = database['GAIA_ID'].values

for target in AlltargetGAIA:
    gaia_id = "GAIA DR2 "+ str(target)
    print(gaia_id)
    url = f"https://exofop.ipac.caltech.edu/tess/target.php?id={gaia_id}"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        overview_tid = soup.find('div', class_='overview_tid')
        if overview_tid:
            print(overview_tid.text.strip())
        else:
            print("Text not found")
   