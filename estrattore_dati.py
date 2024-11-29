import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO

def parse_xml_to_dataframe(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    data = []
    for item in root.findall(".//ItemNode"):
        row = {
            "Item": item.get("Item"),
            "Category": item.get("Category"),
            "Reference": item.get("Reference"),
            "Qty": item.get("Qty"),
            "UnitId": item.get("UnitId"),
            "Date": item.get("Date"),
            "InventSiteId": item.get("InventSiteId"),
            "InventLocationId": item.get("InventLocationId"),
            "wMSLocationId": item.get("wMSLocationId"),
            "InventStatusId": item.get("InventStatusId"),
            "LicensePlateId": item.get("LicensePlateId"),
            "inventBatchId": item.get("inventBatchId"),
        }
        data.append(row)
    return pd.DataFrame(data)

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dati Estratti")
    processed_data = output.getvalue()
    return processed_data

# Interfaccia Streamlit
st.title("Estrattore Dati da XML a Excel")
st.write("Carica un file XML contenente dati strutturati e genera un file Excel con i dati estratti.")

uploaded_file = st.file_uploader("Carica il file XML", type="xml")

if uploaded_file is not None:
    # Legge il contenuto del file XML
    xml_content = uploaded_file.read()
    
    # Parsing del contenuto XML
    st.write("Sto analizzando il file...")
    df = parse_xml_to_dataframe(xml_content)
    
    # Mostra l'anteprima dei dati
    st.write("Anteprima dei dati estratti:")
    st.dataframe(df)
    
    # Converti in Excel
    excel_file = convert_df_to_excel(df)
    
    # Download del file Excel
    st.download_button(
        label="Scarica il file Excel",
        data=excel_file,
        file_name="dati_estratti.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
