# -*- coding: utf-8 -*-
"""
Restore oss object
"""
import oss2
import json
import logging


logger = logging.getLogger()


def handler(event, context):
    logger.info('Receive event: {}'.format(event))

    # Read params
    data = json.loads(event)
    endpoint = data['endpoint']
    bucket_name = data['bucketName']
    file_name = data['fileName']

    # Use sts auth, restore oss file
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    logger.info('Send restore request for bucket: {}, file: {}'.format(bucket_name, file_name))
    resp = bucket.restore_object(file_name)
    logger.info('Restore response: {}'.format(resp))

    return '{}'
