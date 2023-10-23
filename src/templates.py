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
    <body>
        <h3>Sketch Blend - Please login with this <a href="{{url}}">link</a></h3>
        <img src="https://sketch-blend.isaacdev.net/static/images/email_banner.png" />
        <p>
        Sketch Blend is a demo website offers users the ability to draw sketches, generate new images based on their sketches using Stable Diffusion, and post these images with others.
        </p>
        <span style="opacity: 0"> {{time}} </span>
    </body>
    """
)
