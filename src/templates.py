from pulumi_aws import ses

email_template = ses.Template(
    "email-template",
    name="testing-template",
    subject="{{subject}}",
    html="""
    <h1>You have receive this email, the message is {{message}}</h1>
    """
)
