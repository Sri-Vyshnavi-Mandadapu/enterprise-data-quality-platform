import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from scipy import stats
from fpdf import FPDF

from anomaly_detection.isolation_forest import detect_anomalies
from validation.validator import validate_data

st.set_page_config(
    page_title="Enterprise Data Quality Platform",
    layout="wide"
)

st.title("Enterprise Data Quality & Reporting Platform")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Dataset")
    st.dataframe(df)

    # Missing Values

    missing_values = df.isnull().sum().sum()

    st.metric(
        "Missing Values",
        missing_values
    )

    # Duplicates

    duplicate_rows = df.duplicated().sum()

    st.metric(
        "Duplicate Rows",
        duplicate_rows
    )

    # Cleaning

    cleaned_df = df.copy()

    cleaned_df.drop_duplicates(
        inplace=True
    )

    for col in cleaned_df.columns:

        if cleaned_df[col].dtype != "object":

            cleaned_df[col].fillna(
                cleaned_df[col].median(),
                inplace=True
            )

        else:

            cleaned_df[col].fillna(
                "Unknown",
                inplace=True
            )

    # Quality Score

    total_cells = (
        cleaned_df.shape[0] *
        cleaned_df.shape[1]
    )

    remaining_missing = (
        cleaned_df.isnull().sum().sum()
    )

    quality_score = (
        (1 - remaining_missing / total_cells)
        * 100
    )

    st.metric(
        "Quality Score",
        f"{quality_score:.2f}%"
    )

    # Validation

    st.subheader("Validation Results")

    results = validate_data(
        cleaned_df
    )

    for item in results:

        st.write(item)

    # Anomaly Detection

    cleaned_df = detect_anomalies(
        cleaned_df
    )

    anomalies = cleaned_df[
        cleaned_df["Anomaly"] == -1
    ]

    st.subheader("Detected Anomalies")

    st.dataframe(anomalies)

    # Correlation

    numeric_df = cleaned_df.select_dtypes(
        include=np.number
    )

    if not numeric_df.empty:

        corr = numeric_df.corr()

        fig = px.imshow(
            corr,
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Export Excel

    excel_file = "reports/cleaned_data.xlsx"

    cleaned_df.to_excel(
        excel_file,
        index=False
    )

    with open(excel_file, "rb") as f:

        st.download_button(
            "Download Cleaned Excel",
            f,
            file_name="cleaned_data.xlsx"
        )

    # PDF Report

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.cell(
        200,
        10,
        txt="Data Quality Report",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Quality Score: {quality_score:.2f}%",
        ln=True
    )

    pdf_file = "reports/quality_report.pdf"

    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:

        st.download_button(
            "Download PDF Report",
            f,
            file_name="quality_report.pdf"
        )