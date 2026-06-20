import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF

from anomaly_detection.isolation_forest import detect_anomalies
from validation.validator import validate_data

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise Data Quality Platform",
    layout="wide"
)

st.title("📊 Enterprise Data Quality & Reporting Platform")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Raw Dataset")
    st.dataframe(df)

    # --------------------------------------------------
    # DATA QUALITY METRICS
    # --------------------------------------------------

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Missing Values", int(missing_values))

    with col2:
        st.metric("Duplicate Rows", int(duplicate_rows))

    # --------------------------------------------------
    # DATA CLEANING
    # --------------------------------------------------

    cleaned_df = df.copy()

    # Remove duplicates
    cleaned_df = cleaned_df.drop_duplicates()

    # Fill missing values
    for col in cleaned_df.columns:

        if pd.api.types.is_numeric_dtype(cleaned_df[col]):
            median_value = cleaned_df[col].median()
            cleaned_df[col] = cleaned_df[col].fillna(median_value)

        else:
            cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    # --------------------------------------------------
    # QUALITY SCORE
    # --------------------------------------------------

    total_cells = cleaned_df.shape[0] * cleaned_df.shape[1]
    remaining_missing = cleaned_df.isnull().sum().sum()

    quality_score = (
        (1 - remaining_missing / total_cells) * 100
        if total_cells > 0 else 0
    )

    st.metric(
        "Quality Score",
        f"{quality_score:.2f}%"
    )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    st.subheader("✅ Validation Results")

    validation_results = validate_data(cleaned_df)

    for result in validation_results:
        st.write(result)

    # --------------------------------------------------
    # ANOMALY DETECTION
    # --------------------------------------------------

    st.subheader("🚨 Anomaly Detection")

    cleaned_df = detect_anomalies(cleaned_df)

    anomalies = cleaned_df[
        cleaned_df["Anomaly"] == -1
    ]

    if len(anomalies) > 0:
        st.warning(
            f"{len(anomalies)} anomaly records detected"
        )
        st.dataframe(anomalies)

    else:
        st.success("No anomalies detected")

    # --------------------------------------------------
    # CLEANED DATA
    # --------------------------------------------------

    st.subheader("🧹 Cleaned Dataset")
    st.dataframe(cleaned_df)

    # --------------------------------------------------
    # CORRELATION HEATMAP
    # --------------------------------------------------

    numeric_df = cleaned_df.select_dtypes(
        include=np.number
    )

    if not numeric_df.empty:

        st.subheader("📈 Correlation Heatmap")

        correlation_matrix = numeric_df.corr()

        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------
    # DATA DISTRIBUTION
    # --------------------------------------------------

    numeric_columns = cleaned_df.select_dtypes(
        include=np.number
    ).columns

    if len(numeric_columns) > 0:

        st.subheader(
            "📊 Numeric Column Distribution"
        )

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        histogram = px.histogram(
            cleaned_df,
            x=selected_column,
            nbins=20,
            title=f"{selected_column} Distribution"
        )

        st.plotly_chart(
            histogram,
            use_container_width=True
        )

    # --------------------------------------------------
    # EXPORT FILES
    # --------------------------------------------------

    os.makedirs(
        "reports",
        exist_ok=True
    )

    # Excel Export

    excel_file = "reports/cleaned_data.xlsx"

    cleaned_df.to_excel(
        excel_file,
        index=False
    )

    with open(excel_file, "rb") as file:

        st.download_button(
            label="⬇ Download Cleaned Excel",
            data=file,
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # --------------------------------------------------
    # PDF REPORT
    # --------------------------------------------------

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        size=12
    )

    pdf.cell(
        200,
        10,
        txt="Enterprise Data Quality Report",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Quality Score: {quality_score:.2f}%",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Missing Values: {missing_values}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Duplicate Rows: {duplicate_rows}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Anomalies Detected: {len(anomalies)}",
        ln=True
    )

    pdf_file = "reports/quality_report.pdf"

    pdf.output(pdf_file)

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="⬇ Download PDF Report",
            data=file,
            file_name="quality_report.pdf",
            mime="application/pdf"
        )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    st.success(
        "Data Quality Analysis Completed Successfully ✅"
    )
