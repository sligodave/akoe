import boto
from boto.s3.key import Key


def upload_file(ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME, SOURCE, DESTINATION):
    conn = boto.connect_s3(ACCESS_KEY, SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)

    k = Key(bucket, DESTINATION)
    print 'Uploading "%s" to "%s" in "%s"' % (SOURCE, DESTINATION, BUCKET_NAME)
    k.set_contents_from_filename(SOURCE, policy='public-read')
    print 'Uploaded'


if __name__ == "__main__":
    from sys import argv
    ACCESS_KEY = argv[1]
    SECRET_ACCESS_KEY = argv[2]
    BUCKET_NAME = argv[3]
    SOURCE = argv[4]
    DESTINATION = argv[5]
    upload_file(ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME, SOURCE, DESTINATION)
