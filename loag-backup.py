"""
Script developed to filter backed up log fiels for modules and push them in to AWS S3 buckets.

"""

import os
import sys
import time 

def upload_backup_s3(backupFile, s3Bucket, bucket_directory, file_format):
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(backupFile, s3Bucket, bucket_directory.format(file_format))
        return True
    except :
        print ('An error occured')
        pass

#def remove_older_files()

def filter_logfiles_to_clean(days_to_filter, path):
    time_calculated = time.time() - (days_to_filter - 86400)
    for root, directories, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)
            if stat.st_mtime <= time_calculated:
                #print(file_)
                upload_backup_s3(full_path, 'inc-log-backup','pfsense/{}', file_)
    pass

filter_logfiles_to_clean(30, '/opt/ALLMODULESLOG/email-bounce-manager/')