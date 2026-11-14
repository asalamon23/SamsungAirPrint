"""Samsung AirPrint Bridge launcher (GPL-3.0 companion to Windows-AirPrint-Bridge)."""
import json
import socket
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

ROOT = Path(__file__).resolve().parent
ENGINE = ROOT / 'airprint_bridge.py'
CONFIG = ROOT / 'config.json'
process = None


def printers():
    import win32print
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    return sorted({p[2] for p in win32print.EnumPrinters(flags) if p[2]})


def ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('1.1.1.1', 80))
            return s.getsockname()[0]
        except OSError:
            return 'unknown'


def save_config():
    name = selected.get().strip()
    if name not in choices:
        messagebox.showerror('Printer required', 'Choose an installed Windows printer.')
        return False
    try:
        cfg = json.loads(CONFIG.read_text(encoding='utf-8')) if CONFIG.exists() else {}
        cfg.update({'printer_name': name, 'max_render_dpi': 300})
        CONFIG.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
        return True
    except Exception as e:
        messagebox.showerror('Configuration error', str(e))
        return False


def start():
    global process
    if process and process.poll() is None:
        return
    if not ENGINE.exists():
        messagebox.showerror('Missing engine', 'Run Setup.ps1 first.')
        return
    if not save_config():
        return
    try:
        log = open(ROOT / 'bridge-console.log', 'ab', buffering=0)
        process = subprocess.Popen([sys.executable, str(ENGINE)], cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        log.close()
        status.set('Starting…')
        root.after(1800, check)
    except Exception as e:
        messagebox.showerror('Start failed', str(e))


def check():
    if process and process.poll() is None:
        status.set('Running — iPhone can discover the printer')
    else:
        status.set('Stopped / startup failed — see airprint_bridge.log')


def stop():
    global process
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=4)
        except subprocess.TimeoutExpired:
            process.kill()
    process = None
    status.set('Stopped')


def close():
    stop()
    root.destroy()


root = tk.Tk()
root.title('Samsung Xpress M2675F — iPhone AirPrint Bridge')
root.geometry('540x290')
root.resizable(False, False)
frame = ttk.Frame(root, padding=22)
frame.pack(fill='both', expand=True)
ttk.Label(frame, text='Samsung → iPhone AirPrint Bridge', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(0, 12))
ttk.Label(frame, text='Choose your USB-connected Samsung printer:').pack(anchor='w')
try:
    choices = printers()
except Exception as e:
    choices = []
    messagebox.showwarning('Printer enumeration failed', str(e))
selected = tk.StringVar(value=next((p for p in choices if '2675' in p.lower()), next((p for p in choices if 'samsung' in p.lower()), choices[0] if choices else '')))
combo = ttk.Combobox(frame, values=choices, textvariable=selected, state='readonly', width=64)
combo.pack(anchor='w', pady=7)
status = tk.StringVar(value='Stopped')
ttk.Label(frame, text=f'PC local IP: {ip_address()}   |   IPP port: 631').pack(anchor='w', pady=5)
ttk.Label(frame, textvariable=status).pack(anchor='w', pady=5)
buttons = ttk.Frame(frame)
buttons.pack(anchor='w', pady=12)
ttk.Button(buttons, text='Start sharing', command=start).pack(side='left', padx=(0, 10))
ttk.Button(buttons, text='Stop', command=stop).pack(side='left')
ttk.Label(frame, text='iPhone: Share → Print → Printer → select the Samsung bridge.\nKeep this window open. PC and iPhone must be on the same LAN.', foreground='#555').pack(anchor='w')
root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()
