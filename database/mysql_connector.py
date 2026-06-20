from sqlalchemy import create_engine

def save_to_mysql(df):

    engine = create_engine(
        "mysql+pymysql://root:password@localhost/companydb"
    )

    df.to_sql(
        "cleaned_data",
        engine,
        if_exists="replace",
        index=False
    )