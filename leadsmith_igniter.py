import pygame
import subprocess
import os
import sys
import time

# Master Palette
DEEP_VOID = (5, 7, 10)
CYAN = (0, 255, 255)
VIOLET = (160, 32, 240)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

class MasterIgniter:
    def __init__(self):
        pygame.init()
        # Scale to Z2A 1080p touch screen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.NOFRAME)
        self.sw, self.sh = pygame.display.get_surface().get_size()
        self.font = pygame.font.SysFont("Consolas", int(self.sh * 0.04), bold=True)
        self.small_font = pygame.font.SysFont("Consolas", int(self.sh * 0.03))
        self.running = True
        self.state = "MAIN" # MAIN, WIFI_LIST, KEYBOARD
        
        self.networks = []
        self.selected_ssid = ""
        self.wifi_pass = ""
        
        # Gamepad init
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
        if self.joy: self.joy.init()

    def draw_button(self, text, color, rect, text_color=DEEP_VOID):
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        txt_surf = self.font.render(text, True, text_color)
        self.screen.blit(txt_surf, (rect.centerx - txt_surf.get_width() // 2, rect.centery - txt_surf.get_height() // 2))
        return rect

    def get_networks(self):
        try:
            res = subprocess.run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True)
            self.networks = list(set([line for line in res.stdout.split("\n") if line.strip()]))
        except:
            self.networks = ["Error: nmcli not found", "Check hardware switch"]

    def run_forge(self):
        while self.running:
            self.screen.fill(DEEP_VOID)
            
            if self.state == "MAIN":
                self.draw_main()
            elif self.state == "WIFI_LIST":
                self.draw_wifi_list()
            elif self.state == "KEYBOARD":
                self.draw_keyboard()

            pygame.display.flip()
            self.handle_events()

    def draw_main(self):
        title = self.font.render("LEADSMITH Z2A: IGNITION ENGINE", True, CYAN)
        self.screen.blit(title, (self.sw // 2 - title.get_width() // 2, self.sh * 0.1))
        
        self.ignite_btn = self.draw_button("IGNITE INSTALL", CYAN, pygame.Rect(self.sw//4, self.sh*0.3, self.sw//2, self.sh*0.15))
        self.wifi_btn = self.draw_button("CONNECT WI-FI", VIOLET, pygame.Rect(self.sw//4, self.sh*0.5, self.sw//2, self.sh*0.15))
        self.exit_btn = self.draw_button("EXIT", WHITE, pygame.Rect(self.sw//4, self.sh*0.7, self.sw//2, self.sh*0.15), text_color=DEEP_VOID)

    def draw_wifi_list(self):
        title = self.font.render("SELECT WI-FI NETWORK", True, CYAN)
        self.screen.blit(title, (self.sw // 2 - title.get_width() // 2, self.sh * 0.05))
        
        y = self.sh * 0.15
        self.network_rects = []
        for ssid in self.networks[:8]: # Show top 8
            rect = pygame.Rect(self.sw*0.1, y, self.sw*0.8, self.sh*0.08)
            pygame.draw.rect(self.screen, GRAY, rect, border_radius=5)
            txt = self.small_font.render(ssid, True, WHITE)
            self.screen.blit(txt, (rect.x + 20, rect.centery - txt.get_height()//2))
            self.network_rects.append((rect, ssid))
            y += self.sh * 0.09
        
        self.back_btn = self.draw_button("BACK", WHITE, pygame.Rect(self.sw//4, self.sh*0.88, self.sw//2, self.sh*0.08))

    def draw_keyboard(self):
        title = self.font.render(f"SSID: {self.selected_ssid}", True, CYAN)
        self.screen.blit(title, (self.sw*0.1, self.sh*0.05))
        
        pass_box = pygame.Rect(self.sw*0.1, self.sh*0.12, self.sw*0.8, self.sh*0.1)
        pygame.draw.rect(self.screen, WHITE, pass_box, border_radius=5)
        pass_txt = self.font.render("*" * len(self.wifi_pass) + "_", True, DEEP_VOID)
        self.screen.blit(pass_txt, (pass_box.x + 20, pass_box.centery - pass_txt.get_height()//2))
        
        # Simple Grid Keyboard
        keys = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
        self.key_rects = []
        kw, kh = self.sw // 12, self.sh // 10
        for i, char in enumerate(keys):
            row = i // 10
            col = i % 10
            rect = pygame.Rect(self.sw*0.1 + col*kw, self.sh*0.3 + row*kh, kw-10, kh-10)
            self.draw_button(char, GRAY, rect, WHITE)
            self.key_rects.append((rect, char))
            
        self.del_btn = self.draw_button("DEL", VIOLET, pygame.Rect(self.sw*0.1, self.sh*0.75, kw*2, kh))
        self.conn_btn = self.draw_button("CONNECT", CYAN, pygame.Rect(self.sw*0.4, self.sh*0.75, kw*4, kh))
        self.kb_back_btn = self.draw_button("BACK", WHITE, pygame.Rect(self.sw*0.8, self.sh*0.75, kw*2, kh))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if self.state == "MAIN":
                    if self.ignite_btn.collidepoint(pos): self.start_install()
                    if self.wifi_btn.collidepoint(pos):
                        self.get_networks()
                        self.state = "WIFI_LIST"
                    if self.exit_btn.collidepoint(pos): self.running = False
                
                elif self.state == "WIFI_LIST":
                    for rect, ssid in self.network_rects:
                        if rect.collidepoint(pos):
                            self.selected_ssid = ssid
                            self.state = "KEYBOARD"
                    if self.back_btn.collidepoint(pos): self.state = "MAIN"
                
                elif self.state == "KEYBOARD":
                    for rect, char in self.key_rects:
                        if rect.collidepoint(pos): self.wifi_pass += char
                    if self.del_btn.collidepoint(pos): self.wifi_pass = self.wifi_pass[:-1]
                    if self.kb_back_btn.collidepoint(pos): self.state = "WIFI_LIST"
                    if self.conn_btn.collidepoint(pos): self.connect_wifi()

    def connect_wifi(self):
        print(f"Connecting to {self.selected_ssid}...")
        subprocess.run(["nmcli", "dev", "wifi", "connect", self.selected_ssid, "password", self.wifi_pass])
        self.state = "MAIN"

    def start_install(self):
        print("[IGNITING] Commencing Z2A Forge Installation (SILENT MODE)...")
        config_path = os.path.join(os.path.dirname(__file__), "z2a_config.json")
        # Added --silent and --confirm-external-config for keyboard-less automation
        proc = subprocess.Popen(["archinstall", "--silent", "--config", config_path])
        proc.wait()

        # Inject LeadSmith OS files to the target
        print("[INJECTING] Injecting LeadSmith OS Files to Target OS...")
        source_dir = os.path.dirname(os.path.abspath(__file__))
        target_root = "/mnt/archinstall"
        target_home = os.path.join(target_root, "home/leadsmith/LeadSmithOS")

        try:
            subprocess.run(["mkdir", "-p", target_home], check=True)
            subprocess.run(["cp", "-r", source_dir + "/.", target_home], check=True)
            subprocess.run(["chown", "-R", "1000:1000", target_home], check=True)
            subprocess.run(["chmod", "+x", os.path.join(target_home, "ls-boot.sh")], check=True)
            
            # AUTOMATION: Set up LeadSmith OS Autostart
            autostart_dir = os.path.join(target_root, "home/leadsmith/.config/autostart")
            subprocess.run(["mkdir", "-p", autostart_dir], check=True)
            with open(os.path.join(autostart_dir, "leadsmith.desktop"), "w") as f:
                f.write("[Desktop Entry]\nType=Application\nExec=/home/leadsmith/LeadSmithOS/ls-boot.sh\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=LeadSmith OS Dashboard\n")
            
            # AUTOMATION: Configure GDM Auto-login
            gdm_conf_path = os.path.join(target_root, "etc/gdm/custom.conf")
            subprocess.run(["mkdir", "-p", os.path.dirname(gdm_conf_path)], check=True)
            with open(gdm_conf_path, "w") as f:
                f.write("[daemon]\nAutomaticLoginEnable=True\nAutomaticLogin=leadsmith\n")
            
            print("[âœ“] Injection Success. Auto-Boot configured.")
        except Exception as e:
            print(f"[!] Injection Failed: {str(e)}")

        self.running = False

if __name__ == "__main__":
    MasterIgniter().run_forge()
