from sys import argv

import boto
from boto.s3.key import Key

ACCESS_KEY = argv[1]
SECRET_ACCESS_KEY = argv[2]
BUCKET_NAME = argv[3]
SOURCE_PATH = argv[4]
DESTINATION_PATH = argv[5]

conn = boto.connect_s3(ACCESS_KEY,
                       SECRET_ACCESS_KEY)
bucket = conn.get_bucket(BUCKET_NAME)

print 'Uploading "%s" to "%s" in "%s"' % (SOURCE_PATH, DESTINATION_PATH, BUCKET_NAME)
k = Key(bucket, DESTINATION_PATH)
k.set_contents_from_filename(SOURCE_PATH, policy='public-read')
print 'Uploaded'
