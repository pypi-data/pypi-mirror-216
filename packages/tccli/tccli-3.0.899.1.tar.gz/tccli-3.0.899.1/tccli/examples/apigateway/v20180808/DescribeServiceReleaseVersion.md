**Example 1: DescribeServiceReleaseVersion**



Input: 

```
tccli apigateway DescribeServiceReleaseVersion --cli-unfold-argument  \
    --ServiceId service-ody35h5e
```

Output: 
```
{
    "Response": {
        "Result": {
            "TotalCount": 5,
            "VersionList": [
                {
                    "VersionName": "202002140201231eee121d-058a-4c0c-a2b1-bc25325d42d5",
                    "VersionDesc": "xxx"
                },
                {
                    "VersionName": "20200214020300d0eab0c5-e124-4705-bc61-81545361cc0d",
                    "VersionDesc": "xxx"
                },
                {
                    "VersionName": "202002140204057f8dbac2-1b0e-4ce5-975e-f1d82618e008",
                    "VersionDesc": "xxx"
                },
                {
                    "VersionName": "20200214020506aac44ade-6657-4c7f-b15a-59fa1e4252e7",
                    "VersionDesc": "xxx"
                },
                {
                    "VersionName": "202002161926124aa59df4-7198-4f7a-acc7-887ab7ee0215",
                    "VersionDesc": "xx"
                }
            ]
        },
        "RequestId": "4d712ae3-9fb7-467b-a3aa-eaa17ada621c"
    }
}
```

