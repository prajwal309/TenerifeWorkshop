import lightkurve as lk
import numpy as np
import pandas as pd
import os


data = pd.read_csv('database/databaseTIC.csv')

for target in data["TICID"]:
    try:
        target = f"TIC {target}"
        print(f"Downloading data for {target}")
        search = lk.search_lightcurve(f"{target}")
        destination = f"tessData/{target.replace(' ', '')}"
        os.makedirs(destination, exist_ok=True)
        print("the destination", destination)
        search.download_all(download_dir=destination)
    except Exception as e:
        print(f"Failed to download data for {target}: {e}")
        continue
#now download the data using lightcruve