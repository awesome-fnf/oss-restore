## Description
Use Serverless Workflow concurrent and batch restore OSS files.

## How to use
<video width="100%" height="500"  controls autoplay="autoplay" src="https://dev-fc-application-template-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/oss-restore/media/oss-restore-en.mov"></video>

Parameters：
- endpoint: OSS endpoint
- bucketName: OSS bucket name
- prefix: (optional) OSS bucket prefix
- maxKeys: (optional) OSS ListObjects maxKeys (Don't exceed Workflow foreach number limit，default 100)
- pollInterval: (optional) Poll OSS restore status interval in seconds
   
## Framework
1. `mainRestoreFlow` invoke function `listArchiveFiles`, get OSS archive files start with `marker`.
2. `mainRestoreFlow` invoke subflow `restoreFlow` to restore all files.
3. `restoreFlow` foreach step start a restore task for each file in file list.
4. `restoreFlow` restore task invoke function `restore` to restore file.

![](https://img.alicdn.com/tfs/TB1bb_Fx4D1gK0jSZFKXXcJrVXa-1394-658.png)

## Reference
1. [Application Code](https://github.com/awesome-fnf/oss-restore)

