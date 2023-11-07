from flask import Flask
from flask import render_template
from flask import flash
from flask import request
# Requests limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Entorn vars
from dotenv import dotenv_values
# Boto for aws
import boto3
import os

# S3 resource
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
)

# Entorn vars loading
config = dotenv_values(".env")

# App instance
app = Flask(__name__)
# App secret key
app.secret_key = os.getenv('APP_SECRET_KEY').encode("utf-8")

# Requests Limiter instance
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)
# Requests limiter properties to all endpoints
LIMITER_INT_LIMIT = "100 per hour"
LIMITER_ERROR_MESSAGE = "Please try again later."

#  Google reCaptcha v2 attributes
SITE_KEY = os.getenv("SITE_KEY")
SERVER_KEY = os.getenv("SERVER_KEY")
VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


@app.route('/me-deprecated')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def me_deprecated():
    image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": "frmo-portfolio-pictures",
            "Key": "images/profile_photo.png"
        },
        ExpiresIn=2
    )
    print(image_url)
    return render_template('me-deprecated.html', img_url=image_url)


@app.route('/portfolio')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def portfolio():
    return render_template('portfolio.html')


@app.route('/ai')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def ai():
    return render_template('ai.html')


@app.route('/cloud')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def cloud():
    return render_template('cloud.html')


@app.route('/backend')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def backend():
    return render_template('backend.html')


@app.route('/iiot')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def iiot():
    return render_template('iiot.html')


@app.route('/writing')
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def writing():
    return render_template('writing.html')


@app.route('/dev/test')
def dev():
    return render_template("stack_list.html")


@app.route('/')
def me():
    return render_template('me.html')


@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit(LIMITER_INT_LIMIT, error_message=LIMITER_ERROR_MESSAGE)
def contact():
    if request.method == 'GET':
        return render_template(
            'contact.html',
            siteKey=SITE_KEY,
            reCaptcha=True
        )
    elif request.method == 'POST':
        secretResponse = request.form['g-recaptcha-response']
        print(f"SECRET RESPONSE: {secretResponse}")
        if len(secretResponse) > 0:
            flash('Message was sent successfully.')
            return render_template(
                'contact.html',
                siteKey=SITE_KEY,
                reCaptcha=True
            )
        else:
            return render_template(
                'contact.html',
                siteKey=SITE_KEY,
                reCaptcha=False
            )


if __name__ == "__main__":
    # Ignition
    app.run(host="0.0.0.0", port=8080, debug=False)
