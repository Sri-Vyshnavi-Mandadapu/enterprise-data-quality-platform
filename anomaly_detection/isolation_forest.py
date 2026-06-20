from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        return df

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    predictions = model.fit_predict(numeric_df)

    df["Anomaly"] = predictions

    return df