# https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html
FROM public.ecr.aws/lambda/python:3.10

ENV POETRY_HOME=/etc/poetry
ENV PATH $POETRY_HOME/bin:$PATH
ENV GOOGLE_CHROME_VERSION 114.0.5735.90-1

RUN yum update -y \
  && yum install -y amazon-linux-extras curl \
  && ln -s /usr/lib/python2.7/site-packages/amazon_linux_extras /var/lang/lib/python3.10/site-packages/ \
  && amazon-linux-extras install -y epel \
  && yum install -y https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-${GOOGLE_CHROME_VERSION}.x86_64.rpm \
  && yum clean all

# Install the function's dependencies using file requirements.txt
# from pyproject.toml with poetry export.
COPY pyproject.toml poetry.lock ./
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && poetry export -f requirements.txt --output requirements.txt \
  && curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN python -m pip install --upgrade pip \
  && pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY kot ${LAMBDA_TASK_ROOT}/kot

# Turn off webdriver-manager logs use
# ENV WDM_LOG 0
# Set cache for the latest driver
# RUN python -m kot initialize

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "kot.service.lambda_handler" ]
