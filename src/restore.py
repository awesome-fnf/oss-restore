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
    markers = data['markerTuples']
    prefix = data.get('prefix', '')
    max_keys = data.get('maxKeys', 100)
    start_marker = markers[0]
    end_marker = markers[1]

    # Use sts auth, restore oss file
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    files_to_dealt = []
    end_file = end_marker
    mkr = start_marker
    if end_file == "":
        # list to end
        is_truncated = True
        while is_truncated:
            resp = bucket.list_objects(prefix=prefix, marker=mkr)
            is_truncated = resp.is_truncated
            for obj in resp.object_list:
                if obj.storage_class == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
                    end_file = obj.key
            mkr = resp.next_marker

    ended = False
    while not ended:
        resp = bucket.list_objects(prefix=prefix, marker=start_marker, max_keys=max_keys)

        for obj in resp.object_list:
            if obj.storage_class == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
                files_to_dealt.append(obj.key)
                if end_file == obj.key:
                    ended = True
                    break
        start_marker = resp.next_marker

    for file in files_to_dealt:
        resp = bucket.restore_object(file)
        logger.info('Restore file: {}'.format(file))

    return '{}'
