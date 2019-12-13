"""     Python GWSI Water Levels Grapher  -  VERSION 1.11
             Started on 6/04/2019
             Last Updated 11/14/2019 (November 14 2019, I am American)

@author: Justin A. Clark

This program takes data from an excel file and a text file and creates graphs that stand alone as PNG files.
   The excel files contain water level data and well construction data from wells in ADWRs GWSI database.
   The PNG files generated are saved to the main "Path" Folder.
   This program includes a loop to make all the PNG files.
   This version (version 1.11) is a clean version that just makes PNG files, does not use Seaborn.
   matplotlib and Pandas are the primary libraries.

This tool was designed for use by Arizona Department of Water Resources (ADWR) Groundwater Flow 
and Transport Modelers to Process the input data for MODFLOW Models and PEST Calibration Runs.

Approximate Run Time = 9 minutes 51.4 sec      (HP Z240 Tower Workstation
                                               Intel I7-7700, 16 GB Ram
                                               Windows 10 Enterprise)
"""
import pandas as pd
import matplotlib.pyplot as plt
import os, xlsxwriter
from matplotlib.dates import DateFormatter
from matplotlib.dates import YearLocator

#
#Find Kernel's Current Directory, set to desired location if necessary
cwd = os.getcwd()
Path = r"C:\GIS\ADWR\GWSI_ZIP\Data_Tables"
os.chdir(Path)
cwd = os.getcwd()


#
## Set variables for the filenames
filename1 = "GWSI_TRANSDUCER_LEVELS.txt"
filename2 = "GWSI_SITES.xlsx"
filename3 = "TucsonAMA_Errors_Nov2019.csv"

#
## Define a list of column names based on GWSI Protocol, to be used reading first txt file
###THIS IS STILL VERY SLOPPY AND SHOULD BE PROGRAMMED USING DATA EXTRACTION, NOT HARD CODED
ColNames = ["WELL_SITE_ID","ID","Date","DEPTH_TO_WATER","WATER_LEVEL_ELEVATION","SOURCE_CODE","METHOD_CODE","REMARK_CODE","TEMPERATURE","BATTERY_VOLTAGE"]

#
## Create a Pandas DataFrame with Water Level Elevations Extracted From Wells with High Frequency Data (Transducers)
df = pd.read_csv(filename1, delimiter = ",", engine = 'python', names=ColNames, index_col = False)

#
## DROP DTW ENTRIES THAT PROBABLY HAVE ERRORS (For Now Only 4 wells in TAMA)
dfDrop = pd.read_csv(filename3, delimiter = ",", engine = 'python', index_col =False)
#indexNames = dfDrop['ID'].index

#
## Create a Pandas DataFrame with Well Construction Data
df2 = pd.read_excel(filename2, index_col = None)

#
##Change the name of a Well ID column in df2 to match df
col_start = "SITE_WELL_SITE_ID"
col = ColNames[0]
df2 = df2.rename(columns={col_start:col})

#
## Set Bottom Elevation
df2['WELL_BOT'] = df2['SITE_WELL_ALTITUDE'] - df2['SITE_WELL_DEPTH']

#
##GET A LIST OF UNIQUE WELLS
wells = list(set(df[col]))

#Set Kernel's Current Directory to desired location
Path = r"C:\GIS\ADWR\PythonOutput"
os.chdir(Path)
cwd = os.getcwd()

wells = [315614110543601,321745111012801,321542110502701,321537110585001]

for location in wells:
     ##THIS FIRST SECTION MAKES THE WELL SPECIFIC DATAFRAME AND ADDS a new 'Rise' column
     df3 = df.loc[df[col] == location].copy()
###     df3 = df.loc[df[col] == location] ##WARNING POPPED UP
###     df3 = df.loc[df[col] == location, :]
     ###THE NEXT STEP COULD PROBABLY BE DONE BY RE-INDEXING "df3.Date"
     df3['UpDate'] = pd.to_datetime(df3.Date)
     df3 = df3.sort_values('UpDate')
     
     ##THIS METHOD GIVES A WARNING, FIX LATER
     elev = df2[df2[col]==location]['SITE_WELL_ALTITUDE']
     df3['LSE'] = elev.iloc[0]
     
     bottom = df2[df2[col]==location]['WELL_BOT']
     df3['Bottom'] = bottom.iloc[0]
     
     depth = df2[df2[col]==location]['SITE_WELL_DEPTH']
     df3['Depth'] = depth.iloc[0]
     
     RegNo = df2[df2[col]==location]['SITE_WELL_REG_ID']
     df3['Reg_No'] = RegNo.iloc[0]
     RegNo = df3.Reg_No.iloc[0]

     min_hd_float = df3['WATER_LEVEL_ELEVATION'].min()
     df3['Rise'] = df3['WATER_LEVEL_ELEVATION'] - min_hd_float

     ## This is a sloppy way to avoid errors, should add individual replacers above
     df3.fillna(value = 0, inplace = True)

     #
     ## THIS SECTION DEFINES AXES MIN/MAX
     min_date_str = df3['UpDate'].min()
     min_date_datetime = pd.to_datetime(min_date_str)

     min_date_datetime = df3['UpDate'].min() - pd.DateOffset(years = 1)

     max_date_str = df3['UpDate'].max()
     max_date_datetime = pd.to_datetime(max_date_str)

     #
     ## DELETE THESE ROW INDEXES FROM DataFrame3
