def validate_data(df):

    validation_results = []

    if "Age" in df.columns:

        invalid_age = df[
            (df["Age"] < 0) |
            (df["Age"] > 100)
        ]

        validation_results.append(
            f"Invalid Age Records: {len(invalid_age)}"
        )

    if "Salary" in df.columns:

        invalid_salary = df[
            df["Salary"] < 0
        ]

        validation_results.append(
            f"Invalid Salary Records: {len(invalid_salary)}"
        )

    return validation_results