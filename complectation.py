from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
import os
import subprocess

console = Console()

warning_text = Text("\nWARNING!!!!", style="bold red")
dev_text = Text("\nРазработчик: Yoshiko", style="bold white")
rules_text = Text("\n- Ознакомьтесь с правилами", style="bold yellow")
disclaimer_text = Text("\nДисклеймер: Этот проект создан в развлекательных целях и был написан с помощью ИИ, автор не несет ответственности за ваши действия!", style="italic green")

console.print(dev_text)
console.print(warning_text)
console.print(rules_text)
console.print("\n1.0: Мы не несем ответственности за ваши действия которые будут сделаны с помощью этой программы", style="cyan")
console.print(disclaimer_text)

agreement = Prompt.ask("[bold blue]Согласны?[/bold blue] -", choices=["Да", "Нет"])

if agreement == "Да":
    console.print("[bold green]Вы согласились с условиями.[/bold green]")
    
    def convert_to_exe(py_file):
        command = f"pyinstaller --onefile {py_file}"


        subprocess.run(command, shell=True)

    py_file = "stealer/Melver.py"  

    if os.path.exists(py_file):
        console.print(f"[bold yellow]Создание .exe из {py_file}...[/bold yellow]")
        convert_to_exe(py_file)
        console.print("[bold green]Файл .exe создан![/bold green]")
    else:
        console.print(f"[bold red]Файл {py_file} не найден.[/bold red]")
else:
    console.print("[bold red]Вы не согласились с условиями. Программа будет закрыта.[/bold red]")
