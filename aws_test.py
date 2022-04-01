import boto3  # pip install boto3

# Let's use Amazon S3
s3 = boto3.resource("s3")

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# Create an S3 access object
s3 = boto3.client("s3")
s3.download_file(
    Bucket="pydatabucket", Key="screenshot.png", Filename="data/screenshot.png"
)
s3.upload_file(
    Filename="data/full_eo_list_actual.csv",
    Bucket="pydatabucket",
    Key="full_eo_list_actual.csv",
)



