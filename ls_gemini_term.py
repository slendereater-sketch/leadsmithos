from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Input, RichLog
from textual.binding import Binding
import subprocess
import threading
import os

class GeminiTerminal(App):
    TITLE = "LeadSmith Gemini Terminal"
    
    CSS = """
    Screen { background: #05070a; color: #94f7ed; }
    #chat-log { height: 1fr; border: solid #7b5ea7; }
    #prompt-area { height: 3; dock: bottom; border-top: solid #00d1c1; }
    Input { background: #05070a; border: none; color: #ffffff; }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Exit Terminal"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield RichLog(id="chat-log", markup=True, wrap=True)
        with Horizontal(id="prompt-area"):
            yield Input(placeholder="Ask Gemini / Prefix with ! for shell command...", id="shell-prompt")
        yield Footer()

    def on_mount(self):
        self.query_one(Input).focus()
        log = self.query_one(RichLog)
        log.write("[bold #00d1c1]LeadSmith Forge Terminal - Powered by Gemini Core[/]")
        log.write("[#7b5ea7]Type a prompt to ask Gemini, or prefix with '!' to run a local system command.[/]")
        log.write("[#7b5ea7]Example: 'Write a python script for a dashboard' or '!ls -la'[/]\n")

    def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value
        if not cmd.strip(): return
        
        event.input.value = ""
        log = self.query_one(RichLog)
        log.write(f"\n[bold white]User:[/] {cmd}")
        
        if cmd.startswith("!"):
            # Run local command
            threading.Thread(target=self.run_local, args=(cmd[1:].strip(),), daemon=True).start()
        else:
            # Run Gemini command
            threading.Thread(target=self.run_gemini, args=(cmd,), daemon=True).start()
            
    def run_local(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            out = result.stdout if result.stdout else result.stderr
            if not out: out = "Command executed with no output."
            self.call_from_thread(self.write_log, f"[bold #7b5ea7]System:[/] \n{out}")
        except Exception as e:
            self.call_from_thread(self.write_log, f"[bold red]System Error:[/] {str(e)}")
            
    def run_gemini(self, prompt):
        self.call_from_thread(self.write_log, "[italic #00d1c1]Consulting Gemini Core...[/italic]")
        try:
            # Use gemini CLI
            # Since the user is using the Gemini CLI, 'gemini' should be accessible.
            # Using 'gemini' command or via npx if needed, but standard 'gemini' works globally.
            import os
            cmd = f'gemini ask "{prompt}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            
            out = result.stdout.strip()
            err = result.stderr.strip()
            
            if out:
                self.call_from_thread(self.write_log, f"[bold #00d1c1]Gemini:[/] \n{out}")
            elif err:
                # Some CLIs print output to stderr
                self.call_from_thread(self.write_log, f"[bold #00d1c1]Gemini:[/] \n{err}")
            else:
                self.call_from_thread(self.write_log, f"[bold #00d1c1]Gemini:[/] (No response received. Ensure Gemini CLI is configured.)")
        except Exception as e:
            self.call_from_thread(self.write_log, f"[bold red]Gemini Link Failed:[/] {e}")

    def write_log(self, text):
        log = self.query_one(RichLog)
        # remove Textual-breaking markup tags if necessary or rely on rich parsing
        # but Gemini outputs markdown. RichLog handles markdown partially, but wait!
        # RichLog(markup=True) interprets [ ] tags. If gemini outputs [ ], it breaks.
        # So we should escape [ to \[ inside the content? Or set markup=False for the content.
        # Let's set markup=False for user/gemini content and use write(text)
        log.write(text)

if __name__ == "__main__":
    try:
        GeminiTerminal().run()
    except Exception as e:
        import traceback
        with open("gemini_error.log", "w") as f:
            f.write(traceback.format_exc())
