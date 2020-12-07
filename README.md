## Description
Use Serverless Workflow concurrent and batch restore OSS files.

## How to use
<video width="100%" height="500"  controls autoplay="autoplay" src="https://dev-fc-application-template-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/oss-restore/media/oss-restore-en.mov"></video>

Parameters：
- endpoint: OSS endpoint
- bucketName: OSS bucket name
- destBucketName: OSS bucket name, restore files will be put in this bucket
- prefix: (optional) OSS bucket prefix
- marker: (optional) OSS file marker to be started
- pollInterval: (optional) Poll OSS restore status interval in seconds
- maxKeys: (optional) OSS ListObjects maxKeys (the file number per function dealt with)
- batches: (optional) Max batches dealt per round, do not over 100(batches is the number of the subflow foreach fc tasks) 

In one round, batches * maxKeys files will be restore.
   
eg:
{
  "endpoint": "oss-cn-beijing.aliyuncs.com",
  "bucketName": "oss-restore",
  "destBucketName": "oss-restore-dest",
  "prefix":"",
  "pollInterval": 10,
  "marker": "",
  "maxKeys": 3,
  "batches": 5
}
 
## Framework
1. `mainRestoreFlow` invoke function `listArchiveFiles`, get OSS archive files start with `marker`.
2. `mainRestoreFlow` invoke subflow `restoreFlow` to restore all files.
3. `restoreFlow` foreach step start a restore task for each file in file list.
4. `restoreFlow` restore task invoke function `restore` to restore file.

![](https://img.alicdn.com/tfs/TB1bb_Fx4D1gK0jSZFKXXcJrVXa-1394-658.png)

## Reference
1. [Application Code](https://github.com/awesome-fnf/oss-restore)

