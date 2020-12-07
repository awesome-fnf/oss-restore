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
    marker_list = data['markerList']
    bucket_name = data['bucketName']
    dest_bucket_name = data['destBucketName']
    prefix = data.get('prefix', '')

    start_marker = marker_list[0][0]
    end_marker = marker_list[-1][-1]

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
        resp = bucket.list_objects(prefix=prefix, marker=start_marker)

        for obj in resp.object_list:
            if obj.storage_class == oss2.BUCKET_STORAGE_CLASS_ARCHIVE:
                files_to_dealt.append(obj.key)
                if end_file == obj.key:
                    ended = True
                    break
        start_marker = resp.next_marker


    # Check file restore completed
    status = 'success'
    for file_name in files_to_dealt:
        resp = bucket.head_object(file_name)
        logger.info('Head object response headers: {}'.format(resp.headers))
        restore_header = 'x-oss-restore'
        if restore_header not in resp.headers:
            # restore request not submit or out of expire date
            status = 'success'
            # put object
            bucket.copy_object(bucket_name, file_name, dest_bucket_name)
            logger.error('Restore file: {} not submit. Please rerun'.format(file_name))
        elif resp.headers[restore_header].find('ongoing-request="false"') != -1:
            status = 'success'
            # put object
            bucket.copy_object(bucket_name, file_name, dest_bucket_name)
            logger.info('Restore file: {} finished, now put to {}'.format(file_name, dest_bucket_name))
        else:
            status = 'running'
            logger.info('Restore file: {} running'.format(file_name))
            break

    return '{"status": "%s"}' % status