#     cond = df3['ID'].isin(dfDrop['ID']) == True
#     df3.drop(df3[cond].index, inplace = True)

     plt.xlabel("Date")
     xrange = pd.date_range(min_date_datetime, end=max_date_datetime, freq='A')
     plt.rcParams['xtick.labelsize']=8

     x = df3['UpDate']
     y1 = df3['DEPTH_TO_WATER']
     y2 = df3['WATER_LEVEL_ELEVATION']

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

     fig.suptitle('GWSI Site: ' + str(location) + ', RegID: 55-' + str(int(df3["Reg_No"].iloc[0])) + ', Depth: ' + str(int(df3["Depth"].iloc[0]))+ ' ft', fontsize=12)

     ax1.grid(b=True, which='major', color='#666666', linestyle='-')

     myFmt = DateFormatter("%Y")
     ax1.xaxis.set_major_formatter(myFmt)
     years = YearLocator()
     ax1.xaxis.set_major_locator(YearLocator())
     ax1.format_xdata = DateFormatter('%Y-%m-%d')
     
     for tick in ax1.get_xticklabels():
          tick.set_rotation(90)

     plt.rcParams.update({'font.size': 12})

     plt.show()

     outname = str('Hydrographs_GWSI_') + str(location) + str('__Transducer.png')
     fig.savefig(outname, dpi = 400, bbox_inches='tight', pad_inches=.1)
     
     outname = str('GWSI_WLE_ZipExtract_Seasonal_') + str(location) + str('__Raw_Data_Table.csv')
     df3.to_csv(outname, index=False)

##############################################################################
##############################################################################
##############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Example and Test Code Used for This Program   ##
"""
#
## Get a list of columns in the initial DataFrame
df4 = df2.loc[df2[col] == set(df[col])]


###seasonal trending wells with high variation:
#wells = [315614110543601, 315705110560901, 315909110540601, 320216110405901, 320249110413501, 320944111125701, 321034111140801, 321058110563301, 321244110504401, 321348111154401, 321404111153201, 321414111133601, 321424110432901, 321445110554601, 321456111160201, 321503110484901, 321504110521601, 321512110480701, 321523110491801, 321530110523501, 321537110585001, 321542110502701, 321548110561801, 321601110544601, 321703110575401, 321706110442201, 321745111012801, 321748110582101, 322238111065701, 322339111170001, 323635111330001]
#wells = [315614110543601, 315705110560901]

#     #
#     ## Error Checker
#     wellbot = df3.iloc[0].loc['Bottom']
#     if wellbot = np.nan

##
###SET GRAPH STYLE, FORMATTING
#import seaborn as sns
#sns.set_style("darkgrid")

import datetime
Time_Start = datetime.datetime.now()
Time_End = datetime.datetime.now()
Run_Time = Time_End - Time_Start

#
##Find Kernel's Current Directory, set to desired location if necessary
import os
cwd = os.getcwd()
Path = "J:\HYDRO\pythonShare\Programs\JustinClark\SeasonalTrend_Grapher"
os.chdir(Path)
cwd = os.getcwd()

iloc vs query:
df.loc[df['B'] == 3, 'A']
df.query('B==3')['A']
df[df['B']==3]['A']
"""
###############################################################################
#  ### ### ### ### ### #### ### ### ### ### ### #### ### ### ### ### ### ###  #
##   Websites Visited   ##
"""
https://pythonmatplotlibtips.blogspot.com/2018/01/add-second-x-axis-below-first-x-axis-python-matplotlib-pyplot.html

https://stackoverflow.com/questions/14946371/editing-the-date-formatting-of-x-axis-tick-labels-in-matplotlib

https://stackoverflow.com/questions/2051744/reverse-y-axis-in-pyplot

https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.axes.Axes.yaxis_inverted.html#matplotlib.axes.Axes.yaxis_inverted

https://matplotlib.org/3.1.1/gallery/subplots_axes_and_figures/invert_axes.html

https://www.programcreek.com/python/example/61483/matplotlib.dates.DateFormatter

https://stackoverflow.com/questions/4761623/changing-the-color-of-the-axis-ticks-and-labels-for-a-plot-in-matplotlib

https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py
https://scentellegher.github.io/programming/2017/05/24/pandas-bar-plot-with-formatted-dates.html
https://stackoverflow.com/questions/25973581/how-do-i-format-axis-number-format-to-thousands-with-a-comma-in-matplotlib
http://kitchingroup.cheme.cmu.edu/blog/2013/09/13/Plotting-two-datasets-with-very-different-scales/


https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html


https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
http://ishxiao.com/blog/python/2017/07/23/how-to-change-the-font-size-on-a-matplotlib-plot.html
https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.get_yticklabels.html
https://plot.ly/python/subplots/

https://stackoverflow.com/questions/45943321/convert-datetimeindex-to-contain-only-year-hour-and-day-not-time-information

secondary x axis:
https://pythonmatplotlibtips.blogspot.com/2018/01/add-second-x-axis-below-first-x-axis-python-matplotlib-pyplot.html

https://stackoverflow.com/questions/28754603/indexing-pandas-data-frames-integer-rows-named-columns

dropping data:
https://thispointer.com/python-pandas-how-to-drop-rows-in-dataframe-by-conditions-on-column-values/
"""