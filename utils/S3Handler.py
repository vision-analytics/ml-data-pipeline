import boto3
import json

from config.Config import Config

class S3Handler:
    def __init__(self):

        self.config = Config()

        self.session = boto3.Session(
            aws_access_key_id = self.config.AWS_ACCESS_KEY_ID, 
            aws_secret_access_key = self.config.AWS_SECRET_ACCESS_KEY, 
            region_name = self.config.AWS_REGION_NAME
            )

        self.BUCKET = self.config.AWS_BUCKET_NAME
        self.AWS_OUT_DIR = self.config.AWS_OUT_DIR

        self.s3 = self.session.resource('s3')
        
        
    def upload_file(self, file_path, upload_path):
        self.s3.meta.client.upload_file(Filename=file_path, Bucket=self.BUCKET, Key=upload_path)

    def write_json_to_s3_file(self, json_data, upload_path):
        s3object = self.s3.Object(self.BUCKET, upload_path)

        s3object.put(
            Body=(bytes(json.dumps(json_data).encode('UTF-8')))
        )

    def list_dir(self, run_id):
        bucket = self.s3.Bucket(name=self.BUCKET)

        prefix = self.AWS_OUT_DIR + '/' + run_id

        return bucket.objects.filter(Prefix=prefix)
