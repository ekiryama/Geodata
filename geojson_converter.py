import streamlit as st
import pandas as pd
import geojson
from shapely import wkt
from shapely.geometry import mapping
import re
import os

# Display the image on the app
with st.container():
    image="sucafinaLogo.JPG"
    st.image(image, width=200) 

st.title("Conversion of CSV to GeoJson")

st.subheader("Upload the CSV (Direct & Indirect supply chains)")
uploaded_file = st.file_uploader("Choose a csv file", type="csv", key="uploader1")

def fix_wkt(wkt):
    # Check if the input is a polygon
    if wkt.strip().startswith("POLYGON"):
        # Extract the coordinates part of the WKT
        coords = re.findall(r"\(\((.*)\)\)", wkt)
        if coords:
            coord_list = coords[0].strip().split(",")
            
            # Remove any trailing commas or empty points
            coord_list = [c.strip() for c in coord_list if c.strip()]
            
            # Ensure the polygon is closed (start and end point are the same)
            if coord_list[0] != coord_list[-1]:
                coord_list.append(coord_list[0])
            
            # Reconstruct the fixed WKT
            fixed_coords = ", ".join(coord_list)
            return f"POLYGON (({fixed_coords}))"
    return wkt  # Return original WKT if it's not a polygon

if uploaded_file is not None:
    
    # Get the file name without extension
    file_name = os.path.splitext(uploaded_file.name)[0]
    
    df= pd.read_csv(uploaded_file)
    
    # Check if all required columns are present
    required_columns = ["Geometry", "ProducerName", "Area", "ProducerCountry", "EUDR compliance"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"The file is not in the correct format, please use the current export from the dashboard with columns labeled: {', '.join(missing_columns)}")
    else:
        st.subheader("Data Preview")
        st.write("Total Number of features: ", df.shape[0])
        st.write(df.head())
        features = []
        # Fix WKT polygons
        df["Geometry"] = df["Geometry"].apply(fix_wkt)
    
        # Loop through each row in the DataFrame to create GeoJSON features
        for _, row in df.iterrows():
            # Convert the WKT geometry to a shapely object
            geometry = wkt.loads(row['Geometry'])
            
            # Create a GeoJSON feature with properties and geometry
            feature = geojson.Feature(
                geometry=mapping(geometry),
                properties = {
                    "ProducerName": str(row.get("ProducerName", "Unknown")),
                    "Area": float(row.get("Area", 0)),
                    "ProducerCountry": str(row.get("ProducerCountry", "Unknown")),
                    "ProductionPlace": str(row.get("ProductionPlace", "Unknown")),
                    "EUDR compliance": str(row.get("EUDR compliance", "Unknown"))
                }
            )
            
            # Append the feature to the list of features
            features.append(feature)
            
        # Define the output filename
        geojson_filename = f"{file_name}.geojson"

    
        # Create a GeoJSON FeatureCollection
        feature_collection = geojson.FeatureCollection(features)
    
        # # Save the FeatureCollection to a GeoJSON file
        # with open('MyOutput.geojson', 'w') as f:
        #     geojson.dump(feature_collection, f)
    
        st.download_button(
            label="Download GeoJSON",
            data= geojson.dumps(feature_collection),
            file_name= geojson_filename,
            mime="application/geo+json"
        )
        # print("GeoJSON file has been created successfully.")

## ------------------------------  ICE-COT conversion  -------------------------------
st.subheader("Upload the CSV (ICE-COT)")
uploaded_file2 = st.file_uploader("Choose a csv file", type="csv", key="uploader2")


if uploaded_file2 is not None:
    
    # Get the file name without extension
    file_name = os.path.splitext(uploaded_file2.name)[0]
    
    df2= pd.read_csv(uploaded_file2)
    
    # Check if all required columns are present
    required_columns2 = ["Geometry", "Commodity", "Area", "ProducerCountry", "Variety", "CTOFarmerID", "Aggregator_ID", "CTOPlotID","DateOfMapping"]
    missing_columns2 = [col for col in required_columns2 if col not in df2.columns]

    if missing_columns2:
        st.error(f"The file is not in the correct format, please use the current export from the dashboard with columns labeled: {', '.join(missing_columns2)}")
        st.stop()
    else:
        st.subheader("Data Preview")
        st.write("Total Number of features: ", df2.shape[0])
        st.write(df2.head())
        features = []
        # Fix WKT polygons
        df2["Geometry"] = df2["Geometry"].apply(fix_wkt)
    
        # Loop through each row in the DataFrame to create GeoJSON features
        for _, row in df2.iterrows():
            # Convert the WKT geometry to a shapely object
            geometry = wkt.loads(row['Geometry'])
            
            # Create a GeoJSON feature with properties and geometry
            feature = geojson.Feature(
                geometry=mapping(geometry),
                properties = {
                     "ProducerCountry": str(row.get("ProducerCountry", "Unknown")),
                    "Commodity": str(row.get("Commodity", "Unknown")),
                    "Variety": str(row.get("Variety", "Unknown")),
                    "CTOFarmerID": str(row.get("CTOFarmerID", "Unknown")),
                    "Aggregator_ID": str(row.get("Aggregator_ID", "Unknown")),
                    "CTOPlotID": str(row.get("CTOPlotID", "Unknown")),
                    "DateOfMapping": str(row.get("DateOfMapping", "Unknown")),
                     "Area": float(row.get("Area", 0))
                }
            )
            
            # Append the feature to the list of features
            features.append(feature)
            
        # Define the output filename
        geojson_filename = f"{file_name}.geojson"

    
        # Create a GeoJSON FeatureCollection
        feature_collection = geojson.FeatureCollection(features)
    
    
        st.download_button(
            label="Download GeoJSON",
            data= geojson.dumps(feature_collection),
            file_name= geojson_filename,
            mime="application/geo+json"
        )

