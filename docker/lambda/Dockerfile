# https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html
FROM public.ecr.aws/lambda/python:3.9

RUN yum update -y \
    && yum install -y amazon-linux-extras \
    && ln -s /usr/lib/python2.7/site-packages/amazon_linux_extras /var/lang/lib/python3.9/site-packages/ \
    && amazon-linux-extras install -y epel \
    && yum install -y chromium

# Copy function code
COPY kot ${LAMBDA_TASK_ROOT}/kot

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "kot.service.lambda_handler" ]
