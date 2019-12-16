# AZ_Hydrographer_GWSI_Transducers
Hydrograph Maker for GWSI Data Collected from Automated Sites (Transducers or Stevens Recorders).

Program Author: Justin Clark

Contributors: James Dieckhoff and Michael T. Giansiracusa

-This program takes data from an excel file and a text file and creates graphs that stand alone as PNG files.

-The excel files contain water level data and well construction data from wells in ADWRs GWSI database.

-The PNG files generated are saved to the current active directory.

-This program includes a for loop to make all the PNG files.

-This version (version 1.12) is a clean version that just makes PNG files, does not use Seaborn.

-Pandas and matplotlib are the primary libraries used for this program.


Designed for use by Arizona Department of Water Resources (ADWR) Groundwater Flow 
and Transport Modelers to Process the input data for MODFLOW Models and PEST Calibration Runs.


All data referenced can be downloaded here:
https://new.azwater.gov/sites/default/files/GWSI_ZIP_10182019.zip


Approximate Run Time = 59 minutes 

Computer with these specs:
HP Z240 Tower Workstation
Intel I7-7700, 16 GB Ram
Windows 10 Enterprise
