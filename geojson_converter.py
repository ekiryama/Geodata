import streamlit as st
import pandas as pd
import geojson
from shapely import wkt
from shapely.geometry import mapping
import re

st.title("Conversion of CSV to GeoJson")

st.subheader("Upload the CSV")
uploaded_file = st.file_uploader("Choose a csv file", type="csv")

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
    df= pd.read_csv(uploaded_file)

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
            properties={
                "ProducerName": row["ProducerName"],
                "Area": row["Area"],
                "ProducerCountry": row["ProducerCountry"],
                "ProductionPlace": row["ProductionPlace"],
                "EUDR compliance": row["EUDR compliance"]
            }
        )
        
        # Append the feature to the list of features
        features.append(feature)

    # Create a GeoJSON FeatureCollection
    feature_collection = geojson.FeatureCollection(features)

    # # Save the FeatureCollection to a GeoJSON file
    # with open('MyOutput.geojson', 'w') as f:
    #     geojson.dump(feature_collection, f)

    st.download_button(
        label="Download GeoJSON",
        data= geojson.dumps(feature_collection),
        file_name="converted_GeoJson.geojson",
        mime="application/geo+json"
    )
    # print("GeoJSON file has been created successfully.")
