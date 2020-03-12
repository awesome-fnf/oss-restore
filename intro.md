## 应用简介
使用 Serverless Workflow 和函数计算 FC 来并发的批量解冻 oss 文件。

## 调用示例
1. 选择 `解冻 OSS 文件` 模板创建应用
![](https://img.alicdn.com/tfs/TB1BKDBxVY7gK0jSZKzXXaikpXa-2770-1186.png)

2. 跳转到创建应用页面，部署应用
![](https://img.alicdn.com/tfs/TB15U6Ex1L2gK0jSZFmXXc7iXXa-2740-1274.png)

3. 等待应用创建成功
![](https://img.alicdn.com/tfs/TB1RevBx8v0gK0jSZKbXXbK2FXa-2708-1268.png)

4. 执行应用

    输入：
    ```json
    {
      "endpoint": "",
      "bucketName": "",
      "prefix": "",
      "maxKeys": 100
    }
    ```
    参数说明：
    - endpoint: OSS endpoint
    - bucketName: OSS bucket 名称
    - prefix: (可选) OSS bucket 文件过滤前缀
    - maxKeys: (可选) OSS ListObjects 最大数量 (这里不要超过 Workflow foreach 的并发，默认是 100)
  
   ![](https://img.alicdn.com/tfs/TB1sg_Cx9f2gK0jSZFPXXXsopXa-2714-1270.png)
   
## 工作原理
1. `mainRestoreFlow` 任务步骤调用函数 `listArchiveFiles` 获取从 OSS `marker` 开始的文件列表。
2. `mainRestoreFlow` 调用 `restoreFlow` 对获取到的文件列表进行解冻。
3. `restoreFlow` 并行循环 (foreach) 步骤并行的为列表中每个文件启动解冻任务。
4. `restoreFlow` 中任务步骤调用函数 `restore` 对文件进行解冻。
5. `restoreFlow` 中任务步骤调用函数 `restoreStatus` 以循环 poll 的方式检测文件解冻是否完成。
6. 循环执行步骤 1 - 5，直到所有文件都列举完毕。

![](https://img.alicdn.com/tfs/TB1bb_Fx4D1gK0jSZFKXXcJrVXa-1394-658.png)

## 链接
1. [应用代码](https://github.com/awesome-fnf/oss-restore)