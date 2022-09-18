# **1. Data Representation Take-home Tech Assessment (TTA)**
## 1.1 Question:

With `monthly_data.csv`, `weekly_data.csv` and `hourly_data.csv` data files given to you by the engineering team, how do you use them to output **time series of normalized Google Trends data from 2017 till the present with time interval of hours that is relatively comparable/consistent**?


## 1.2 Solution:
Task: we need to find a comparable/consistent normalized version of the values in the houly_data file.

Let $n_{h,d,w,m,y}$ be the number of bitcoin searches in the hour $h$ of the day $d$ of the week $w$ of the month $m$ of the year $y$.

We need to find $\frac{n_{h,d,w,m,y}}{n_{hourly}^{max}}$ where $n_{hourly}^{max}$ is the maximum value that $n_{h,d,w,m,y}$ can take in all the data, but each value we observe in the hourly_data file is given by $\frac{n_{h,d,w,m,y}}{n_{w,m,y}^{max}}$ where $n_{w,m,y}^{max}$ is the maximum value that $n_{h,d,w,m,y}$ can take in a particular $w,m,y$ tuple. 

Definitions:

1. Let $n_{w,m,y}=\sum_{d}\sum_{h}n_{h,d,w,m,y}$ be the number of bitcoin searches in the specific week $w$ of month $m$ of year $y$.

    Adding up all elements of the hourly_data file by week, month, and year, we have:

    $\frac{n_{w,m,y}}{n_{w,m,y}^{max}}=\frac{\sum_{d}\sum_{h}n_{h,d,w,m,y}}{n_{w,m,y}^{max}}$   $\left( Eq. 1 \right)$

2. Let $n_{m,y}=\sum_{w}n_{w,m,y}$ be the number of bitcoin searches in the specific month $m$ of year $y$.

    Adding up all elements of the weekly_data file by month, and year, we have

    $\frac{n_{m,y}}{n_{y}^{max}}=\frac{\sum_{w}n_{w,m,y}}{n_{y}^{max}}$    $\left( Eq. 2 \right)$

    where $n_{y}^{max}$ is the maximum value that $n_{w,m,y}$ can take in a particular year $y$.

3. Each value we observe of the monthly_data file is given by $\frac{n_{m,y}}{n_{monthly}^{max}}$ where $n_{monthly}^{max}$ is the maximum value of $n_{m,y}$.



Therefore, to find $\frac{n_{h,d,w,m,y}}{n_{hourly}^{max}}$ we need: 

1. That for each value in the week_data file, $\frac{n_{w,m,y}}{n_{y}^{max}}$, using Eq. 2 we calculate:

    $\frac{n_{w,m,y}}{n_{monthly}^{max}}=\frac{n_{w,m,y}}{n_{y}^{max}}\frac{n_{y}^{max}}{n_{m,y}}\frac{n_{m,y}}{n_{monthly}^{max}}$ $\left( Eq. 3 \right)$

2. That for each value in the hourly_data file, $\frac{n_{h,d,w,m,y}}{n_{w,m,y}^{max}}$, using Eq. 1 and Eq. 3 we calculate:

    $\frac{n_{h,d,w,m,y}}{n_{monthly}^{max}}=\frac{n_{h,d,w,m,y}}{n_{w,m,y}^{max}}\frac{n_{w,m,y}^{max}}{n_{w,m,y}}\frac{n_{w,m,y}}{n_{monthly}^{max}}$ $\left( Eq. 4 \right)$

3. Let $\frac{n_{h,d,w,m,y}^{max}}{n_{monthly}^{max}}$ the maximum value that $\frac{n_{h,d,w,m,y}}{n_{monthly}^{max}}$ can take for all h,d,w,m,y. The comparable/consistent normalized version of the values in the houly_data file is then given by:

    $\frac{n_{h,d,w,m,y}}{n_{hourly}^{max}}=\frac{\frac{n_{h,d,w,m,y}}{n_{monthly}^{max}}}{\frac{n_{h,d,w,m,y}^{max}}{n_{monthly}^{max}}}$ $\left( Eq. 5 \right)$

## 1.3 Run the file:
To run the DataRepresentation_TTA.py file, from the terminal:  

    $ pip install -r requirements.txt
    
    $ python DataRepresentation_TTA.py
   
# **2. Coding & Data Collection Take-home Tech Assessment (TTA)**
## 2.1 Coding:
Submitted

## 2.2 Data Collection Take-home Tech Assessment:
2.2.1. describing your idea
I use the pytrends library to search for the word "bitcoin", and store the requested data in pandas dataframes. I follow the next steps:

Step 1: 
I requeste a monthly time series, normalized using all data points by default.

Step 2: 
I requeste a daily time series, normalized by month by default. I store this data in a pandas dataframe.

Step 3: 
I re-normalize the daily data, using all data points, so that all point as comparable. To do so, I follow:

 
1. Let $\frac{n_{m,y}}{n^{max}}$ be the number of bitcoin searches in the specific month $m$ of year $y$ observed in the monthly_data dataframe. 

2. Let $n_{m,y}=\sum_{d}n_{d,m,y}$ be the number of bitcoin searches in the specific month $m$ of year $y$, calculated from summing over the number of bitcoin searches in the specific day $d$ of month $m$ of year $y$ and let ${n_{d,m,y}^{max}}$ be the maximum value of that month.

    Adding up all elements of the daily_data dataframe by month, and year, we have:

    $\frac{n_{m,y}}{n_{d,m,y}^{max}}=\frac{\sum_{d}n_{d,m,y}}{n_{d,m,y}^{max}}$   $\left( Eq. 1 \right)$

3. Calculate:

    $weight = \frac{n_{d,m,y}^{max}}{\sum_{d}n_{d,m,y}} \frac{n_{m,y}}{n^{max}}$    $\left( Eq. 2 \right)$ 

4. Calculate the re-normalize time series by:

    $\frac{n_{d,m,y}}{n^{max}} = \frac{n_{d,m,y}}{n_{d,m,y}^{max}}weight$   $\left( Eq. 3 \right)$ 
    
    $\frac{n_{d,m,y}}{n_d^{max}} = \frac{\frac{n_{d,m,y}}{n^{max}}}{\frac{n_{d,m,y}^{max}}{n^{max}}}$   $\left( Eq. 4 \right)$ 
    
    where $\frac{n_{d,m,y}^{max}}{n^{max}}$ is the maximum value of $\frac{n_{d,m,y}}{n^{max}}$


2.2.2. the amount of time you spent on finishing the program code (or pseudo code),
One morning.

2.2.3. the different ways you have tried to approach the TECH ASSESSMENT, 
Just one way.

2.2.4. the reasons of settling on the current approach, and finally, 
I devoted the majority of the time to undestand the pytrend library. Once I collected the data, the next task is just to re-normalize the data. 

2.2.5. how to execute your program.    
    

# **Files:**
To run the DataCollection_TTA.py file, from the terminal: 

    $ pip install -r requirements.txt

    $ python DataCollection_TTA.py
    