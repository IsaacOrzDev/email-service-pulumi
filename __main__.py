"""A Python Pulumi program"""

import pulumi
from pulumi_aws import sns, sqs, iam, lambda_, iam
import src.templates

sns_topic = sns.Topic("email-topic")

sqs_queue = sqs.Queue("email-queue")

sqs_policy = sqs.QueuePolicy("email-queue-policy", queue_url=sqs_queue.id, policy="""{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "*"
    }
  ]
}""")

sns_subscription = sns.TopicSubscription(
    "email-topic-subscription",
    topic=sns_topic.arn,
    protocol="sqs",
    endpoint=sqs_queue.arn,
    raw_message_delivery=True
)

lambda_role = iam.Role(
    'lambdaRole',
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Effect": "Allow",
            "Sid": ""
        }]
    }"""
)

attach_lambda_execute_policy = iam.RolePolicyAttachment(
    'lambda-execute-policy-attachment',
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSLambdaExecute"
)

lambda_function = lambda_.Function(
    "email-trigger-lambda",
    role=lambda_role.arn,
    runtime="python3.10",
    handler="send_email.handler",
    code=pulumi.AssetArchive({
        '.': pulumi.FileArchive('./lambda')
    }))

lambda_permission = lambda_.Permission(
    'lambdaPermission',
    action='lambda:InvokeFunction',
    function=lambda_function.name,
    principal='sqs.amazonaws.com',
    source_arn=sqs_queue.arn
)

policy = iam.RolePolicy(
    "email-lambda-policy",
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
                "Resource": "*"
            }, {
              "Effect": "Allow",
              "Action": ["ses:SendEmail", "ses:SendRawEmail", "ses:SendTemplatedEmail"],
              "Resource": ["*"]
            }
        ]
    }""",
    role=lambda_role.name
)


mapping = lambda_.EventSourceMapping(
    "email-trigger-mapping",
    event_source_arn=sqs_queue.arn,
    function_name=lambda_function.arn
)


publish_to_sns_policy = iam.get_policy_document(statements=[
    iam.GetPolicyDocumentStatementArgs(
        actions=["sns:Publish"],
        resources=[sns_topic.arn],
    ),
])

iam_user = iam.User('publish-message-iam-user')

user_keys = iam.AccessKey('iam-user-key', user=iam_user.name)

# Create the IAM Policy with the defined document
iam_policy = iam.Policy('allow-sns-publish-policy',
                        policy=publish_to_sns_policy.json)

# Attach the policy to the user
policy_attachment = iam.UserPolicyAttachment('user-policy-attachment',
                                             user=iam_user.name,
                                             policy_arn=iam_policy.arn)

pulumi.export('accessKeyID', user_keys.id)
pulumi.export('secretAccessKey', user_keys.secret)
