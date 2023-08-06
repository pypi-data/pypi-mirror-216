from shortcut import *
from rich.console import Console
from rich.prompt import Prompt, Confirm

con = Console(style='blue')

desktop=False
menu=False

con.print('[bold]>>>>>>>>>')
print()

place = Prompt.ask("[bold blue]which shortcut do you want ? ", choices=('menu','desktop','both'), default='both')
while(not (name:=(con.input('[bold]name : ').strip()))):
    con.print("[red]name field can't be empty")
while(not (command:=(con.input('[bold]command : ').strip()))):
    con.print("[red]command field can't be empty")
while(not (icon:=(con.input('[bold]icon : ').strip()))):
    con.print("[red]icon field can't be empty")
terminal=Confirm.ask('[bold blue]does it needs terminal ? ')

if place=='both':
    desktop=True
    menu=True
elif place=='desktop':
    desktop=True
else:
    menu=True
try:
    if menu:
        createMenuShortCut(name=name,command=command,icon=icon,terminal=terminal)
    if desktop:
        createDesktopShortCut(name=name,command=command,icon=icon,terminal=terminal)
    con.print('[bold green]successfully created')
    print()
    con.print('[bold green]✔✔✔')
except:
    con.print('[red]something went wrong!')
    print()
    con.print('[bold red]✗✗✗')
