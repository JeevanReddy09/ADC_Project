import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ev_database"]
collection = db["vehicle_data"]

# Streamlit App Configuration
st.set_page_config(page_title="EV Dashboard", page_icon="⚡", layout="wide")

# Header
st.title("⚡ Electric Vehicle Dashboard")
st.write("Explore EV data with an interactive dashboard.")

# Sidebar - User Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Choose a Feature",
    ["Vehicle Details", "VIN Retrieval by Criteria", "Update EV Info", "Popular Models & Makes", "EV Adoption by County"]
)

# Style Customization for Buttons
st.markdown("""
    <style>
    .stButton > button {
        border-radius: 12px;
        background-color: #FF6347; /* Vibrant color */
        color: white;
        font-size: 16px;
        padding: 8px 20px;
        border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Feature 1: VIN Lookup
if page == "Vehicle Details":
    st.subheader("🔍 Vehicle Information Lookup")
    vin_input = st.text_input("Enter VIN (First 10 Characters)", max_chars=10)
    if st.button("Search VIN"):
        # Query the database
        car_details = collection.find_one({"vin_1_10": vin_input})
        if car_details:
            st.success("Vehicle details found!")
            for key, value in car_details.items():
                if key != "_id":
                    st.write(f"**{key.replace('_', ' ').capitalize()}**: {value}")
        else:
            st.error("No vehicle found with the given VIN.")

# Feature 2: VIN Retrieval by Criteria
elif page == "VIN Retrieval by Criteria":
    st.subheader("🔍 VIN Retrieval by Criteria")
    st.write("Enter vehicle details (make, model, zip code, and year) to retrieve VIN numbers.")

    # Form for Input Fields
    with st.form("criteria_form"):
        make = st.text_input("Enter Make (e.g., Tesla, Nissan):")
        model = st.text_input("Enter Model (e.g., Model 3, Leaf):")
        zip_code = st.text_input("Enter ZIP Code (e.g., 98101):")
        year = st.text_input("Enter Model Year (e.g., 2021):")
        submit_button = st.form_submit_button("Search")

    # Search and Display Results
    if submit_button:
        # Build the query dynamically
        query = {}
        if make:
            query["make"] = make
        if model:
            query["model"] = model
        if zip_code:
            query["zip_code"] = zip_code
        if year:
            query["model_year"] = year
        
        # Query MongoDB
        results = list(collection.find(query, {"vin_1_10": 1, "_id": 0}))
        
        # Display Results
        if results:
            st.success(f"Found {len(results)} VIN(s) matching your criteria.")
            for idx, result in enumerate(results, start=1):
                st.write(f"**VIN {idx}:** {result['vin_1_10']}")
        else:
            st.error("No vehicles found matching your criteria.")

# Feature 3: Update EV Info
elif page == "Update EV Info":
    st.subheader("✏️ Update EV Information")
    vin_input = st.text_input("Enter VIN (First 10 Characters) to Update")
    if vin_input:
        car_details = collection.find_one({"vin_1_10": vin_input})
        if car_details:
            st.write("Current details of the vehicle:")
            for key, value in car_details.items():
                if key != "_id":
                    st.write(f"**{key.replace('_', ' ').capitalize()}**: {value}")
            
            st.write("Update the details below:")
            
            # Form for updating fields
            make = st.text_input("Update Make", value=car_details.get("make", ""))
            model = st.text_input("Update Model", value=car_details.get("model", ""))
            year = st.text_input("Update Year", value=car_details.get("model_year", ""))
            zip_code = st.text_input("Update ZIP Code", value=car_details.get("zip_code", ""))
            
            # Optional fields
            electric_range = st.text_input("Update Vehicle Range", value=car_details.get("electric_range", ""))
            base_msrp = st.text_input("Update Vehicle Price (Base MSRP)", value=car_details.get("base_msrp", ""))
            
            if st.button("Update Info"):
                updated_data = {
                    "make": make,
                    "model": model,
                    "model_year": year,
                    "zip_code": zip_code,
                    "electric_range": electric_range,
                    "base_msrp": base_msrp  # Updated the key to base_msrp instead of price
                }
                collection.update_one({"vin_1_10": vin_input}, {"$set": updated_data})
                st.success("Vehicle information updated successfully!")
        else:
            st.error("No vehicle found with the given VIN.")


# Feature 4: Popular Models & Makes
elif page == "Popular Models & Makes":
    st.subheader("🚗 Popular Models & Makes")
    if st.button("Fetch Popular Models"):
        pipeline = [
            {"$group": {"_id": {"make": "$make", "model": "$model"}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}  # Top 10 models
        ]
        results = list(collection.aggregate(pipeline))
        data = [{"Make": r["_id"]["make"], "Model": r["_id"]["model"], "Count": r["count"]} for r in results]
        df = pd.DataFrame(data)

        # Display Data
        st.dataframe(df)

        # Plot
        fig = px.bar(
            df,
            x="Model",
            y="Count",
            color="Make",
            title="Top 10 Popular EV Models",
            labels={"Count": "Number of Registrations"},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig, use_container_width=True)

# Feature 5: EV Adoption by County
elif page == "EV Adoption by County":
    st.subheader("📊 EV Adoption by County")
    if st.button("Fetch EV Adoption Data"):
        pipeline = [
            {"$group": {"_id": "$county", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        results = list(collection.aggregate(pipeline))
        data = [{"County": r["_id"], "Registrations": r["total"]} for r in results]
        df = pd.DataFrame(data)

        # Display Data
        st.dataframe(df)

        # Plot
        fig = px.bar(
            df,
            x="County",
            y="Registrations",
            title="EV Registrations by County",
            labels={"Registrations": "Number of Registrations"},
            color="County",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig, use_container_width=True)





# Footer
st.markdown("---")
    
