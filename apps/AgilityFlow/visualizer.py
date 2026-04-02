import pygame
import numpy as np
import sounddevice as sd
from scipy.fft import fft
import json
import os
import sys
from enum import Enum

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
import moderngl
from pyrr import Matrix44

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Set up display - ROG Ally Z2A resolution
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Milkdrop 4 - Next Gen (ROG Ally Z2A Edition)")

# ModernGL context
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND)
ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

# Colors from spec
PRIMARY = (10, 10, 15)
ACCENT1 = (0, 255, 255)
ACCENT2 = (188, 19, 254)

# XInput Button Mapping for ROG Ally Z2A
class ControllerButton(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    BACK = 6
    START = 7
    LEFT_STICK = 8
    RIGHT_STICK = 9

# Joystick
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick: {joystick.get_name()}")

# Audio setup
SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
audio_data = np.zeros(BLOCK_SIZE)
audio_smoothing = 0.85

smooth_bass, smooth_mids, smooth_highs, smooth_sub_bass = 0, 0, 0, 0

def audio_callback(indata, frames, time, status):
    global audio_data
    if status:
        print(status)
    audio_data = indata[:, 0]

stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE)
stream.start()

# Generic vertex shader for a fullscreen quad
fullscreen_quad_vs = """
    #version 330
    in vec2 in_vert;
    out vec2 v_text;
    void main() {
        v_text = in_vert * 0.5 + 0.5;
        gl_Position = vec4(in_vert, 0.0, 1.0);
    }
"""

