# -*- coding: utf-8 -*-
"""
List oss objects in bucket begin with marker
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
    marker = data.get('marker', '')
    prefix = data.get('prefix', '')
    max_keys = data.get('maxKeys', 100)

    # Sts
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # list achieve files
    achieve_list = []
    resp = bucket.list_objects(prefix=prefix, marker=marker, max_keys=max_keys)
    for obj in resp.object_list:
        if obj.storage_class == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
            achieve_list.append(obj.key)

    # Capsule all data into json and return
    res = {
        'bucketName': bucket_name,      # bucket name
        'files': achieve_list,          # achieve file list
        'marker': resp.next_marker,     # next maker for list object
        'end': not resp.is_truncated,   # whether all objects been listed
    }
    return json.dumps(res)

