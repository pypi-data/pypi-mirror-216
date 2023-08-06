import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 腾讯云 COS 配置
BUCKET_NAME = os.environ.get("BUCKET_NAME")
COS_REGION = os.environ.get("COS_REGION", "ap-beijing")
COS_SECRET_ID = os.environ.get("COS_SECRET_ID")
COS_SECRET_KEY = os.environ.get("COS_SECRET_KEY")


def get_cos_url(key):
    token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
    scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Token=token,
        Scheme=scheme,
    )
    client = CosS3Client(config)

    # 生成URL
    url = client.get_object_url(Bucket=BUCKET_NAME, Key=key)
    return url


def upload_file(key, file_path):
    token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
    scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Token=token,
        Scheme=scheme,
    )
    client = CosS3Client(config)

    # 上传文件
    response = client.upload_file(
        Bucket=BUCKET_NAME,
        LocalFilePath=file_path,
        Key=key,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False,
    )
    return response["ETag"]