# --- Base Shader Engine Class ---
class ShaderEngine:
    def __init__(self, context):
        self.time = 0
        self.ctx = context
        self.program = None
        self.vao = None

    def load_preset(self, preset_data):
        # Base implementation does nothing, child classes should override
        pass

    def update(self, dt):
        self.time += dt

    def get_fullscreen_quad(self, program):
        vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        content = [(vbo, '2f', 'in_vert')]
        return self.ctx.vertex_array(program, content)

    def draw(self, screen, bass, mids, highs, fft_data):
        if self.program:
            self.ctx.clear(PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
            self.vao.render(moderngl.TRIANGLE_STRIP)

# --- SHADER-BASED VISUALIZATIONS ---

class SpectrumBars(ShaderEngine):
    def __init__(self, context):
        super().__init__(context)
        self.name = "Spectrum Bars"
        self.bar_count = 128
        self.program = self.ctx.program(
            vertex_shader=fullscreen_quad_vs,
            fragment_shader="""
                #version 330
                in vec2 v_text;
                out vec4 f_color;
                uniform float fft_data[128];
                uniform vec3 color_primary, color_accent1, color_accent2;
                void main() {
                    int bar_index = int(v_text.x * 128.0);
                    float bar_height = fft_data[bar_index] * 1.5;
                    vec3 final_color = color_primary;
                    if (v_text.y < bar_height) {
                        float color_t = float(bar_index) / 128.0;
                        vec3 color = mix(color_accent1, color_accent2, color_t);
                        if (v_text.y > bar_height - 0.02) color = vec3(1.0);
                        final_color = color;
                    }
                    f_color = vec4(final_color, 1.0);
                }
            """
        )
        self.program['color_primary'].value = (PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
        self.program['color_accent1'].value = (ACCENT1[0]/255.0, ACCENT1[1]/255.0, ACCENT1[2]/255.0)
        self.program['color_accent2'].value = (ACCENT2[0]/255.0, ACCENT2[1]/255.0, ACCENT2[2]/255.0)
        self.vao = self.get_fullscreen_quad(self.program)

    def draw(self, screen, bass, mids, highs, fft_data):
        self.ctx.clear(PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
        fft_texture_data = np.zeros(self.bar_count, dtype='f4')
        valid_fft = fft_data[np.isfinite(fft_data)]
        if len(valid_fft) > 0:
            for i in range(self.bar_count):
                idx = int((i / self.bar_count) * len(valid_fft))
                if idx < len(valid_fft): fft_texture_data[i] = min(1.0, valid_fft[idx])
        self.program['fft_data'].value = tuple(fft_texture_data)
        self.vao.render(moderngl.TRIANGLE_STRIP)

class RadialWaves(ShaderEngine):
    def __init__(self, context):
        super().__init__(context)
        self.name = "Radial Waves"
        self.program = self.ctx.program(
            vertex_shader=fullscreen_quad_vs,
            fragment_shader="""
                #version 330
                in vec2 v_text;
                out vec4 f_color;
                uniform float time, bass, mids, highs;
                uniform vec2 resolution;

                vec3 hsv2rgb(vec3 c) {
                    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
                }

                void main() {
                    vec2 uv = v_text * 2.0 - 1.0;
                    uv.x *= resolution.x / resolution.y;
                    float d = length(uv);
                    float color = 0.0;
                    for(int i = 0; i < 12; i++){
                        float t = time * 0.5 + float(i) * 0.3;
                        float r = fract(d * 2.0 + t + bass * 2.0);
                        float ripple = smoothstep(0.0, 0.2, r) - smoothstep(0.2, 0.4, r);
                        color += ripple * (1.0 - d);
                    }
                    vec3 hsv = vec3(fract(d + time * 0.1 + mids * 0.5), 1.0, 1.0);
                    vec3 rgb = hsv2rgb(hsv);
                    f_color = vec4(rgb * color, 1.0);
                }
            """
        )
        self.program['resolution'].value = (WIDTH, HEIGHT)
        self.vao = self.get_fullscreen_quad(self.program)

    def draw(self, screen, bass, mids, highs, fft_data):
        self.ctx.clear(PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
        self.program['time'].value = self.time
        self.program['bass'].value = bass
        self.program['mids'].value = mids
        self.program['highs'].value = highs
        self.vao.render(moderngl.TRIANGLE_STRIP)

class DotGrid(ShaderEngine):
    def __init__(self, context):
        super().__init__(context)
        self.name = "Dot Grid"
        self.program = self.ctx.program(
            vertex_shader=fullscreen_quad_vs,
            fragment_shader="""
                #version 330
                in vec2 v_text;
                out vec4 f_color;
                uniform float time, bass, mids, highs;
                uniform vec2 resolution;
                uniform vec3 color_primary, color_accent1, color_accent2;

                // Params from neon_grid.milk
                uniform float grid_spacing = 50.0;
                uniform float dot_size_base = 6.0;
                uniform float pulse_intensity = 0.8;
                uniform float pulse_speed = 2.5;

                float circle(vec2 uv, vec2 pos, float radius, float softness) {
                    float d = length(uv - pos);
                    return 1.0 - smoothstep(radius - softness, radius + softness, d);
                }

                void main() {
                    vec2 uv = v_text * resolution;
                    vec2 grid_uv = fract(uv / grid_spacing) * grid_spacing;
                    
                    float dot_size = dot_size_base + bass * pulse_intensity * 20.0 + highs * 5.0;
                    
                    float c = circle(grid_uv, vec2(grid_spacing/2.0), dot_size, 1.0);
                    
                    vec3 color = mix(color_accent1, color_accent2, fract(v_text.x + time * 0.1 + mids * 0.5));
                    
                    f_color = vec4(color * c + color_primary * (1.0 - c), 1.0);
                }
            """
        )
        self.program['resolution'].value = (WIDTH, HEIGHT)
        self.program['color_primary'].value = (PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
        self.program['color_accent1'].value = (ACCENT1[0]/255.0, ACCENT1[1]/255.0, ACCENT1[2]/255.0)
        self.program['color_accent2'].value = (ACCENT2[0]/255.0, ACCENT2[1]/255.0, ACCENT2[2]/255.0)
        self.vao = self.get_fullscreen_quad(self.program)

    def load_preset(self, preset_data):
        if "parameters" in preset_data:
            for key, value in preset_data["parameters"].items():
                if key in self.program:
                    self.program[key].value = value

    def draw(self, screen, bass, mids, highs, fft_data):
        self.ctx.clear(PRIMARY[0]/255.0, PRIMARY[1]/255.0, PRIMARY[2]/255.0)
        self.program['time'].value = self.time
        self.program['bass'].value = bass
        self.program['mids'].value = mids
        self.program['highs'].value = highs
        self.vao.render(moderngl.TRIANGLE_STRIP)

# --- MILKDROP ENGINE ---
class MilkdropEngine(ShaderEngine):
    def __init__(self, context):
        super().__init__(context)
        self.name = "Milkdrop Engine"

        # Default parameters
        self.zoom_amount = 0.05
        self.color_r = 0.1
        self.color_g = 0.0
        self.color_b = 0.05

        # Create two textures and two framebuffers for the feedback loop
        self.texture_a = self.ctx.texture((WIDTH, HEIGHT), 4, dtype='f4')
        self.texture_b = self.ctx.texture((WIDTH, HEIGHT), 4, dtype='f4')
        self.fbo_a = self.ctx.framebuffer(color_attachments=[self.texture_a])
        self.fbo_b = self.ctx.framebuffer(color_attachments=[self.texture_b])

        # 1. WARP SHADER
        self.warp_program = self.ctx.program(
            vertex_shader=fullscreen_quad_vs,
            fragment_shader="""
                #version 330
                in vec2 v_text;
                out vec4 f_color;
                uniform float fTime, fBass, fMid, fTreb;
                uniform float zoom_amount;
                uniform sampler2D txPrevFrame;
                void main() {
                    vec2 uv = v_text;
                    vec2 centered_uv = uv - 0.5;

                    // Time-based rotation
                    float angle = fTime * 0.05;
                    mat2 rotation = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
                    centered_uv = rotation * centered_uv;

                    // Zoom effect
                    float zoom = 0.99 + (fBass * zoom_amount);
                    vec2 zoomed_uv = centered_uv * zoom;

                    // Add slight perturbations from mid and treb
                    zoomed_uv.x += fMid * 0.01;
                    zoomed_uv.y -= fTreb * 0.01;

                    vec2 final_uv = zoomed_uv + 0.5;
                    f_color = texture(txPrevFrame, final_uv) * 0.98;
                }
            """
        )

        # 2. COMPOSITE SHADER
        self.comp_program = self.ctx.program(
            vertex_shader=fullscreen_quad_vs,
                            fragment_shader="""
                            #version 330
                            in vec2 v_text;
                            out vec4 f_color;
                            uniform float fBass;
                            uniform float color_r, color_g, color_b;
                            uniform sampler2D txWarpedFrame;
                            void main() {
                                vec4 warped_color = texture(txWarpedFrame, v_text);
                                vec3 added_color = vec3(fBass * color_r, fBass * color_g, fBass * color_b);
                                // Add a tiny bit of energy to prevent the feedback loop from dying completely
                                added_color += 0.003;
                                f_color = vec4(warped_color.rgb + added_color, 1.0);
                            }
                        """        )
        self.warp_vao = self.get_fullscreen_quad(self.warp_program)
        self.comp_vao = self.get_fullscreen_quad(self.comp_program)

    def load_preset(self, preset_data):
        if "parameters" in preset_data:
            params = preset_data["parameters"]
            self.zoom_amount = params.get("zoom_amount", 0.05)
            self.color_r = params.get("color_r", 0.1)
            self.color_g = params.get("color_g", 0.0)
            self.color_b = params.get("color_b", 0.05)

    def draw(self, screen, bass, mids, highs, fft_data):
        # --- PASS 1: WARP SHADER ---
        # Render the warped previous frame (from texture_b) into texture_a
        self.fbo_a.use()
        self.texture_b.use(location=0)
        self.warp_program['txPrevFrame'].value = 0
        self.warp_program['fTime'].value = self.time
        self.warp_program['fBass'].value = bass
        self.warp_program['fMid'].value = mids
        self.warp_program['fTreb'].value = highs
        self.warp_program['zoom_amount'].value = self.zoom_amount
        self.warp_vao.render(moderngl.TRIANGLE_STRIP)

        # --- PASS 2: COMPOSITE SHADER ---
        # Render the composite of the warped frame (texture_a) and new shapes into texture_b
        self.fbo_b.use()
        self.texture_a.use(location=1)
        self.comp_program['txWarpedFrame'].value = 1
        self.comp_program['fBass'].value = bass
        self.comp_program['color_r'].value = self.color_r
        self.comp_program['color_g'].value = self.color_g
        self.comp_program['color_b'].value = self.color_b
        self.comp_vao.render(moderngl.TRIANGLE_STRIP)

        # --- FINAL BLIT TO SCREEN ---
        # The final image for this frame is now in texture_b (via fbo_b).
        # We copy it to the screen. The screen is the default framebuffer.
        self.ctx.copy_framebuffer(self.ctx.screen, self.fbo_b)
        # texture_b now correctly holds the final image of this frame,
        # making it the correct 'previous frame' for the next draw call.

# Preset Manager
class PresetManager:
    def __init__(self, presets_dir="milk_presets"):
        self.presets_dir, self.presets, self.current_idx = presets_dir, [], 0
        self.load_presets()

    def load_presets(self):
        if os.path.exists(self.presets_dir):
            for file in sorted(os.listdir(self.presets_dir)):
                if file.endswith('.milk'):
                    try:
                        with open(os.path.join(self.presets_dir, file), 'r') as f:
                            preset_data = json.load(f)
                            self.presets.append(preset_data)
                        print(f"[+] Loaded: {preset_data.get('name', file)}")
                    except Exception as e:
                        print(f"[-] Failed to load {file}: {e}")

    def get_current(self):
        return self.presets[self.current_idx] if self.presets else None

    def next(self):
        if not self.presets: return
        self.current_idx = (self.current_idx + 1) % len(self.presets)
        print(f"-> Preset: {self.get_current()['name']}")

    def prev(self):
        if not self.presets: return
        self.current_idx = (self.current_idx - 1 + len(self.presets)) % len(self.presets)
        print(f"<- Preset: {self.get_current()['name']}")

# --- Engine and Preset Setup ---
engine_map = {
    "spectrum_bars": SpectrumBars,
    "radial_waves": RadialWaves,
    "dotgrid": DotGrid,
    "milkdrop": MilkdropEngine
    # Add other engine types here as they are implemented
}

# Instantiate all available engines
engines = {name: cls(ctx) for name, cls in engine_map.items()}

preset_manager = PresetManager(presets_dir=resource_path('assets/milk_presets' if not getattr(sys, 'frozen', False) else 'milk_presets'))
current_engine = engines["dotgrid"] # Default engine

# Main loop
running = True
clock = pygame.time.Clock()

# Pygame font for UI - must be initialized after pygame.init()
pygame.font.init()
font_large = pygame.font.SysFont(None, 56, bold=True)
font_small = pygame.font.SysFont(None, 32)
font_tiny = pygame.font.SysFont(None, 24)

# --- UI Rendering Setup ---
ui_program = ctx.program(
    vertex_shader='''
        #version 330
        in vec2 in_vert;
        in vec2 in_uv;
        out vec2 v_uv;
        uniform vec2 ui_pos;
        uniform vec2 ui_size;
        uniform vec2 screen_size;
        void main() {
            v_uv = in_uv;
            // Pygame surfaces have (0,0) at top-left, but OpenGL textures have (0,0) at bottom-left.
            // So we flip the y-coordinate of the UVs.
            
            vec2 pos = in_vert * ui_size + ui_pos;
            vec2 ndc = (pos / screen_size) * 2.0 - vec2(1.0, 1.0);
            gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330
        in vec2 v_uv;
        out vec4 f_color;
        uniform sampler2D ui_texture;
        void main() {
            f_color = texture(ui_texture, v_uv);
        }
    '''
)
ui_program['screen_size'].value = (WIDTH, HEIGHT)

ui_vertices = np.array([0, 0, 1, 0, 0, 1, 1, 1], dtype='f4')
ui_vbo_vert = ctx.buffer(ui_vertices.tobytes())
ui_uvs = np.array([0, 1, 1, 1, 0, 0, 1, 0], dtype='f4')
ui_vbo_uv = ctx.buffer(ui_uvs.tobytes())

ui_vao_content = [
    (ui_vbo_vert, '2f', 'in_vert'),
    (ui_vbo_uv, '2f', 'in_uv')
]
ui_vao = ctx.vertex_array(ui_program, ui_vao_content)
ui_texture = None # Will be created on the fly

def update_engine_from_preset():
    global current_engine
    preset = preset_manager.get_current()
    if preset:
        preset_type = preset.get("type")
        engine_to_use = engines.get(preset_type)
        if engine_to_use:
            current_engine = engine_to_use
            # Pass preset parameters to the engine if it has a method to accept them
            if hasattr(current_engine, 'load_preset'):
                current_engine.load_preset(preset)
            print(f"Switched to engine: {current_engine.name} for preset: {preset['name']}")
        else:
            print(f"No engine found for preset type: {preset_type}")

update_engine_from_preset() # Set initial engine

while running:
    dt = clock.tick(120) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.JOYBUTTONDOWN and joystick:
            print(f"DEBUG: JOYBUTTONDOWN event received. button={event.button}")
            if event.button == ControllerButton.A.value:
                print("DEBUG: 'A' button detected. Changing to next preset.")
                preset_manager.next()
                update_engine_from_preset()
            elif event.button == ControllerButton.B.value:
                print("DEBUG: 'B' button detected. Changing to previous preset.")
                preset_manager.prev()
                update_engine_from_preset()
            elif event.button == ControllerButton.Y.value:
                pass  # Reserved
            else:
                print(f"DEBUG: Unmapped controller button pressed: {event.button}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                preset_manager.next()
                update_engine_from_preset()


    # Audio Processing
    if np.any(audio_data):
        fft_data = np.abs(fft(audio_data))[:BLOCK_SIZE//2]
        # Normalize, avoiding division by zero
        max_val = np.max(fft_data)
        if max_val > 0: fft_data /= max_val
    else:
        fft_data = np.zeros(BLOCK_SIZE//2)

    # Calculate frequency bands
    raw_bass = np.mean(fft_data[5:16])
    raw_mids = np.mean(fft_data[16:64])
    raw_highs = np.mean(fft_data[64:128])
    
    # Smooth the values
    smooth_bass = smooth_bass * audio_smoothing + raw_bass * (1 - audio_smoothing)
    smooth_mids = smooth_mids * audio_smoothing + raw_mids * (1 - audio_smoothing)
    smooth_highs = smooth_highs * audio_smoothing + raw_highs * (1 - audio_smoothing)
    
    # Clamp to prevent instability from feedback
    bass, mids, highs = min(smooth_bass, 1.0), min(smooth_mids, 1.0), min(smooth_highs, 1.0)

    # --- Render active engine ---
    current_engine.update(dt)
    
    # The draw call now handles its own screen clearing or framebuffer logic
    current_engine.draw(screen, bass, mids, highs, fft_data)

    # --- UI Overlay ---
    preset = preset_manager.get_current()
    preset_name = preset['name'] if preset else "None"
    
    # Create a semi-transparent surface for the UI background
    info_surface = pygame.Surface((450, 150), pygame.SRCALPHA)
    info_surface.fill((10, 10, 15, 200))

    # Render text
    preset_text = font_large.render(preset_name, True, (255, 255, 255))
    engine_text = font_small.render(f"Engine: {current_engine.name}", True, (200, 200, 200))
    fps = clock.get_fps()
    fps_text = font_small.render(f"FPS: {fps:.2f}", True, (200, 200, 200))
    
    # Blit text onto the info surface
    info_surface.blit(preset_text, (20, 10))
    info_surface.blit(engine_text, (20, 70))
    info_surface.blit(fps_text, (20, 100))
    
    # Create/update the ModernGL texture from the Pygame surface
    ui_size = info_surface.get_size()
    
    texture_data = pygame.image.tostring(info_surface, 'RGBA', False)

    if ui_texture is None or ui_texture.size != ui_size:
        if ui_texture: ui_texture.release()
        ui_texture = ctx.texture(ui_size, 4, texture_data)
    else:
        ui_texture.write(texture_data)
    
    # Render the UI texture
    ctx.enable(moderngl.BLEND)
    ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
    ui_texture.use(location=0)
    ui_program['ui_texture'].value = 0
    ui_program['ui_pos'].value = (20, 20)
    ui_program['ui_size'].value = ui_size
    ui_vao.render(moderngl.TRIANGLE_STRIP)

    pygame.display.flip()

# Cleanup
stream.stop()
pygame.quit()

