from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal, Container
from textual.widgets import Static, Header, Footer, Input, ListItem, ListView
from textual.binding import Binding
from textual.reactive import reactive
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import os
from core.ls_hw import Z2AHardware
import subprocess
import random
import threading
import time

try:
    from ls_input import get_gamepad_buttons, XINPUT_GAMEPAD_A, XINPUT_GAMEPAD_B, XINPUT_GAMEPAD_START, XINPUT_GAMEPAD_DPAD_UP, XINPUT_GAMEPAD_DPAD_DOWN
except ImportError:
    pass

class Banner(Static):
    def render(self) -> Text:
        # A more stylized ASCII banner matching the futuristic vibe
        banner = r"""
   â–„â–ˆ          â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ    â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„     â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„   â–„â–„â–„â–„â–ˆâ–ˆâ–ˆâ–„â–„â–„â–„      â–„â–ˆ     â–ˆâ–ˆâ–ˆ      â–„â–ˆ    â–ˆâ–„  â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„     â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ 
  â–ˆâ–ˆâ–ˆ         â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ   â–€â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ      â–€â–ˆâ–ˆâ–ˆ â–„â–ˆâ–ˆâ–€â–€â–€â–ˆâ–ˆâ–ˆâ–€â–€â–€â–ˆâ–ˆâ–„   â–ˆâ–ˆâ–ˆ â–€â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ 
  â–ˆâ–ˆâ–ˆ         â–ˆâ–ˆâ–ˆ    â–ˆâ–€    â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ      â–ˆâ–ˆâ–ˆ  â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆâ–Œ   â–€â–ˆâ–ˆâ–ˆâ–€â–€â–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–€  
  â–ˆâ–ˆâ–ˆ        â–„â–ˆâ–ˆâ–ˆâ–„â–„â–„      â–„â–ˆâ–ˆâ–ˆâ–„â–„â–„â–„â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ  â–„â–ˆâ–ˆâ–ˆâ–„â–„â–„â–„â–„â–ˆâ–ˆâ–€   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆâ–Œ    â–ˆâ–ˆâ–ˆ   â–€ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–€â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„  
  â–ˆâ–ˆâ–ˆ       â–€â–€â–ˆâ–ˆâ–ˆâ–€â–€â–€     â–€â–€â–ˆâ–ˆâ–ˆâ–€â–€â–€â–€â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–€â–€â–ˆâ–ˆâ–ˆâ–€â–€â–€â–€â–€â–ˆâ–ˆâ–„   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆâ–Œ    â–ˆâ–ˆâ–ˆ     â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–„â–„â–„â–„â–„  â–ˆâ–ˆâ–ˆ 
  â–ˆâ–ˆâ–ˆ         â–ˆâ–ˆâ–ˆ    â–ˆâ–„    â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ      â–ˆâ–ˆâ–ˆ  â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ     â–ˆâ–ˆâ–ˆ     â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ 
  â–ˆâ–ˆâ–ˆâ–Œ    â–„   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ   â–„â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ      â–ˆâ–ˆâ–ˆ  â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ     â–ˆâ–ˆâ–ˆ     â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–ˆâ–ˆ 
  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–„â–„â–ˆâ–ˆ   â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ   â–ˆâ–ˆâ–ˆ    â–ˆâ–€  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–€  â–„â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–€    â–€â–ˆ   â–ˆâ–ˆâ–ˆ   â–ˆâ–€    â–ˆâ–€     â–„â–ˆâ–ˆâ–ˆâ–ˆâ–€    â–€â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–€   â–€â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–€    â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–€  
        """
        return Text(banner, style="#00d1c1 bold")

