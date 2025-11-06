import json, gzip
import boto3
from urllib.parse import urlparse

s3 = boto3.client("s3")
MAX_RECORDS = 200  # keep demo predictable

def handler(event, _):
    """
    event = { "s3_uri": "s3://bucket/path/file.jsonl[.gz]" }
    returns { "feedback_items": [ {...}, ... ] }
    """
    s3_uri = event["s3_uri"]
    u = urlparse(s3_uri)
    obj = s3.get_object(Bucket=u.netloc, Key=u.path.lstrip("/"))
    body = obj["Body"].read()
    if u.path.endswith(".gz"):
        body = gzip.decompress(body)

    items = []
    for line in body.decode("utf-8").splitlines():
        if line.strip():
            items.append(json.loads(line))
            if len(items) >= MAX_RECORDS:
                break
    return {"feedback_items": items}
