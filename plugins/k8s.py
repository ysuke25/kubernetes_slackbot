import datetime
import json
import os
import re
import subprocess

from kubernetes import client, config
from slackbot.bot import listen_to
from slackbot.bot import respond_to

# mention to me
@listen_to(".*alertname.*")
def mention_to_me(message):

    color = "warning"
    
    attachments = [{
        'text': "<!channel> アラートが発生しました",
        'color': color,
        'mrkdwn_in': [
            'text'
        ]
    }]
    message.reply_webapi('', json.dumps(attachments))

# kubectlコマンドを実行する
@respond_to(r'^kubectl (.*)')
def mention_kubectl(message, kubectl_args):
    try:
        cmd = 'kubectl {}'.format(kubectl_args)
        completed_process = subprocess.run(cmd.split(),
                                           check=True,
                                           capture_output=True)
        result_str = completed_process.stdout.decode('utf-8') + completed_process.stderr.decode('utf-8')
        color = 'good'

    except subprocess.CalledProcessError as e:
        result_str = e.stdout.decode('utf-8') + e.stderr.decode('utf-8')
        color = 'warning'

    msg = '```\n{}```'.format(result_str)

    attachments = [{
        'text': msg,
        'color': color,
        'mrkdwn_in': [
            'text'
        ]
    }]
    message.reply_webapi('', json.dumps(attachments))


# Pod削除
@respond_to('(.*)の(.*)(削除|削除して|消して)')
def menthon_pod(message, arg1, arg2, arg3):
    # Kubernetes上で動いているかを環境変数から判断する
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        # ServiceAccountの権限で実行する
        config.load_incluster_config()
    else:
        # $HOME/.kube/config から読み込む
        config.load_kube_config()

    name = arg2
    namespace = arg1

    v1 = client.CoreV1Api()
    respons = v1.delete_namespaced_pod(name, namespace)

    attachments = [{
        'text': respons,
        'color': "good",
        'ts': datetime.datetime.now().strftime('%s')
    }]
    message.send_webapi('', json.dumps(attachments))
