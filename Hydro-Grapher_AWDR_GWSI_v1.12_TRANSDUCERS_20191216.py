"""     Python GWSI Water Levels Grapher  -  VERSION 1.12
             Started on 6/04/2019
             Last Updated 12/16/2019 (Dec. 16 2019, I am American)

@author: Justin A. Clark
@contibutor(s): Michael T. Giansiracusa

This program takes data from an excel file and a text file and creates graphs that stand alone as PNG files.
   The first txt files contain depth to water and water level elevation data.
   The xlsx file contains well construction data from wells in ADWRs GWSI database.
   The PNG files generated are saved to the current working drive (path is not defined).
   This program includes a for loop to make all the PNG files.
   This version (version 1.12) is a clean version that just makes basic PNG files, does not use Seaborn.
   Pandas and matplotlib are the primary libraries used.
   ~60 Lines of active code are used (the rest is just comments and blank lines).

This tool was designed for use by Arizona Department of Water Resources (ADWR) Groundwater Flow
and Transport Modelers to Process the input data for MODFLOW Models and PEST Calibration Runs.

All data referenced can be downloaded here:
https://new.azwater.gov/sites/default/files/GWSI_ZIP_10182019.zip

Approximate Run Time = 59 minutes       (HP Z240 Tower Workstation
                                        Intel I7-7700, 16 GB Ram
                                        Windows 10 Enterprise)
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime  # TODO this is unused and should be removed in a cleanup branch
from matplotlib import dates
from multiprocessing import Pool, cpu_count


##MAKE VARIABLES FOR THE FILENAMES
filename1 = "GWSI_TRANSDUCER_LEVELS.txt"
filename2 = "GWSI_SITES.xlsx"
#filename3 = "TucsonAMA_Errors_Dec2019.csv"

##DEFINE A LIST OF COLUMN NAMES based on GWSI Protocol, to be used reading first txt file
###THIS IS STILL VERY SLOPPY AND SHOULD BE PROGRAMMED USING DATA EXTRACTION, NOT HARD CODED
ColNames = ["WELL_SITE_ID","ID","Date","DEPTH_TO_WATER","WATER_LEVEL_ELEVATION","SOURCE_CODE","METHOD_CODE","REMARK_CODE","TEMPERATURE","BATTERY_VOLTAGE"]

## CREATE A PANDAS DataFrame WITH OBSERVATIONS From AUTOMATICALLY COLLECTED Depth to Water Measurements Extracted From Wells with High Frequency Data Collectors (Transducers). Data From GWSI Wells in Arizona.
df = pd.read_csv(filename1, delimiter = ",", engine = 'python', names=ColNames, index_col = False)

## Create a Pandas DataFrame with Well Construction Data
df2 = pd.read_excel(filename2, index_col = None)

#
##Change the name of a Well ID column in df2 to match df
col_start = "SITE_WELL_SITE_ID"
col = ColNames[0]
df2 = df2.rename(columns={col_start:col})

#
## Set Bottom Elevation
df2['Well_Bot_Elev'] = df2['SITE_WELL_ALTITUDE'] - df2['SITE_WELL_DEPTH']

#
##GET A LIST OF UNIQUE WELLS
wells = list(set(df[col]))   ## Mike G said this is not the best way, use the set method below
wells = set(df[col])


def figure_proc(location):
    df3 = pd.merge(df, df2, on="WELL_SITE_ID")

    df4 = df3.loc[df3[col] == location]
    df4['Date'] = pd.to_datetime(df4['Date'])
    df4 = df4.sort_values('Date')

    ##THIS SECTION MAKES THE WELL SPECIFIC 'Rise' COLUMN, RELATIVE TO LOWEST OBSERVATION
    min_hd_float = df4['WATER_LEVEL_ELEVATION'].min()
    df4['Rise'] = df4['WATER_LEVEL_ELEVATION'] - min_hd_float

    ## THIS IS AN ERROR AVOIDING STEP THAT IS SLOPPY, should remove individual "bad" data first.
    df4.fillna(value=0, inplace=True)

    ##THIS SECTION DELETES ROWS WITH "ZERO ERRORS"
    df4.drop(df4[df4['DEPTH_TO_WATER'] == 0].index, inplace=True)
    ## DROP DTW ENTRIES THAT PROBABLY HAVE ERRORS (water level data must be 'cleaned')
    ## Data contained in filename3 should be used to remove suspected anomolies

    min_date_datetime = df4['Date'].iloc[0]
    max_date_datetime = df4['Date'].iloc[len(df4['Date']) - 1]

    min_date_4fig = min_date_datetime.replace(month=1)
    min_date_4fig = min_date_4fig.replace(day=1)
    min_date_4fig = min_date_4fig.replace(hour=0)

    max_date_4fig = max_date_datetime + pd.offsets.DateOffset(years=1)
    max_date_4fig = max_date_4fig.replace(month=1)
    max_date_4fig = max_date_4fig.replace(day=1)

    plt.xlabel("Date")
    plt.rcParams['xtick.labelsize'] = 8

    x = df4['Date']
    y1 = df4['DEPTH_TO_WATER']
    y2 = df4['WATER_LEVEL_ELEVATION']

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, y1)
    ax1.set_ylabel("Depth to Water [ft bgs]")
    plt.gca().invert_yaxis()

    ax2 = ax1.twinx()
    ax2.plot(x, y2, 'b-')
    ax2.set_ylabel("Water Level Elevation [ft amsl]", color='g')

    for tl in ax2.get_yticklabels():
        tl.set_color('g')

    fig.suptitle('GWSI Site: ' + str(location) + ', RegID: 55-' + str(
        int(df4["SITE_WELL_REG_ID"].iloc[0])) + ', Depth: ' + str(
        int(df4["SITE_WELL_DEPTH"].iloc[0])) + ' ft', fontsize=12)

    ax1.grid(b=True, which='major', color='#666666', linestyle='-')

    myFmt = dates.DateFormatter("%Y")
    ax1.xaxis.set_major_formatter(myFmt)

    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)

    # SET X-AXIS LIMITS (xlim)
    ax1.set_xlim([min_date_4fig, max_date_4fig])

    ax1.xaxis.set_major_locator(dates.YearLocator(1))  # THIS WORKS

    plt.rcParams.update({'font.size': 12})

    plt.show() # TODO remove this, it significantly slows down the program.

    outname = str('Hydrographs_GWSI_Automated__') + str(location) + str('.png')
    fig.savefig(outname, dpi=400, bbox_inches='tight', pad_inches=.1)


with Pool(cpu_count()) as pool:
    pool.map(figure_proc, wells)
    pool.join()


#    outname = str('GWSI_WLE_ZipExtract_Seasonal_') + str(location) + str('__Raw_Data_Table.csv')
#    df4.to_csv(outname, index=False)
#
#    outname = str('_Error_Date_Bad.csv')
#    df.to_csv(outname, index=False)

##############################################################################
##############################################################################
##############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Example and Test Code Used for This Program   ##
"""
outname = str('test_df4.csv')
df4.to_csv(outname, index=False)


###seasonal trending wells with high variation:
#wells = [315614110543601, 315705110560901, 315909110540601, 320216110405901, 320249110413501, 320944111125701, 321034111140801, 321058110563301, 321244110504401, 321348111154401, 321404111153201, 321414111133601, 321424110432901, 321445110554601, 321456111160201, 321503110484901, 321504110521601, 321512110480701, 321523110491801, 321530110523501, 321537110585001, 321542110502701, 321548110561801, 321601110544601, 321703110575401, 321706110442201, 321745111012801, 321748110582101, 322238111065701, 322339111170001, 323635111330001]

###SET GRAPH STYLE, FORMATTING
#import seaborn as sns
#sns.set_style("darkgrid")

"""
###############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Websites Visited   ##
"""
secondary x axis:
https://pythonmatplotlibtips.blogspot.com/2018/01/add-second-x-axis-below-first-x-axis-python-matplotlib-pyplot.html
"""

