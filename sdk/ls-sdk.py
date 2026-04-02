import os, sys, argparse
from rich.console import Console
console = Console()
class LeadSmithForge:
    def __init__(self, name):
        self.name = name.lower().replace(" ", "_")
        self.path = os.path.expanduser(f"~/LeadSmithOS/apps/{self.name}")
    def forge(self):
        os.makedirs(f"{self.path}/src", exist_ok=True)
        with open(f"{self.path}/src/main.py", "w") as f:
            f.write("from textual.app import App
class New(App): pass
if __name__ == '__main__': New().run()")
        print(f"Forged: {self.name}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    LeadSmithForge(args.name).forge()
