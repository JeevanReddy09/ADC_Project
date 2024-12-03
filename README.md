
# ⚡ Electric Vehicle Dashboard Using MongoDB and Streamlit
## Overview



The **Electric Vehicle Dashboard** is an interactive web application built using **Streamlit** and **MongoDB**. It allows users to explore and analyze electric vehicle (EV) data, including vehicle details, VIN lookups, popular models, and EV adoption statistics by county. 

This project involves three main components:
1. **Data Cleaning and Conversion**: Processing and formatting raw EV data for analysis.
2. **Data Upload to MongoDB**: Storing the cleaned data in a MongoDB database using MongoDB Compass GUI.
3. **Streamlit UI Application**: Providing an interactive user interface for data exploration and visualization.

Additionally, a Jupyter Notebook (`test.ipynb`) is included for initial testing and querying the MongoDB database directly.

## Features

- **Vehicle Details Lookup**: Search for specific vehicle information using VIN.
- **VIN Retrieval by Criteria**: Retrieve VINs based on make, model, zip code, and year.
- **Update EV Information**: Update existing EV records in the database.
- **Popular Models & Makes**: Visualize the most popular EV models and makes.
- **EV Adoption by County**: Analyze EV registration trends across different counties.

## Technologies Used

- **Python 3.x**
- **Streamlit**: For building the interactive web application.
- **MongoDB**: As the database to store and manage EV data.
- **MongoDB Compass**: GUI tool for managing MongoDB databases.
- **PyMongo**: Python driver for interacting with MongoDB.
- **Pandas**: For data manipulation and analysis.
- **Plotly Express**: For creating interactive visualizations.
- **Jupyter Notebook**: For initial data testing and querying.

## Project Structure

The file_conversion script processes and cleans the Washington State EV charging station dataset in JSON format. It extracts metadata, formats the data, and saves it to a new JSON file for easier analysis.

The data was loaded to MongoDB using MongoDB GUI Compass.

This is the link to the download the dataset - https://data.wa.gov/api/views/f6w7-q2d2/rows.json?accessType=DOWNLOAD