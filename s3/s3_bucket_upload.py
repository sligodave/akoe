
from os import listdir
from os.path import isdir, isfile, abspath, join, split

import boto
from boto.s3.key import Key


def upload_path_to_s3(path,
                access_key,
                secret_access_key,
                bucket_name,
                include_root=True,
                overwrite=False):
    conn = boto.connect_s3(access_key, secret_access_key)
    bucket = conn.get_bucket(bucket_name)
    handle_path(path, path, bucket, include_root, overwrite)


def handle_path(path, base_path, bucket, include_root=True, overwrite=False):
    if isdir(path):
        handle_folder(path, base_path, bucket, include_root, overwrite)
    elif isfile(path):
        handle_file(path, base_path, bucket, include_root, overwrite)


def handle_folder(path, base_path, bucket, include_root=True, overwrite=False):
    for item in listdir(path):
        path2 = join(path, item)
        handle_path(path2, base_path, bucket, include_root, overwrite)


def handle_file(path, base_path, bucket, include_root=True, overwrite=False):
    base_path = abspath(base_path)
    path = abspath(path)
    filename = path[len(base_path):]
    if filename.startswith('/'):
        filename = filename[1:]
    if include_root:
        base_upload_path = split(base_path)[1]
        if base_upload_path.endswith('/'):
            base_upload_path = base_upload_path[1:]
        filename = base_upload_path + '/' + filename
    k = Key(bucket, filename)
    if overwrite == False and k.exists():
        print 'Exists "%s"' % filename
        return
    print 'Uploading "%s"' % filename
    k.set_contents_from_filename(path, policy='public-read')


if __name__ == "__main__":
    from sys import argv
    # Path to upload
    path = argv[1]
    # AWS Access key
    access_key = argv[2]
    # AWS Secret Access Key
    secret_access_key = argv[3]
    # AWS Bucket Name
    bucket_name = argv[4]
    # Whether we include the root folder name in the uploaded filename
    include_root = True if len(argv) <= 5 else\
                    {'True': True, 'False': False}[argv[5]]
    # Whether we overwrite items that already exist in the bucket
    overwrite = True if len(argv) <= 6 else\
                    {'True': True, 'False': False}[argv[6]]

    upload_path_to_s3(path,
                      access_key,
                      secret_access_key,
                      bucket_name,
                      include_root,
                      overwrite)
