FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN wget -q https://storage.googleapis.com/kubernetes-release/release/$(wget https://storage.googleapis.com/kubernetes-release/release/stable.txt -O -)/bin/linux/amd64/kubectl \
  && mv kubectl /usr/local/bin/kubectl \
  && chmod +x /usr/local/bin/kubectl

RUN wget https://github.com/openshift/okd/releases/download/4.6.0-0.okd-2021-01-23-132511/openshift-client-linux-4.6.0-0.okd-2021-01-23-132511.tar.gz \
    && tar -zxvf openshift-client-linux-4.6.0-0.okd-2021-01-23-132511.tar.gz \
    && mv oc /usr/local/bin/oc \
    && chmod +x /usr/local/bin/oc

COPY run.py slackbot_settings.py ./
COPY ./plugins ./plugins

ENTRYPOINT [ "python", "./run.py" ]
