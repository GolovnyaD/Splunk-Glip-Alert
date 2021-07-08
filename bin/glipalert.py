# Splunk alert for sending message to RingCentral Glip messenger

import requests
import json
import sys


def log_output(message):
    print(message, file=sys.stderr)


def send_message(configuration, result):
    webhook_uri = 'https://hooks.glip.com/webhook/' + str(configuration.get('webhook_id'))
    # in cases where no splunk_results/add_info fields/title in Splunk results
    if 'title' in configuration:
        title = configuration.get('title')
    else:
        title = 'No title'

    message = ''
    if 'splunk_results' in result:
        message = result.get('splunk_results')
    if 'add_info' in configuration:
        if len(message) > 0:
            message = message + "\n\n" + configuration.get('add_info')
        else:
            message = configuration.get('add_info')

    post_data = {
        "activity": title,
        "title": message
    }

    try:
        response = requests.post(webhook_uri, data=post_data, timeout=20) # timeout for cases when firewall blocking connection
    except requests.exceptions.RequestException as e:
        log_output("ERROR glipalert Exception while response: " + str(e))
        return False

    if response.status_code == 200:
        log_output("INFO glipalert Notification successfully sent")
        return True
    else:
        log_output("INFO glipalert Returned status code: " + str(response.status_code) + ", response: " + response.text)
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        # in cases when Splunk results is empty, it's generating JSON is wrong format: ...'result': None}
        payload_raw = sys.stdin.read()
        payload_raw = payload_raw.replace("\": None", "\": \"\"")
        payload = json.loads(payload_raw)
        # if something goes wrong, I want to have raw payload for investigation
        log_output("INFO glipalert Post data " + str(payload))
        if not send_message(payload.get('configuration'), payload.get('result')):
            log_output("FATAL glipalert Failed trying to send notification")
            sys.exit(2)
    else:
        log_output("FATAL glipalert No message argument")
        sys.exit(1)