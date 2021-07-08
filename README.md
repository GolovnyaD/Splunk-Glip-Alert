# Splunk alert python script
which push message in RingCentral Glip messenger using REST API and JSON.

## What was added:
- Debug info and exceptions catching.
- Field "Additional info" in Adaptive Response Actions for static data (fo example playbook wiki page that not depends on search results).
- Field "splunk_results" that must generate in Splunk search and will send to Glip (for example affected hosts).

### Debugging logs:
By default you can find running/error logs in Splunk "index=_internal sourcetype=splunkd glipalert". Also you can rewrite function log_output to your needs.

### How to use?
Make tar archive and follow instruction for single-instance deployment: https://docs.splunk.com/Documentation/AddOns/released/Overview/Singleserverinstall or distributed deployment: https://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall

### How to test?
 You can run script and push JSON like Splunk do (configuration - data from Adaptive Response page, result - Splunk search results):
`echo '{"configuration":{"webhook_id":"YOUR WEBHOOK ID HERE", "title":"Honeypot Incident", "add_info":"mywiki/playbook"}, "result":{ "splunk_results":"host1,host2"}}' |  python3 glipalert.py --execute`
