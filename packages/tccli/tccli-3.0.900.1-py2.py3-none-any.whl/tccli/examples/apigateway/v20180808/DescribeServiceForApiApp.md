**Example 1: DescribeServiceForApiApp**



Input: 

```
tccli apigateway DescribeServiceForApiApp --cli-unfold-argument  \
    --ServiceId service-rypiqi13 \
    --ApiRegion ap-guangzhou
```

Output: 
```
{
    "Response": {
        "ServiceDesc": "xx",
        "CreatedTime": "2020-09-22T00:00:00+00:00",
        "SetId": 1,
        "InnerHttpsPort": 0,
        "InnerHttpPort": 0,
        "Tags": [
            {
                "Value": "xx",
                "Key": "xx"
            }
        ],
        "NetTypes": [
            "OUTER"
        ],
        "IpVersion": "xx",
        "UserType": "xx",
        "UsagePlanList": [
            {
                "MaxRequestNumPreSec": 0,
                "UsagePlanId": "xx",
                "ModifiedTime": "2020-09-22T00:00:00+00:00",
                "UsagePlanDesc": "xx",
                "Environment": "xx",
                "CreatedTime": "2020-09-22T00:00:00+00:00",
                "UsagePlanName": "xx"
            }
        ],
        "OuterSubDomain": "xx",
        "UsagePlanTotalCount": 0,
        "ApiIdStatusSet": [
            {
                "AuthType": "xx",
                "Protocol": "xx",
                "UniqVpcId": "xx",
                "ModifiedTime": "2020-09-22T00:00:00+00:00",
                "OauthConfig": {
                    "PublicKey": "xx",
                    "LoginRedirectUrl": "xx",
                    "TokenLocation": "xx"
                },
                "ApiId": "xx",
                "AuthRelationApiId": "xx",
                "ApiDesc": "xx",
                "ApiType": "xx",
                "ApiBusinessType": "xx",
                "ServiceId": "xx",
                "ApiName": "xx",
                "Path": "xx",
                "CreatedTime": "2020-09-22T00:00:00+00:00",
                "RelationBuniessApiIds": [
                    "xx"
                ],
                "IsDebugAfterCharge": false,
                "Method": "xx",
                "TokenLocation": "xx"
            }
        ],
        "ServiceName": "xx",
        "RequestId": "xx",
        "Protocol": "xx",
        "ApiTotalCount": 1,
        "ModifiedTime": "2020-09-22T00:00:00+00:00",
        "ExclusiveSetName": "xx",
        "AvailableEnvironments": [
            "release"
        ],
        "ServiceId": "xx",
        "InternalSubDomain": "xx"
    }
}
```

