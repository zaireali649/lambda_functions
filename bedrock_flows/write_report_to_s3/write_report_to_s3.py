import json, time
import boto3
from urllib.parse import urlparse

s3 = boto3.client("s3")

def handler(event, _):
    """
    event = {
      "report_json": {...},
      "s3_uri": "s3://bucket/feedback/raw/YYYY-MM-DD/file.jsonl"
    }
    returns { "report_s3_uri": "s3://bucket/feedback/reports/YYYY-MM-DD/summary.json" }
    """
    report = event["report_json"]
    src = event["s3_uri"]
    u = urlparse(src)
    # Use today's date for output folder
    date_prefix = time.strftime("%Y-%m-%d")
    out_key = f"feedback/reports/{date_prefix}/summary.json"
    s3.put_object(
        Bucket=u.netloc,
        Key=out_key,
        Body=json.dumps(report, indent=2).encode("utf-8"),
        ContentType="application/json"
    )
    return {"report_s3_uri": f"s3://{u.netloc}/{out_key}"}
