from typing import Optional
import typer

from path_thraversal import AutomizedPathTraversal
from xss import xss_poc

app = typer.Typer()


@app.command()
def path_traversal_resolver(ctf_session_code: str):
    """
    An automized script to solve all path traversal CTFs of PortSwigger. 
    """
    AutomizedPathTraversal.main(ctf_session_code=ctf_session_code)

@app.command()
def xss_resolver(ctf_session_code: Optional[str] = typer.Argument(None), exploit_server_session_code: Optional[str]  = typer.Argument(None)):
    """
    A script to solve the CTF "Reflected XSS into HTML context with most tags and attributes blocked".
    """
    xss_poc.main(ctf_session_code, exploit_server_session_code)

@app.command()
def ssrf_resolver(ctf_session_code: str):
    """
    A script to solve the CTF "SSRF with whitelist-based input filter".
    """
    pass


if __name__ == "__main__":
    app()