import logging
import pandas as pd
import numpy as np
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError, NoSuchTableError
from sqlalchemy.dialects.mysql import LONGTEXT, DOUBLE, VARCHAR
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine, exc, MetaData, Table, Column, Integer, text, \
    String, DateTime, func, inspect, Numeric, Float, Text, Boolean, Date, Time, \
    LargeBinary, DDL, event
from sqlalchemy.dialects.mysql import MEDIUMTEXT, LONGTEXT

logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, db_string, echo=False):
        """
        Initialize a DatabaseHandler instance to interact with the database.

        Supported databases and connection string formats:
        - MySQL: 'mysql+pymysql://user:password@localhost/dbname'
        - PostgreSQL: 'postgresql://user:password@localhost/dbname'
        - SQLite: 'sqlite:///your_database.db'

        For Oracle and Microsoft SQL Server, manual database creation is recommended.

        :param db_string: A database connection string.
        :param echo: Whether to enable echo mode.
        """
        self.engine = create_engine(db_string, echo=echo)
        self.metadata = MetaData()
        self.db_name = db_string.split('/')[-1]  # Extract the database name from the connection string
        self.setup_db()

    def get_engine(self):
        """
        Returns the SQLAlchemy engine instance.
        """
        return self.engine

    def connect_db(self):
        """
        Establishes a connection to the database and returns the connection object.
        """
        return self.engine.connect()

    def setup_db(self):
        """
        Sets up the database. Creates it if it does not exist.
        """
        try:
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
                logger.info(f"Database '{self.db_name}' created.")
            else:
                logger.info(f"Database '{self.db_name}' already exists.")
        except exc.SQLAlchemyError as e:
            logger.error(f"Error setting up database: {e}")

    def setup_table(self, table_name, columns_spec=None):
        """
        Sets up a table with specified columns, if it doesn't exist.

        :param table_name: The name of the table to create or verify.
        :param columns_spec: Optional; A list of strings or a dictionary with column names and types.
        """
        if not inspect(self.engine).has_table(table_name):
            if columns_spec is None:
                raise NoSuchTableError(f"Table '{table_name}' does not exist. Provide column specifications to create.")
            self._create_table(table_name, columns_spec)
        else:
            logger.info(f"Table '{table_name}' already exists.")

    def create_table(self, table_name, columns_spec):
        """
        Creates a new table with the specified columns, if it doesn't exist.

        :param table_name: The name of the table to create.
        :param columns_spec: A list of strings or a dictionary with column names and types.
        """
        if not inspect(self.engine).has_table(table_name):
            self._create_table(table_name, columns_spec)
        else:
            logger.warning(f"Table '{table_name}' already exists and will not be recreated.")

    def _create_table(self, table_name, columns_spec):
        """
        Helper method to create a table with the given columns.

        ...
        TODO: Some data types may not be correctly recognized by SQLAlchemy. Optimization needed.
        For tables with unrecognized types, consider manual or raw SQL creation.
        ...

        :param table_name: The name of the table to create.
        :param columns_spec: A list of strings or a dictionary representing the column names or specifications.
                             If a list is provided, all columns are created as String type with a default length.
                             If a dictionary is provided, create columns with specified types and properties.

                             The dictionary format for columns_spec should be:
                             {
                                 'ColumnName': {'type': SQLAlchemyType, 'length': length, ...},
                                 # Example for a string column with max length 50
                                 'ID': {'type': String, 'length': 50},
                                 # Example for a numeric column with precision and scale
                                 'FpTm': {'type': Numeric, 'precision': 10, 'scale': 2},
                                 # Example for an integer column
                                 'RpSize': {'type': Integer},
                                 # Example for a text column
                                 'Note': {'type': Text},
                                 # ... other columns ...
                             }


        """
        autoinc_column = self._autoinc_col(columns_spec)
        columns = [Column(autoinc_column, Integer, primary_key=True, autoincrement=True)]

        if isinstance(columns_spec, list):
            # If a list is provided, all columns are created as String type with a default length
            columns += [Column(name, String(255)) for name in columns_spec]
        elif isinstance(columns_spec, dict):
            # If a dictionary is provided, create columns with specified types and properties
            for name, spec in columns_spec.items():
                col_type = spec.get('type', String)
                if issubclass(col_type, String):
                    col_length = spec.get('length', 255)
                    columns.append(Column(name, col_type(col_length)))
                elif col_type in [Integer, Float, Numeric, Text, LONGTEXT, DateTime]:
                    columns.append(Column(name, col_type))
                else:
                    raise ValueError(f"Unrecognized or unsupported column type for column '{name}'.")
        else:
            raise ValueError("columns_spec must be a list or a dictionary")

        # columns += [
        #     Column('CreatedAt', DateTime, default=func.now()),
        #     Column('UpdatedAt', DateTime, default=func.now(), onupdate=func.now())
        # ]
        created_at = Column('CreatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'))
        updated_at = Column('UpdatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'))

        table = Table(table_name, self.metadata, *columns, created_at, updated_at)

        # Add DDL listening events to set ON UPDATE constraints
        on_update_ddl = DDL(
            f"ALTER TABLE {table_name} MODIFY `UpdatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        event.listen(table, 'after_create', on_update_ddl)

        self.metadata.create_all(bind=self.engine)
        logger.info(
            f"Table '{table_name}' created with columns {', '.join(columns_spec if isinstance(columns_spec, list) else columns_spec.keys())}.")

    @staticmethod
    def _autoinc_col(columns_spec):
        """
        Determines the auto-increment column name.

        :param columns_spec: A list or dictionary representing the column names or specifications.
        :return: The name for the auto-incrementing primary key column.
        """
        if isinstance(columns_spec, dict):
            # Check the keys of the dictionary for 'id' or 'ID'
            return 'auto_id' if 'id' in columns_spec.keys() or 'ID' in columns_spec.keys() else 'id'
        elif isinstance(columns_spec, list):
            # Check the list for 'id' or 'ID'
            return 'auto_id' if 'id' in columns_spec or 'ID' in columns_spec else 'id'
        else:
            raise ValueError("columns_spec must be a list or a dictionary")

    def create_df_table(self, table_name, df):
        """
        Creates a table based on a DataFrame schema.

        ...
        TODO: Some data types may not be correctly recognized by SQLAlchemy. Optimization needed.
        For tables with unrecognized types, consider manual or raw SQL creation.
        ...

        :param table_name: The name of the table to create.
        :param df: DataFrame with schema for table creation.
        """
        if not inspect(self.engine).has_table(table_name):
            autoinc_column_name = self._autoinc_col(df.columns.to_list())
            columns = [Column(autoinc_column_name, Integer, primary_key=True, autoincrement=True)]

            for col_name in df.columns:
                if col_name not in [autoinc_column_name]:
                    col_type = self._map_dtype(df, col_name)
                    columns.append(Column(col_name, col_type))

            # 1. Using SQLAlchemy's func.now() for default and onupdate.
            #    Limitation: Depends on SQLAlchemy to correctly translate func.now() for all database dialects.
            #    Example: Column('CreatedAt', DateTime, default=func.now())

            # columns.append(Column('CreatedAt', DateTime, default=func.now()))
            # columns.append(Column('UpdatedAt', DateTime, default=func.now(), onupdate=func.now()))

            # 2. Using text('CURRENT_TIMESTAMP') as server_default and onupdate.
            #    It's a direct SQL expression that corresponds to the database's CURRENT_TIMESTAMP function.
            #    Still relies on SQLAlchemy to properly translate onupdate parameter into the appropriate SQL.
            #    Example: Column('UpdatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

            # columns.append(Column('CreatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP')))
            # columns.append(Column('UpdatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'),
            #                       onupdate=text('CURRENT_TIMESTAMP')))

            # 3. Using DDL to add an ALTER TABLE statement directly at the database level after table creation.
            #    This method doesn't depend on SQLAlchemy's translation of the onupdate parameter,
            #    as it executes an SQL command directly in the database to set the ON UPDATE rule.
            #    Example:
            #    on_update_ddl = DDL("ALTER TABLE tablename MODIFY UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            #    event.listen(table, 'after_create', on_update_ddl)

            created_at = Column('CreatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'))
            updated_at = Column('UpdatedAt', DateTime, server_default=text('CURRENT_TIMESTAMP'))

            table = Table(table_name, self.metadata, *columns, created_at, updated_at)

            # Add DDL listening events to set ON UPDATE constraints
            on_update_ddl = DDL(
                f"ALTER TABLE {table_name} MODIFY `UpdatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            event.listen(table, 'after_create', on_update_ddl)

            self.metadata.create_all(bind=self.engine)
            logger.info(f"Created table '{table_name}' from DataFrame schema.")
        else:
            logger.info(f"Table '{table_name}' already exists.")

    @staticmethod
    def _map_dtype(df, col_name):
        """
        Maps a pandas dtype to a SQLAlchemy type.

        :param dtype: Pandas data type.
        :return: SQLAlchemy column type.
        """
        dtype = df[col_name].dtype
        max_length = df[col_name].apply(lambda x: len(str(x)) if x is not None else 0).max()

        if pd.api.types.is_integer_dtype(dtype):
            return Integer
        elif pd.api.types.is_float_dtype(dtype):
            return Float
        elif pd.api.types.is_object_dtype(dtype):
            # Object dtype usually means string, but could be anything.
            # May require manual inspection and adjustment.
            # Dynamically sets the type of column based on the maximum length
            if max_length <= 255:
                return String(255)
            elif max_length <= 65535:
                return Text
            elif max_length <= 16777215:
                return MEDIUMTEXT
            else:
                return LongText
        elif pd.api.types.is_bool_dtype(dtype):
            return Boolean
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return DateTime
        elif pd.api.types.is_timedelta64_dtype(dtype):
            # SQLAlchemy doesn't have a direct equivalent for timedeltas
            # They are usually stored as integers or strings in databases
            return String(255)
        elif pd.api.types.is_categorical_dtype(dtype):
            # Categoricals are often converted to strings, but could also be mapped to integers
            return String(255)
        elif pd.api.types.is_date_dtype(dtype):
            return Date
        elif pd.api.types.is_time_dtype(dtype):
            return Time
        elif pd.api.types.is_complex_dtype(dtype):
            # There's no direct equivalent for complex numbers in SQL
            # They might be stored as strings or split into two float columns for real and imaginary parts
            return String(255)
        elif pd.api.types.is_bytes_dtype(dtype):
            # For binary data, use LargeBinary or BLOB
            return LargeBinary
        # Add mappings for other specific pandas dtypes if necessary
        else:
            # As a fallback, use Text type which can hold arbitrary length strings
            return Text

    def insert_df(self, table_name, df, if_exists='append'):
        """
        Inserts a DataFrame into the specified database table.

        :param table_name: The name of the database table.
        :param df: The DataFrame to be inserted.
        :param if_exists: Action to take when the table already exists. Defaults to 'append'.
                         Other options: 'fail', 'replace'.
        """
        df = df.copy()
        record_count = df.shape[0]

        if 'CreatedAt' in df.columns:
            del df['CreatedAt']
            logger.info("Deleted 'CreatedAt' column from DataFrame.")
        if 'UpdatedAt' in df.columns:
            del df['UpdatedAt']
            logger.info("Deleted 'UpdatedAt' column from DataFrame.")

        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
        logger.info(f"Inserted {record_count} records into '{table_name}' table successfully.")

    def insert_data(self, table_name, data, ignore_unmatched=False):
        """
        Inserts data into the specified table.

        :param table_name: The name of the table where data will be inserted.
        :param data: Data to be inserted. Can be a pandas DataFrame or a list of dictionaries.
                    For a DataFrame, columns should match the table's column names.
                    For a list of dictionaries, each dictionary represents a row with keys as column names.
        :param ignore_unmatched: If True, drop columns from DataFrame that are not in the database table.
                                 If False, raise an error if there are unmatched columns.

        Examples:
            Using a pandas DataFrame:
                data_df = pd.DataFrame({'column1': [1, 2], 'column2': ['A', 'B']})
                db_handler.insert_data('your_table_name', data_df)

            Using a list of dictionaries:
                data_list = [{'column1': 1, 'column2': 'A'}, {'column1': 2, 'column2': 'B'}]
                db_handler.insert_data('your_table_name', data_list)
        """
        try:
            # Get column definitions from the database table
            inspector = inspect(self.engine)
            columns_info = [col for col in inspector.get_columns(table_name)]
            pk_constraint = inspector.get_pk_constraint(table_name)
            primary_keys = set(pk_constraint['constrained_columns'])

            # Dynamically create columns and set the primary_key parameter based on whether the primary key is the primary key
            table_columns = [
                Column(col['name'], col['type'], primary_key=(col['name'] in primary_keys))
                for col in columns_info
            ]

            # Use extend_existing to fit into existing table definitions
            table = Table(table_name, self.metadata, *table_columns, extend_existing=True)

            # Replace NaN values with None and prepare data for insertion
            if isinstance(data, pd.DataFrame):
                data = data.replace({np.nan: None})
                df_column_names = set(data.columns)
                db_column_names = {col['name'] for col in columns_info}
                unmatched_columns = df_column_names - db_column_names
                if unmatched_columns:
                    if ignore_unmatched:
                        logger.warning(f"Dropping columns not found in the database table: {unmatched_columns}")
                        data = data.drop(columns=unmatched_columns, errors='ignore')
                    else:
                        raise ValueError(f"Columns not found in the database table: {unmatched_columns}")
                data_dicts = data.to_dict(orient='records')
            elif isinstance(data, list) and all(isinstance(row, dict) for row in data):
                data_dicts = data
            else:
                raise ValueError("Data must be a pandas DataFrame or a list of dictionaries.")

            # Insert data row by row
            with self.engine.connect() as conn:
                transaction = conn.begin()  # Start a new transaction
                for row in data_dicts:
                    conn.execute(table.insert().values(**row))
                transaction.commit()  # Explicitly commit a transaction
            logger.info(f"Inserted {len(data_dicts)} records into table '{table_name}'.")

        except Exception as e:
            logger.error(f"Error inserting data into '{table_name}': {e}")
            raise

    def execute_query(self, query):
        """
        Executes a raw SQL query and returns the result as a DataFrame.

        :param query: The SQL query to execute.
        :return: A DataFrame containing the result of the query execution.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return result

    def query_df(self, query, exclude_timestamps=True):
        """
        Executes a SQL query and returns a DataFrame.

        :param query: SQL query string.
        :param exclude_timestamps: Whether to exclude 'CreatedAt' and 'UpdatedAt' columns. Default is True.
        :return: DataFrame with query results.
        """
        df = pd.read_sql(query, self.engine)
        if exclude_timestamps:
            return df.drop(columns=['CreatedAt', 'UpdatedAt'], errors='ignore')
        return df
