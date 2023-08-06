import clipboard
import re
import boto3
import awswrangler as wr
import pandas as pd
from io import BytesIO

class AWSHandler:
    def __init__(self, profile_name='default', region_name='us-east-1', use_sagemaker_role=False):
        if use_sagemaker_role:
            self.session = boto3.session.Session()
            print(f"Successfully initialized SageMaker Credentials")
        else:
            self.parse_clipboard_credentials()            
            self.session = boto3.session.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                region_name=region_name
            )      
            print(f"Successfully initialized credentials for {self.profile_name.split('_')[1]}")
            
        self.glue_client = self.session.client("glue", region_name=region_name)        
        self.s3 = self.session.client('s3')
            
        
    def parse_clipboard_credentials(self):
        content = clipboard.paste()
        pattern = r'\[(.+)\]\naws_access_key_id=(.+)\naws_secret_access_key=(.+)\naws_session_token=(.+)'
        match = re.search(pattern, content)

        if match:
            self.profile_name = match.group(1)
            self.aws_access_key_id = match.group(2)
            self.aws_secret_access_key = match.group(3)
            self.aws_session_token = match.group(4)

            # Clear the clipboard after parsing the credentials
            clipboard.copy('')
        else:
            raise ValueError("No AWS credentials found in the clipboard.")
            
    def query(self, sql: str, database: str):
        return wr.athena.read_sql_query(sql=sql, database=database, boto3_session=self.session)

    def list_tables(self, database: str) -> dict:
        tables = []
        views = []

        paginator = self.glue_client.get_paginator("get_tables")
        for page in paginator.paginate(DatabaseName=database):
            for table in page["TableList"]:
                if table["TableType"] == "VIRTUAL_VIEW":
                    views.append(table["Name"])
                else:
                    tables.append(table["Name"])
        return {"tables": tables, "views": views}
    
    def list_data_sources(self) -> list:             
        databases = []
        paginator = self.glue_client.get_paginator("get_databases")
        for page in paginator.paginate():
            databases.extend([db["Name"] for db in page["DatabaseList"]])
        return databases

    def save_df(self, df, bucket_name, key):
        file_format = key.split('.')[-1] if '.' in key else ''
        buffer = BytesIO()
        if file_format == 'parquet':
            df.to_parquet(buffer, engine='pyarrow')
        elif file_format == 'csv':
            df.to_csv(buffer, index=False)
        else:
            raise ValueError(f"Invalid file_format: {file_format}. Please use 'parquet' or 'csv'.")
        buffer.seek(0)
        self.s3.upload_fileobj(buffer, bucket_name, key)

    def load_df(self, bucket_name, key):
        file_format = key.split('.')[-1] if '.' in key else ''
        buffer = BytesIO()
        self.s3.download_fileobj(bucket_name, key, buffer)
        buffer.seek(0)
        if file_format == 'parquet':
            return pd.read_parquet(buffer, engine='pyarrow')
        elif file_format == 'csv':
            return pd.read_csv(buffer)
        else:
            raise ValueError(f"Invalid file_format: {file_format}. Please use 'parquet' or 'csv'.")

    def list_all_buckets(self):
        try:
            response = self.s3.list_buckets()
            print("You have access to the following buckets:")
            for bucket in response['Buckets']:
                print(f"{bucket['Name']}")
        except Exception as e:
            print("Error listing buckets:", e)

    def list_bucket(self, bucket_name, folder_prefix=''):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
            print(f"Objects in folder '{folder_prefix}' in bucket '{bucket_name}':")
            for content in response.get('Contents', []):
                print(f"{content['Key']}")
        except Exception as e:
            print("Error listing objects in folder:", e)