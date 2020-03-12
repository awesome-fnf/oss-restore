## Description
Use Serverless Workflow concurrent and batch restore OSS files.

## How to use
1. Choose `OSS Restore` template
![](https://img.alicdn.com/tfs/TB1SyPJx8r0gK0jSZFnXXbRRXXa-2736-1276.png)

2. Jump to create application
![](https://img.alicdn.com/tfs/TB15U6Ex1L2gK0jSZFmXXc7iXXa-2740-1274.png)

3. Wait for application created success
![](https://img.alicdn.com/tfs/TB1RevBx8v0gK0jSZKbXXbK2FXa-2708-1268.png)

4. Run StartExecution for `mainRestoreFlow`

    Input：
    ```json
    {
      "endpoint": "",
      "bucketName": "",
      "prefix": "",
      "maxKeys": 100
    }
    ```
    Parameters：
    - endpoint: OSS endpoint
    - bucketName: OSS bucket name
    - prefix: (optional) OSS bucket prefix
    - maxKeys: (optional) OSS ListObjects maxKeys (Don't exceed Workflow foreach number limit，default 100)
  
   ![](https://img.alicdn.com/tfs/TB1sg_Cx9f2gK0jSZFPXXXsopXa-2714-1270.png)
   
## Framework
1. `mainRestoreFlow` invoke function `listArchiveFiles`, get OSS archive files start with `marker`.
2. `mainRestoreFlow` invoke subflow `restoreFlow` to restore all files.
3. `restoreFlow` foreach step start a restore task for each file in file list.
4. `restoreFlow` restore task invoke function `restore` to restore file.

![](https://img.alicdn.com/tfs/TB1bb_Fx4D1gK0jSZFKXXcJrVXa-1394-658.png)

## Reference
1. [Application Code](https://github.com/awesome-fnf/oss-restore)

