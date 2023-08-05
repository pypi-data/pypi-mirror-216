import postgres_client.utils
import psycopg2
import logging
import os

logger = logging.getLogger(__name__)

class PostgresClient:
    def __init__(
        self,
        dsn=None,
        host=None,
        port=None,
        dbname=None,
        user=None,
        password=None,
    ):
        # For each of the connection parameters, give precedence to (1)
        # Parameters explicitly specified to the constructor, and then (2)
        # Wildflower-specific environment variables, before (3) passing to
        # PostgresSQL defaults(see https://www.psycopg.org/docs/module.html and
        # https://www.postgresql.org/docs/current/libpq-envars.html for the
        # latter)
        self.dsn = dsn 
        self.host = host or os.getenv('WF_PGHOST')
        self.port = port or os.getenv('WF_PGPORT')
        self.dbname = dbname or os.getenv('WF_PGDATABASE')
        self.user = user or os.getenv('WF_PGUSER')
        self.password = password or os.getenv('WF_PGPASSWORD')
    
    def connect(self):
        connection = psycopg2.connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )
        return connection

    def execute(
        self,
        sql_object,
        parameters=None,
        connection=None,
    ):
        existing_connection = True if connection is not None else False
        if not existing_connection:
            connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute(sql_object, parameters)
            description = cursor.description
            try:
                data_list = cursor.fetchall()
            except:
                data_list = None
        if not existing_connection:
            connection.commit()
            connection.close()
        return data_list, description

    def executemany(
        self,
        sql_object,
        parameters_list,
        connection=None,
    ):
        existing_connection = True if connection is not None else False
        if not existing_connection:
            connection = self.connect()
        with connection.cursor() as cursor:
            cursor.executemany(sql_object, parameters_list)
        if not existing_connection:
            connection.commit()
            connection.close()
    
    def select(
        self,
        table,
        schema=None,
        fields=None,
        query_list=None,
        connection=None,
        convert_to_dataframe=True
    ):
        sql_object, parameters = postgres_client.utils.compose_select_sql(
            table=table,
            schema=schema,
            fields=fields,
            query_list=query_list,
        )
        data_list, description = self.execute(
            sql_object=sql_object,
            parameters=parameters,
            connection=connection,
        )
        if convert_to_dataframe:
            dataframe = postgres_client.utils.convert_to_dataframe(
                data_list=data_list,
                description=description
            )
            return dataframe
        else:
            return data_list, description
