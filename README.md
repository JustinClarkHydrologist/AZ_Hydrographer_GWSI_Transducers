# AZ_Hydrographer_GWSI_Transducers
Hydrograph Maker for GWSI Data Collected from Automated Sites (Transducers or Stevens Recorders).

Program Author: Justin Clark

Contributors: James Dieckhoff and Michael T. Giansiracusa

-This program takes data from an excel file and a text file and creates graphs that stand alone as PNG files.

-The excel files contain water level data and well construction data from wells in ADWRs GWSI database.

-The PNG files generated are saved to the current active directory.

-This program includes a for loop to make all the PNG files.

-This version (version 1.2) is a clean version that just makes PNG files, does not use Seaborn.

-Pandas and matplotlib are the primary libraries used for this program.


All data referenced can be downloaded here:

https://www.azwater.gov/sites/default/files/zip/GWSI_ZIP_20250714.zip

Approximate Run Time = 59 minutes for the entire state of Arizona

Computer with these specs:
Lenovo Ideapad
AMD Ryzen 5 4500U, 16 GB Ram
Windows 10 Home
