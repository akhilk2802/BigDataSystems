from utils.logging_module import log_success, log_error
from sqlalchemy import create_engine
import pandas as pd


def df_to_sql(dataframe_path: str, schema: str, table_name: str, db_config: dict):
    try:
        # Load the DataFrame from file
        dataframe = pd.read_csv(dataframe_path)
        log_success(f"Loaded DataFrame from {dataframe_path}.")

        # Create SQLAlchemy engine
        conn_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = create_engine(conn_string)
        log_success("Created SQLAlchemy engine.")

        # Log DataFrame preview
        log_success(f"DataFrame preview: {dataframe.head()}")

        
        # Write DataFrame to SQL table
        dataframe.to_sql(
        schema=schema,
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False
        )

        
        log_success(f"Data successfully loaded into {schema}.{table_name} table.")
    except Exception as e:
        log_error(f"Failed to load DataFrame to SQL: {e}")
        raise