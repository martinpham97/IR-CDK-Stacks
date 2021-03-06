import json
import boto3
import urllib3
import os

iam = boto3.client('iam')
sns = boto3.client('sns')

clwDenyPolicyName1 = 'ClWDenyAccess1'
clwDenyPolicyName2 = 'ClWDenyAccess2'
clwGroupName = os.environ["white_list_group"]

notificationTopic='CDKCLWAccess'
http = urllib3.PoolManager()


def hasValidGroup(userName):
    response = iam.get_group(GroupName=clwGroupName)

    groupUsernames = []

    for user in response['Users']:
        groupUsernames.append(user['UserName'])


    if userName in groupUsernames:
        return True
    else:
        return False


def hasDenyPolicy(userName):
    inline_user_policies = iam.list_attached_user_policies(UserName=userName)['AttachedPolicies']

    print('Check Deny Policy')

    found = False
    for policy in inline_user_policies:
        if policy['PolicyName'] == clwDenyPolicyName1 or policy['PolicyName'] == clwDenyPolicyName2:
            found = True
            break

    return found


def sendNotification(message):
    print('sending notification')

    all_sns_topics = sns.list_topics()
    for topic in all_sns_topics['Topics']:
        if notificationTopic in topic['TopicArn']:
            notificationTopicArn = topic['TopicArn']

    response = sns.publish(
        TopicArn=notificationTopicArn,
        Message=message,
        Subject='Access to CloudWatch',
        MessageStructure='string'
    )



def sendSlackNotification(message):
    message = "IN-CLW-01 Unauthorised CloudWatch Access:\n" + message
    webhook_url = os.environ["webhook_url"]

    slack_message = {"channel": "ir-cdk-stacks", "text": message}
    encoded_data = json.dumps(slack_message).encode("utf-8")
    response = http.request(
        "POST",
        webhook_url,
        body=encoded_data,
        headers={"Content-Type": "application/json"},
    )


def lambda_handler(event, context):
    userName = event['detail']['userIdentity']['userName']
    userType = event['detail']['userIdentity']['type']
    sourceIPAddress = event["detail"]['sourceIPAddress']
    eventTime = event["detail"]["eventTime"]
    userAgent = event["detail"]["userAgent"]
    eventName = event["detail"]["eventName"]
    message = f'IN_CLW_01: {userName} tried to perform {eventName} on Cloudwatch at time {eventTime} from userAgent {userAgent} with IP {sourceIPAddress}. '

    validUser = hasValidGroup(userName)

    if hasDenyPolicy(userName):

        message = message + ' CloudWatchDeny Policy is already attached to deny access to CloudWatch.'
        sendNotification(message)

    else:
        if userType == "IAMUser" and not validUser:

            all_policies = iam.list_policies()
            for _policy in all_policies['Policies']:
                if _policy['PolicyName'] == clwDenyPolicyName1:
                    policyArn1 = _policy['Arn']
                if _policy['PolicyName'] == clwDenyPolicyName2:
                    policyArn2 = _policy['Arn']

            response = iam.attach_user_policy(UserName=userName, PolicyArn=policyArn1)
            response = iam.attach_user_policy(UserName=userName, PolicyArn=policyArn2)

            message = message + ' CloudWatchDeny Policy attached to deny access to CloudWatch.'
            sendNotification(message)

        else:

            message = message + ' Access Granted : CloudWatch Access allowed.'
            sendNotification(message)
            sendSlackNotification(message)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from CloudWatch Lambda!')
    }
