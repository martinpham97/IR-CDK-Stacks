import regex
from PyInquirer import Validator, ValidationError
from prompt_toolkit.document import Document


class AwsAuroraClusterNameValidator(Validator):
    def validate(self, document: Document) -> None:
        # Regular expression for validating an AWS Aurora Cluster name
        # Constraints:
        # Can only contain letters, numbers and hyphens
        # 1 to 60 alphanumeric characters or hyphens.
        # First character must be a letter.
        # Can't contain two consecutive hyphens.
        # Can't end with a hyphen.
        cluster_name_regex = r"(?!.*(--).*)^[a-zA-Z][a-zA-Z0-9\-]{0,59}(?<!-)$"
        ok = regex.match(cluster_name_regex, document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid Aurora Cluster name",
                cursor_position=len(document.text),
            )


class EmailValidator(Validator):
    def validate(self, document: Document) -> None:
        # Regular expression for validating an Email format
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        ok = regex.match(email_regex, document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid email", cursor_position=len(document.text)
            )


class SlackWebhookValidator(Validator):
    def validate(self, document: Document) -> None:
        # Regular expression for validating a Slack Webhook URL
        webhook_regex = r"^https:\/\/hooks\.slack\.com\/services\/T[0-9A-Z]+\/B[0-9A-Z]+\/[0-9A-Za-z]+$"
        ok = regex.match(webhook_regex, document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid Slack Webhook URL",
                cursor_position=len(document.text),
            )


class AwsAccountIdValidator(Validator):
    def validate(self, document: Document) -> None:
        # Regular expression for validating an AWS Account ID
        aws_id_regex = r"^[0-9]{12}$"
        ok = regex.match(aws_id_regex, document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid AWS Account ID",
                cursor_position=len(document.text),
            )


class ApiArnValidator(Validator):
    def validate(self, document):
        # Regular expression for validating an AWS Account ID
        aws_id_regex = "^arn:.*:(apigateway|elasticloadbalancing):.*$"
        ok = regex.match(aws_id_regex, document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid AWS API gateway or Elastic Load Balancer ARN",
            )


class AwsRegionValidator(Validator):
    def validate(self, document):
        # Regular expression for validating an AWS region
        aws_regions = [
            "us-east-2",
            "us-east-1",
            "us-west-1",
            "us-west-2",
            "ap-east-1",
            "ap-south-1",
            "ap-northeast-3",
            "ap-northeast-2",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "ca-central-1",
            "eu-central-1",
            "eu-west-1",
            "eu-west-2",
            "eu-west-3",
            "eu-north-1",
            "me-south-1",
            "sa-east-1",
        ]
        ok = document.text in aws_regions
        if not ok:
            raise ValidationError(
                message="Please enter a valid AWS Region",
                cursor_position=len(document.text),
            )


class RateValidator(Validator):
    def validate(self, document):
        if document.text.isdigit():
            if int(document.text) < 100 or int(document.text) > 20000000:
                raise ValidationError(
                    message="Please enter an integer rate between 100 and 20000000 inclusive",
                    cursor_position=len(document.text),
                )
        else:
            raise ValidationError(
                message="Please enter an integer rate between 100 and 20000000 inclusive",
            )


class YesOrNoValidator(Validator):
    def validate(self, document):
        if not (document.text == 'y' or document.text == 'no'):
            raise ValidationError(
                message="Please enter y or n",
            )
