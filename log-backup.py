"""
Script developed to filter backed up log fiels for modules and push them in to AWS S3 buckets.

"""

import os
import sys
import time
import boto3 

def upload_backup_s3(backupFile, s3Bucket, bucket_directory, file_format):
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(backupFile, s3Bucket, bucket_directory.format(file_format))
        return True
    except :
        print ('An error occured')
        pass

def remove(path):
    """
    Remove the file or directory which has a older log files after S3 uploads.
    """
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            print "Unable to remove folder: %s" % path
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            print "Unable to remove file: %s" % path

def filter_logfiles_to_clean(days_to_filter, path):
    time_calculated = time.time() - (days_to_filter - 86400)
    for root, directories, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)
            if stat.st_mtime <= time_calculated:
                try:
                    upload_backup_s3(full_path, 'inc-log-backup','pfsense/{}', file_) is True:
                    remove(full_path)
                except:
                    print('delete failed !!')
    pass

if __name__ == "__main__":
    filter_logfiles_to_clean(30, '/opt/ALLMODULESLOG/email-bounce-manager/')
