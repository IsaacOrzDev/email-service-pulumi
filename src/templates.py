from pulumi_aws import ses

email_template = ses.Template(
    "email-template",
    name="testing-template",
    subject="{{subject}}",
    html="""
    <h1>You have receive this email, the message is {{message}}</h1>
    """
)

sketch_blend_email_template = ses.Template(
    "sketch-blend-login-template",
    name="sketch-blend-login-template",
    subject="{{subject}}",
    html="""
    <h3>Sketch Blend - Please login with this <a href="{{url}}">link</a></h3>
    <img src="https://personal-images.isaacdev.net/sketch_blend_banner.png" />
    """
)
