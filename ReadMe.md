## Details
**Created by:** Prajwal Niraula  
**For:** SPECULOOS Workshop at Tenerife

## Folders Description
- **figures**:  
    Contains figures showing light curves, Lomb-Scargle periodograms, and BLS results.
- **tessData**:  
    Contains all the downloaded TESS data.
- **database**:  
    Contains information on the 60 SPECULOOS targets, including GAIA IDs and cross-matched TESS IDs.
- **processedLC**:  
    Contains processed light curves for the targets extracted from the FITS files, normalized to the median flux of the sector.

## File Description
- **downloadScript.py**:  
    Script to download the data.
- **readData.py**:  
    Script to read the data.
- **run.ipynb**:  
    Jupyter notebook for working with the data.
- **getTICID.py**:  
    Script to get TIC IDs for the corresponding GAIA IDs. Results are saved in `databaseTIC.csv`.
