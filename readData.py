import numpy as np
import pandas as pd
from astropy.io import fits
import os
import matplotlib.pyplot as plt
from wotan import flatten
from astropy.timeseries import LombScargle

def getAllFiles(Location):
    files = []
    for r, d, f in os.walk(Location):
        for file in f:
            if '.fits' in file:
                files.append(os.path.join(r, file))
    return files

database = pd.read_csv('database/databaseTIC.csv')

for GAIA_ID, TIC_ID in zip(database["GAIAID"],database["TICID"]):
    print(f"Processing TIC {TIC_ID}")
    ID = f"TIC {TIC_ID}"
    AllFiles = getAllFiles(f"tessData/{ID.replace(' ', '')}")

    #get all files with SPOC if none chose eleanor
    lcSelection = ["spoc", "qlp", "eleanor", "everest"]
    
    for lc in lcSelection:
        selectedFiles = [fileItem for fileItem in AllFiles if lc in fileItem.lower()]
        if len(selectedFiles) > 0:
            break
    
    print("The selected files are", selectedFiles)
    if len(AllFiles)>0 and len(selectedFiles) == 0:
        print("No SPOC or eleanor files found")
        input("Wait here...")



    if len(selectedFiles) == 0:
        print(f"No files found for {ID}")
    else:
        AllTime = []
        AllFlux = []
        for fileItem in selectedFiles:

            with fits.open(fileItem) as hdul:
                ColumnName = hdul[1].columns.names

               

                data = hdul[1].data
                CurrentTime = data["TIME"]
                if "PDCSAP_FLUX" in ColumnName:
                    CurrentFlux = data["PDCSAP_FLUX"]
                elif "SAP_FLUX" in ColumnName:
                    CurrentFlux = data["SAP_FLUX"]
                elif "FLUX_CORR" in ColumnName:
                    CurrentFlux = data["FLUX_CORR"]
                elif "PCA_FLUX" in ColumnName:
                    CurrentFlux = data["PCA_FLUX"]
                elif "cal_psf_flux" in ColumnName:
                    CurrentFlux = data["cal_psf_flux"]
                elif "FLUX" in ColumnName: #for everest
                    CurrentFlux = data["FLUX"]
                else:
                    print("No flux data found")
                    print("The columns is", ColumnName)
                    input("Press enter to continue")
                if "QUALITY" in ColumnName:
                    Quality = data["QUALITY"]
                    CurrentTime = CurrentTime[Quality == 0]
                    CurrentFlux = CurrentFlux[Quality == 0]
                
                CurrentFlux = CurrentFlux/np.nanmedian(CurrentFlux)

                #flatten the data
                AllTime.extend(CurrentTime)
                AllFlux.extend(CurrentFlux)
        
        plt.figure()
        plt.plot(AllTime, AllFlux, 'k.')
        plt.xlabel("Time (BJD)")
        plt.ylabel("Flux")
        plt.title(f"{ID}")
        plt.show()

        AllTime = np.array(AllTime)
        AllFlux = np.array(AllFlux)

        NanFlux = np.isnan(AllFlux)
        AllTime = AllTime[~NanFlux]
        AllFlux = AllFlux[~NanFlux]

        #Arrange the data
        SortedIndex = np.argsort(AllTime)
        AllTime = AllTime[SortedIndex]
        AllFlux = AllFlux[SortedIndex]

        #Now save the data
        saveLocation = f"processedLC/{GAIA_ID}.txt"
        np.savetxt(saveLocation, np.transpose((AllTime, AllFlux)))