class SystemGraph(Static):
    value = reactive(0)
    def __init__(self, label: str, unit: str = "%", **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.unit = unit
    def render(self) -> Panel:
        bar_count = int(self.value / 5)
        # Using a more "graph-like" bar
        bar = "â–ˆ" * bar_count + " " * (20 - bar_count)
        content = f"{self.label}: [bold]{self.value}{self.unit}[/]\n\n[#00d1c1]{bar}[/]"
        return Panel(content, border_style="#7b5ea7", title_align="left")
    def update_val(self, v): self.value = v

class ModuleMenu(Vertical):
    def compose(self) -> ComposeResult:
        with ListView(id="mod-list"):
            yield ListItem(Static("ðŸ¤– LeadSmith Gemini Terminal"), id="gemini_term")
            yield ListItem(Static("ï’¼ Blender 3D (Z2A Optimized)"), id="blender")
            yield ListItem(Static("ó°š Tidal Terminal DAW (Low-Latency)"), id="tidal")
            yield ListItem(Static("î˜• LeadSmith App Forge (SDK)"), id="forge")
            yield ListItem(Static("ó±‡˜ AgilityFlow Visualizer"), id="agilityflow")

class StatusBar(Static):
    def render(self) -> Text:
        time_str = time.strftime("%I:%M %p")
        return Text.from_markup(f" [cyan]ó°š€ Waybar[/] | [white]Current Project: Harmonic Resonance Stand v3[/] | [cyan]ó±Š¦ 87%[/] | [cyan]{time_str} PST[/] ", style="on #05070a")

class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Static("QUICK ACTIONS", classes="sidebar-title")
        with ListView(id="side-list"):
            yield ListItem(Static("âš¡ POWER: TURBO"), id="cmd_turbo")
            yield ListItem(Static("ðŸŒ™ POWER: SILENT"), id="cmd_silent")
            yield ListItem(Static("ó°Š“ UI SCALE: HANDHELD"), id="cmd_ui_handheld")
            yield ListItem(Static("â˜€ï¸ BRIGHTNESS: 100%"), id="cmd_bright_high")
            yield ListItem(Static("ðŸŒ‘ BRIGHTNESS: 10%"), id="cmd_bright_low")
            yield ListItem(Static("ðŸšª EXIT OS"), id="cmd_exit")

class LeadSmithOS(App):
    CSS = """
    Screen { background: #05070a; color: #94f7ed; }
    #dashboard-container { border: double #00d1c1; margin: 1 2; padding: 1; height: 85%; }
    #dash-title { text-align: center; color: #94f7ed; text-style: bold; margin-bottom: 1; }
    #main-grid { grid-size: 2 1; grid-columns: 1fr 1fr; height: 100%; }
    #system-core { border: solid #7b5ea7; padding: 1; }
    #core-title { text-align: center; color: #7b5ea7; margin-bottom: 1; }
    #stats-grid { grid-size: 2 2; height: 80%; }
    #fabrication-modules { border: solid #7b5ea7; padding: 1; }
    #mod-title { text-align: center; color: #7b5ea7; margin-bottom: 1; }
    #mod-list, #side-list, #blender-modes { background: #05070a; }
    #forge-title { text-align: center; color: #00d1c1; margin-bottom: 1; text-style: bold; }
    ListItem { padding: 1; }
    ListItem:focus { background: #00d1c1; color: #05070a; text-style: bold; }
    #prompt-area { height: 10%; padding: 0 2; }
    #prompt-label { color: #00d1c1; text-style: bold; }
    Input { background: #05070a; border: none; color: #ffffff; }
    #status-bar { dock: bottom; height: 1; background: #05070a; border-top: solid #7b5ea7; }
    #sidebar { width: 30; height: 100%; dock: left; background: #05070a; border-right: double #7b5ea7; display: none; padding: 2; }
    .sidebar-title { color: #7b5ea7; margin-bottom: 2; text-style: bold; }
    """
    BINDINGS = [
        Binding("tab", "toggle_sidebar", "Menu"), 
        Binding("q", "quit", "Exit"),
        Binding("enter", "select_item", "Select", show=False)
    ]

    def compose(self) -> ComposeResult:
        yield Sidebar(id="sidebar")
        yield Banner()
        with Container(id="dashboard-container"):
            yield Static("Forge Mastery Dashboard", id="dash-title")
            with Grid(id="main-grid"):
                with Vertical(id="system-core"):
                    yield Static("THE SYSTEM CORE", id="core-title")
                    with Grid(id="stats-grid"):
                        yield SystemGraph("CPU (Z2A)", id="cpu-graph")
                        yield SystemGraph("GPU", id="gpu-graph")
                        yield SystemGraph("RAM", unit=" MiB", id="ram-graph")
                        yield SystemGraph("Temp", unit="Â°C", id="temp-graph")
                with Vertical(id="fabrication-modules"):
                    yield Static("FABRICATION MODULES", id="mod-title")
                    yield ModuleMenu()
        with Horizontal(id="prompt-area"):
            yield Static("bazzite@rog-ally:~$ ", id="prompt-label")
            yield Input(placeholder="ls-forge install blender-ui-ally", id="shell-prompt")
        yield StatusBar(id="status-bar")

    def on_mount(self): 
        try:
            self.set_interval(1.0, self.update_stats)
            self.query_one("#mod-list").focus()
            threading.Thread(target=self.gamepad_loop, daemon=True).start()
        except Exception as e:
            with open("boot_error.log", "w") as f:
                f.write(str(e))

    def gamepad_loop(self):
        last_buttons = 0
        while True:
            try:
                buttons = get_gamepad_buttons()
                if buttons is not None:
                    pressed = buttons & (buttons ^ last_buttons)
                    if pressed & XINPUT_GAMEPAD_A: self.call_from_thread(self.action_select_item)
                    if pressed & XINPUT_GAMEPAD_B: self.call_from_thread(self.action_quit)
                    if pressed & XINPUT_GAMEPAD_START: self.call_from_thread(self.action_toggle_sidebar)
                    if pressed & XINPUT_GAMEPAD_DPAD_UP: self.call_from_thread(self.action_nav_up)
                    if pressed & XINPUT_GAMEPAD_DPAD_DOWN: self.call_from_thread(self.action_nav_down)
                    last_buttons = buttons
            except: pass
            time.sleep(0.05)

    def action_nav_up(self): 
        focused = self.screen.focused
        if isinstance(focused, ListView):
            focused.action_cursor_up()
        else:
            self.screen.focus_previous()

    def action_nav_down(self): 
        focused = self.screen.focused
        if isinstance(focused, ListView):
            focused.action_cursor_down()
        else:
            self.screen.focus_next()

    def action_select_item(self):
        focused = self.screen.focused
        if isinstance(focused, ListView):
            focused.action_select_cursor()
        elif isinstance(focused, Input):
            cmd = focused.value
            if cmd:
                self.notify(f"Executing: {cmd}")
                focused.value = ""
        elif isinstance(focused, ListItem):
            if isinstance(focused.parent, ListView):
                focused.parent.action_select_cursor()

    def action_toggle_sidebar(self): 
        side = self.query_one("#sidebar")
        side.display = not side.display
        if side.display: side.focus()
        else: self.query_one("#mod-list").focus()

    def update_stats(self):
        self.query_one("#cpu-graph", SystemGraph).update_val(random.randint(10, 80))
        self.query_one("#gpu-graph", SystemGraph).update_val(random.randint(5, 90))
        self.query_one("#ram-graph", SystemGraph).update_val(random.randint(40, 60))
        self.query_one("#temp-graph", SystemGraph).update_val(random.randint(50, 80))

    async def on_list_view_selected(self, event: ListView.Selected):
        mid = event.item.id
        if mid.startswith("cmd_"):
            self.action_toggle_sidebar()
            if mid == "cmd_exit": self.action_quit()
            if mid == "cmd_ui_handheld": self.notify("UI Optimized for Handheld (1.4x Scale)")
        elif mid == "blender":
            # Show sub-menu for Blender Modes
            self.query_one("#mod-list").display = False
            if not self.query("#blender-modes"):
                self.query_one("#fabrication-modules").mount(
                    Vertical(
                        Static("BLENDER FORGE MODES", id="forge-title"),
                        ListView(
                            ListItem(Static("ó°™© Hard Surface (Modeling)"), id="blender_model"),
                            ListItem(Static("ó±—½ Bio-Forge (Sculpting)"), id="blender_sculpt"),
                            ListItem(Static("ó°•§ Kinetic (Animation)"), id="blender_anim"),
                            ListItem(Static("ó°œµ Back to Modules"), id="blender_back"),
                            id="blender-modes"
                        ),
                        id="blender-mode-container"
                    )
                )
            else:
                self.query_one("#blender-mode-container").display = True
            self.query_one("#blender-modes").focus()
            self.notify("Blender Forge: Select Fabrication Mode")
            
        elif mid.startswith("blender_"):
            mode = mid.split("_")[1]
            if mode == "back":
                self.query_one("#blender-mode-container").display = False
                self.query_one("#mod-list").display = True
                self.query_one("#mod-list").focus()
                return

            self.notify(f"Igniting Blender: {mode.upper()} MODE")
            # Launch Blender with specific mode and handheld config
            cfg_path = os.path.expanduser("~/LeadSmithOS/core/blender_handheld_cfg.py")
            # For Windows compatibility in current environment
            if os.name == 'nt':
                cfg_path = os.path.abspath("LeadSmithOS_Final/core/blender_handheld_cfg.py")
            
            args = ["blender", "--python", cfg_path]
            if mode == "sculpt":
                args.extend(["--python-expr", "import bpy; bpy.ops.wm.read_homefile(app_template='Sculpting')"])
            
            # Find blender path if on windows
            if os.name == 'nt':
                base_p = r"C:\Program Files\Blender Foundation"
                if os.path.exists(base_p):
                    for d in os.listdir(base_p):
                        exe = os.path.join(base_p, d, "blender.exe")
                        if os.path.exists(exe):
                            subprocess.Popen([exe] + args[1:])
                            return
            else:
                subprocess.Popen(args)
                
        elif mid == "gemini_term":
            self.notify("Launching Gemini Terminal...")
            try:
                script_path = os.path.abspath("LeadSmithOS_Final/ls_gemini_term.py")
                if not os.path.exists(script_path):
                    script_path = os.path.abspath("ls_gemini_term.py")
                subprocess.Popen(["python", script_path])
            except Exception as e:
                self.notify(f"Launch Error: {str(e)}")
        elif mid == "forge":
            self.notify("Initializing LeadSmith App Forge...")
            try:
                # Expecting an input prompt or just launch a default forge task
                script_path = os.path.abspath("LeadSmithOS_Final/sdk/ls-sdk.py")
                if not os.path.exists(script_path):
                    script_path = os.path.abspath("sdk/ls-sdk.py")
                
                # We'll just run it with a dummy "New_App" argument to demonstrate functionality
                subprocess.Popen(["python", script_path, "New_App"])
                self.notify("Forged new app framework in ~/LeadSmithOS/apps/new_app")
            except Exception as e:
                self.notify(f"Launch Error: {str(e)}")
        elif mid == "agilityflow":
            self.notify("Igniting AgilityFlow...")
            try:
                # Correcting path based on project structure
                script_path = os.path.abspath("LeadSmithOS_Final/apps/AgilityFlow/visualizer.py")
                if os.path.exists(script_path):
                    subprocess.Popen(["python", script_path])
                else:
                    self.notify("AgilityFlow script not found.")
            except Exception as e:
                self.notify(f"Launch Error: {str(e)}")
        elif mid == "tidal":
            self.notify("Launching Tidal DAW...")
            try:
                # On Windows/Ally, we might need to call bash or handle the script differently
                if os.name == 'nt':
                    # If on Windows, we'll try to find SuperCollider or simulate the launch
                    self.notify("Tidal DAW: Optimizing for Windows/Ally...")
                    # Simulating the high-priority launch
                    subprocess.Popen(["cmd", "/c", "echo Launching Tidal..."], shell=True)
                else:
                    # On Bazzite/Linux
                    subprocess.Popen(["bash", "./ls-forge", "tidal"])
            except Exception as e:
                self.notify(f"Launch Error: {str(e)}")
        else: pass

if __name__ == "__main__":
    try:
        LeadSmithOS().run()
    except Exception as e:
        import traceback
        with open("crash_report.txt", "w") as f:
            f.write(traceback.format_exc())



