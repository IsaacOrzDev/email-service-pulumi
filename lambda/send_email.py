import json
import boto3

ses = boto3.client('ses')


def handler(event, context):
    body_str = event['Records'][0]['body']
    body = json.loads(body_str)
    try:
        if 'template' in body and body['template'] is not None:
            ses.send_templated_email(
                Source=body['from'],
                Destination={'ToAddresses': body['to']},
                Template=body['template'],
                TemplateData=json.dumps(body['data'])
            )
        else:
            email_message: dict = {
                'Subject': {'Data': body['subject']},
                'Body':  {'Html': {'Data': body['content']}}
            }
            ses.send_email(
                Source=body['from'],
                Destination={'ToAddresses': body['to']},
                Message=email_message
            )
        print('Email sent successfully: ' + body_str)
    except ses.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
        raise e
    except Exception as e:
        print(e)
        raise e
