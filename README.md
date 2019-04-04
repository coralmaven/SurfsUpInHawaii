# Surfs Up!

![surfs-up.jpeg](Images/surfs-up.jpeg)

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

## Climate Analysis and Exploration: climateInHawaii.ipynb

 Python and SQLAlchemy are used to do basic climate analysis and data exploration of the climate database. 

### Precipitation Analysis

* Retrieve the last 12 months of precipitation data and analyze.

### Station Analysis

* Find the most active stations.

* Retrieve the last 12 months of temperature observation data (tobs).

### Temperature Analysis

*  `calc_temps` accepts a start date and end date in the format `%Y-%m-%d` and returns the minimum, average, and maximum temperatures for that range of dates.

* Calculate the min, avg, and max temperatures for our trip using the matching dates from the previous year (i.e., use "2017-01-01" if our trip start date was "2018-01-01").

### Daily Rainfall Average.

* The rainfall per weather station using the previous year's matching dates.

* The daily normals. Normals are the averages for the min, avg, and max temperatures.

## Step 2 - Climate App: SurfsUp.py

A Flask API based on the queries from step 1.


### Routes

* `/`

  * Home page.

  * all routes that are available.

* `/api/v1.0/precipitation`

  * A Dictionary using `date` as the key and `prcp` as the value.

  * Returns the JSON representation of the dictionary.

* `/api/v1.0/stations`

  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

- - -

## Copyright

Data Boot Camp ©2019. All Rights Reserved.
