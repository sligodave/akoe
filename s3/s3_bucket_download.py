

from os.path import join, abspath, exists, dirname
from os import unlink, makedirs
import boto


def download_to_path(dst_path,
                access_key,
                secret_access_key,
                bucket_name,
                src_path='',
                overwrite=False):
    # Get the bucket to copy from
    conn = boto.connect_s3(access_key, secret_access_key)
    bucket = conn.get_bucket(bucket_name)
    dst_path = abspath(dst_path)
    keylist = bucket.list(prefix=src_path)
    for key in keylist:
        dst_file_path = join(dst_path, key.name)
        dst_directory_path = dirname(dst_file_path)
        if exists(dst_file_path):
            if not overwrite:
                continue
            else:
                unlink(dst_file_path)
        elif not exists(dst_directory_path):
            makedirs(dst_directory_path)
        key.get_contents_to_filename(dst_file_path)


if __name__ == "__main__":
    from sys import argv
    # Path to download to
    dst_path = argv[1]
    # AWS Access key
    access_key = argv[2]
    # AWS Secret Access Key
    secret_access_key = argv[3]
    # AWS Bucket Name
    bucket_name = argv[4]
    # AWS Source Path in Bucket
    src_path = '' if len(argv) <= 5 else argv[5]
    # Whether we overwrite items that already exist in destination
    overwrite = True if len(argv) <= 6 else\
                    {'True': True, 'False': False}[argv[6].title()]

    download_to_path(dst_path,
                      access_key,
                      secret_access_key,
                      bucket_name,
                      src_path,
                      overwrite)