from .settings import settings
from rich import print

if __name__ == "__main__":
    print("\n[bold blue]Hello from Gandalf![/bold blue]\n")
    print(
        "[italic yellow]“Many that live deserve death. And some that die deserve life. "
        "Can you give it to them? Then do not be too eager to "
        "deal out death in judgement.”[/italic yellow]\n\n"
    )

    print("[bold green]Settings loaded:[/bold green]")
    print(settings.model_dump())
