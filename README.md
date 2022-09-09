# **Question:**

With `monthly_data.csv`, `weekly_data.csv` and `hourly_data.csv` data files given to you by the engineering team, how do you use them to output **time series of normalized Google Trends data from 2017 till the present with time interval of hours that is relatively comparable/consistent**?


## **Solution:**
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

# **Files:**
To run the normalization_hourly_data.py file: 

    $ pip install -r requirements.txt
    
    $ python normalization_hourly_data.py