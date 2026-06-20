from sqlalchemy import create_engine

def save_to_postgres(df):

    engine = create_engine(
        "postgresql://postgres:password@localhost/companydb"
    )

    df.to_sql(
        "cleaned_data",
        engine,
        if_exists="replace",
        index=False
    )