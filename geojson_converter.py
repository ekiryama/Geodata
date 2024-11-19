import streamlit as st
import pandas as pd
import geojson
from shapely import wkt
from shapely.geometry import mapping

st.title("Conversion of CSV to GeoJson")

st.subheader("Upload the CSV")
uploaded_file = st.file_uploader("Choose a csv file", type="csv")

if uploaded_file is not None:
    df= pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())
    features = []

    # Loop through each row in the DataFrame to create GeoJSON features
    for _, row in df.iterrows():
        # Convert the WKT geometry to a shapely object
        geometry = wkt.loads(row['Plot WKT'])
        
        # Create a GeoJSON feature with properties and geometry
        feature = geojson.Feature(
            geometry=mapping(geometry),
            properties={
                "Sucafina_Plot_ID": row["Sucafina Plot ID"],
                "Plot_area_ha": row["Plot area (ha)"],
                "Country": row["Country"],
                "Region": row["Region"],
                "Recommended compliance": row["Recommended compliance"]
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
