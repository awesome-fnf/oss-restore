# -*- coding: utf-8 -*-
"""
Check oss object whether restore completed
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

    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # Check file restore completed
    resp = bucket.head_object(file_name)
    logger.info('Head object response headers: {}'.format(resp.headers))
    restore_header = 'x-oss-restore'
    if restore_header not in resp.headers:
        # restore request not submit or out of expire date
        status = 'success'
    elif resp.headers[restore_header].find('ongoing-request="false"') != -1:
        status = 'success'
    else:
        status = 'running'

    return '{"status": "%s"}' % status
