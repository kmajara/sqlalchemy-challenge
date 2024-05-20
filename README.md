# sqlalchemy-challenge

Title and Description: Climate Analysis and Flask API for Honolulu, Hawaii

Installation

Clone the repository to your local machine.

   git clone https://github.com/kmajara/sqlalchemy-challenge.git 

Usage
Part 1: Analyze and Explore the Climate Data

    Connect to the SQLite Database:
        Use the SQLAlchemy create_engine() function to connect to the hawaii.sqlite database.
        Reflect the tables into classes using the SQLAlchemy automap_base() function.
        Create references to the station and measurement classes.

    Perform Precipitation Analysis:
        Find the most recent date in the dataset.
        Query the previous 12 months of precipitation data.
        Load the query results into a Pandas DataFrame and plot the results.
        Print the summary statistics for the precipitation data.

    Perform Station Analysis:
        Calculate the total number of stations.
        Find the most-active stations by listing them in descending order of observation counts.
        Calculate the lowest, highest, and average temperatures for the most-active station.
        Query the previous 12 months of temperature observation data and plot a histogram.

Part 2: Design Your Climate App

    Set up Flask API:
        Create a Flask app and define the following routes:
            /: List all available routes.
            /api/v1.0/precipitation: Return the last 12 months of precipitation data as JSON.
            /api/v1.0/stations: Return a JSON list of stations.
            /api/v1.0/tobs: Return a JSON list of temperature observations for the previous year.
            /api/v1.0/<start> and /api/v1.0/<start>/<end>: Return JSON lists of the minimum, average, and maximum temperatures for the specified date range.


Features

    Climate data analysis using SQLAlchemy, Pandas, and Matplotlib.
    Flask API to provide access to climate data through various endpoints.

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes and commit them (git commit -m 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Open a pull requ

    est.

License

This project is licensed under the MIT License.
Credits

    Data source: Provided SQLite database (hawaii.sqlite).
    Project starter files: climate_starter.ipynb.

Contact

For any questions or inquiries, please contact [kops4jc@gmail.com].
