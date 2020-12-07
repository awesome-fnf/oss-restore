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
    batches = data.get('batches', 100)

    # Sts
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # list achieve files
    achieve_list = []
    markers_list = []
    is_truncated = True
    while (len(markers_list) < batches) and is_truncated:
        resp = bucket.list_objects(prefix=prefix, marker=marker, max_keys=max_keys)
        is_truncated = resp.is_truncated
        tuples = (marker, resp.next_marker)
        markers_list.append(tuples)
        for obj in resp.object_list:
            if obj.storage_class == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
                achieve_list.append(obj.key)
        marker = resp.next_marker
    next_flow_begin_marker = marker

    empty = False
    if len(markers_list) == 0:
        empty = True
    # Capsule all data into json and return
    res = {
        'bucketName': bucket_name,      # bucket name
        'marker': next_flow_begin_marker,     # next maker for list object
        'markerList': markers_list,  # next maker for list object
        'empty': empty,
        'end': not is_truncated,   # whether all objects been listed
    }
    return json.dumps(res)

