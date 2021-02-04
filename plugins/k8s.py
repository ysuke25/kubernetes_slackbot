import datetime
import json
import os
import re
import subprocess

from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client import configuration 
from slackbot.bot import listen_to
from slackbot.bot import respond_to

# mention to me
'''
@listen_to(".*")
def mention_to_me(message):

    color = "warning"
    msg = '```\n{}```'.format(list(message.body))
    
    attachments = [{
        'text': msg,
        'color': color,
        'mrkdwn_in': [
            'text'
        ]
    }]
    message.send_webapi('', json.dumps(attachments))
'''
#oc コマンドの実行
@respond_to(r'^oc (.*)')
def mention_kubectl(message, kubectl_args):
    try:
        cmd = 'oc {}'.format(kubectl_args)
        completed_process = subprocess.run(cmd.split(),
                                           check=True,
                                           capture_output=True)
        result_str = completed_process.stdout.decode('utf-8') + completed_process.stderr.decode('utf-8')
        color = 'good'

    except subprocess.CalledProcessError as e:
        result_str = e.stdout.decode('utf-8') + e.stderr.decode('utf-8')
        color = 'warning'

    msg = '```\n{}```'.format(result_str)

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
@respond_to('(.*)の(.*)を(削除|削除して|消して)')
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
    try:
        respons = v1.delete_namespaced_pod(name, namespace)
        result = "Success!"
    except :
        result = "Faile!"

    msg = '```\n{}```'.format(respons)

    attachments = [{
        'text': msg,
        'color': "good",
        'mrkdwn_in': [
            'text'
        ]
    }]
    message.send_webapi(result, json.dumps(attachments))

#Podの表示
@respond_to('(Pod|pod|ポッド)(表示して|教えて|一覧|元気？)')
def mention_kubectl(message, arg1, arg2):
    try:
        cmd = 'kubectl {}'.format("get pod")
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

#Podの削除2
@respond_to('(.*)(削除)')
def mention_kubectl(message, arg1, arg2):
    try:
        cmd = 'kubectl {} {}'.format("delete pod",arg1)
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

'''
# Podに負荷を掛ける
@respond_to('(.*)に(負荷をかけて|負荷試験開始して|負荷)')
def menthon_pod(message, arg1, arg2):
    # Kubernetes上で動いているかを環境変数から判断する
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        # ServiceAccountの権限で実行する
        config.load_incluster_config()
        configuration.assert_hostname = False
    else:
        # $HOME/.kube/config から読み込む
        config.load_kube_config()

    podname = arg1
    namespace = "yy-demo-project"

    v1 = client.CoreV1Api()
    exec_command = [
        'yes',
        '>>',
        '/dev/null',
        '&']
    respons = stream(v1.connect_get_namespaced_pod_exec, podname, namespace,
              command=exec_command,
              stderr=True, stdin=False,
              stdout=True, tty=False)

    msg = '```\n{}```'.format(respons)

    attachments = [{
        'text': msg,
        'color': "good",
        'mrkdwn_in': [
            'text'
        ]
    }]
    message.reply_webapi('yesコマンドでCPUに負荷かけてるよ', json.dumps(attachments))
    '''