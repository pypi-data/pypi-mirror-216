#/usr/bin/env python
__author__ = 'Sujit Mandal'
#Date :25-06-2023
import os
import boto3

def upload_file(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, FILE_OBJ, FILE_NAME):
    s3 = boto3.client('s3',
                aws_access_key_id=AWS_ACCESS_KYE,
                aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                )

    s3.upload_file(FILE_OBJ, BUCKET_NAME, FILE_NAME)

   
    s3bucket = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KYE,
                aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                )
    bucket = s3bucket.Bucket(BUCKET_NAME)
   
    upload_file_info = []
    for obj in bucket.objects.filter(Prefix=FILE_NAME):
      upload_file_bucket_name = obj.bucket_name
      upload_file_name = obj.key
      upload_file_info.append(upload_file_bucket_name)
      upload_file_info.append(upload_file_name)

    status = {}
    if BUCKET_NAME in upload_file_info and FILE_NAME in upload_file_info:
       status['status'] = True
       status['message'] = 'File uploaded successfully.'

    else:
        status['status'] = False
        status['message'] = 'Error in uploading file.'

    
    return(status)

    
def download_file(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, S3_FILE_NAME, FILE_NAME):
    s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KYE,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                    )
  
    s3bucket = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KYE,
                aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                )
    bucket = s3bucket.Bucket(BUCKET_NAME)

    upload_file_info = []
    for obj in bucket.objects.filter(Prefix=S3_FILE_NAME):
      upload_file_bucket_name = obj.bucket_name
      upload_file_name = obj.key
      upload_file_info.append(upload_file_bucket_name)
      upload_file_info.append(upload_file_name)

    status = {}
    if BUCKET_NAME in upload_file_info and S3_FILE_NAME in upload_file_info:
        with open(FILE_NAME, 'wb') as f:
            s3.download_fileobj(BUCKET_NAME, S3_FILE_NAME, f)
            f.seek(0)

    if os.path.exists(FILE_NAME):
        status['status'] = True
        status['message'] = 'File download successfully.'
     
    else:
        status['status'] = False
        status['message'] = 'File not found.'
       
    return(status)


def get_all_file_list(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE):
    s3bucket = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KYE,
                aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                )
    bucket = s3bucket.Bucket(BUCKET_NAME)

    upload_file_info = []
    for obj in bucket.objects.all():
      bucket_name = obj.bucket_name
      file_name = obj.key
      
      upload_file_info.append([bucket_name, file_name])

    file_name_dict = {}
    if len(upload_file_info) != 0:
      file_name_dict_list = []
      for file_name_list in upload_file_info:
        tmp_dict = {}
        tmp_dict['bucket_name'] = file_name_list[0]
        tmp_dict['file_name'] = file_name_list[1]

        file_name_dict_list.append(tmp_dict)
      
      file_name_dict['status'] = True
      file_name_dict['data'] = file_name_dict_list
    else:
      file_name_dict['status'] = False
      file_name_dict['message'] = 'File not found.'


    return(file_name_dict)

def check_file_status(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, S3_FILE_NAME):
    s3bucket = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KYE,
                aws_secret_access_key=AWS_SECRET_ACCESS_KYE
                )
    bucket = s3bucket.Bucket(BUCKET_NAME)

    upload_file_info = []
    for obj in bucket.objects.filter(Prefix=S3_FILE_NAME):
      upload_file_bucket_name = obj.bucket_name
      upload_file_name = obj.key
      upload_file_info.append(upload_file_bucket_name)
      upload_file_info.append(upload_file_name)


    status = {}
    if len(upload_file_info) != 0:
      status['status'] = True
      status['data'] = 'File available.'
    else:
      status['status'] = False
      status['message'] = 'File not found.'

    return(status)


if __name__ == '__main__':
  FILE_OBJ = ""
  FILE_NAME = ""
  S3_FILE_NAME = ""
  BUCKET_NAME = ""
  AWS_ACCESS_KYE = ""
  AWS_SECRET_ACCESS_KYE = ""

  get_all_file_list(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE)
  check_file_status(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, S3_FILE_NAME)
  download_file(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, S3_FILE_NAME, FILE_NAME)
  upload_file(BUCKET_NAME, AWS_ACCESS_KYE, AWS_SECRET_ACCESS_KYE, FILE_OBJ, FILE_NAME)