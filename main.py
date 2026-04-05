from api import SiliconAPI
from utils import truncate_tokens, format_code, save_chat_history
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import click

console = Console()
client = SiliconAPI()
# 全局对话历史
chat_history = []

@click.group()
def cli():
    """硅基流动终端对话工具"""
    pass

@cli.command()
def chat():
    """启动交互式对话"""
    main()

def show_help():
    """显示帮助菜单"""
    help_text = Text()
    help_text.append("📖 可用命令：\n", style="bold cyan")
    help_text.append("/model    ", style="bold green")
    help_text.append("切换AI模型（")
    help_text.append(", ".join(client.get_available_models()), style="yellow")
    help_text.append("）\n")
    help_text.append("/exit     ", style="bold green")
    help_text.append("退出程序\n")
    help_text.append("/help     ", style="bold green")
    help_text.append("查看帮助\n")
    help_text.append("/clear    ", style="bold green")
    help_text.append("清空对话历史\n")
    help_text.append("/save     ", style="bold green")
    help_text.append("保存对话历史")
    console.print(Panel(help_text, title="帮助菜单", border_style="cyan"))

def switch_model():
    """切换模型交互"""
    models = client.get_available_models()
    console.print(f"\n[bold cyan]可用模型：[/bold cyan] [yellow]{', '.join(models)}[/yellow]")
    model_name = Prompt.ask("[bold green]请输入模型名称[/bold green]")
    if client.set_model(model_name):
        console.print(f"✅ 已切换模型：[bold yellow]{model_name}[/bold yellow]")
    else:
        console.print(f"❌ 模型不存在！可用：[yellow]{', '.join(models)}[/yellow]")

def clear_history():
    """清空对话历史"""
    global chat_history
    chat_history.clear()
    console.print("[bold green]✅ 对话历史已清空[/bold green]")

def main():
    # 关键修复：在main函数里声明全局变量chat_history
    global chat_history
    console.print(Panel(
        "[bold magenta]🔥 硅基流动终端对话工具 🔥[/bold magenta]\n[dim]输入 /help 查看命令[/dim]",
        border_style="magenta"
    ))
    show_help()

    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]你[/bold blue]").strip()
            if not user_input:
                continue

            if user_input == "/exit":
                console.print("[bold cyan]👋 再见！[/bold cyan]")
                break
            elif user_input == "/help":
                show_help()
            elif user_input == "/model":
                switch_model()
            elif user_input == "/clear":
                clear_history()
            elif user_input == "/save":
                if save_chat_history(chat_history):
                    console.print("[bold green]✅ 对话已保存[/bold green]")
                else:
                    console.print("[bold red]❌ 保存失败[/bold red]")
            else:
                chat_history.append({"role": "user", "content": user_input})
                chat_history = truncate_tokens(chat_history)

                with console.status("[bold yellow]AI 思考中...[/bold yellow]", spinner="dots"):
                    response = client.chat(chat_history)

                response = format_code(response)
                console.print(f"\n[bold green]AI[/bold green]: {response}")
                chat_history.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            console.print("\n[bold cyan]👋 再见！[/bold cyan]")
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ 错误：{str(e)}[/bold red]")
            if chat_history and chat_history[-1]["role"] == "user":
                chat_history.pop()

if __name__ == "__main__":
    cli()