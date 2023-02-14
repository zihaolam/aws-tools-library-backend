import boto3
from botocore.exceptions import ClientError


class Email:
    AWS_REGION = "ap-southeast-1"

    def __init__(self):
        self.sender = "noreply <noreply@lean.social>"
        self.client = boto3.client("ses", region_name=self.AWS_REGION)
        self.client = boto3.client("ses", region_name=self.AWS_REGION)

    def send_email(self, recipient: str, subject: str, body: str, type: str = "Html"):
        try:
            # Provide the contents of the email.
            response = self.client.send_email(
                Destination={
                    "ToAddresses": [
                        recipient,
                    ],
                },
                Message={
                    "Body": {
                        type: {
                            "Charset": "UTF-8",
                            "Data": body,
                        }
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": subject,
                    },
                },
                Source=self.sender,
            )

        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])


email = Email()
