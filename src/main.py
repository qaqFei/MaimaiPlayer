import err_processer as _
import init_logging as _
import fix_workpath as _
import check_edgechromium as _

import sys
import time
import logging
import typing
from ctypes import windll
from os import popen, listdir, mkdir, environ; environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
from os.path import exists, isfile, isdir
from shutil import rmtree
from tempfile import gettempdir
from ntpath import basename
from threading import Thread

from PIL import Image
from pygame import mixer

import webcv
import playsound
import maimai_obj
import tool_funcs
import mmp_help

if not exists("./7z.exe") or not exists("./7z.dll"):
    logging.fatal("7z.exe or 7z.dll Not Found")
    raise SystemExit

if len(sys.argv) == 1:
    HELP = mmp_help.HELP_EN if windll.kernel32.GetSystemDefaultUILanguage() != 0x804 else mmp_help.HELP_ZH
    print(HELP)
    raise SystemExit

debug = "--debug" in sys.argv
lowquality = "--lowquality" in sys.argv
lowquality_scale = float(sys.argv[sys.argv.index("--lowquality-scale") + 1]) ** 0.5 if "--lowquality-scale" in sys.argv else 2.0 ** 0.5
showfps = "--showfps" in sys.argv
lowquality_imjscvscale_x = float(sys.argv[sys.argv.index("--lowquality-imjscvscale-x") + 1]) if "--lowquality-imjscvscale-x" in sys.argv else 1.0
lowquality_imjs_maxsize = float(sys.argv[sys.argv.index("--lowquality-imjs-maxsize") + 1]) if "--lowquality-imjs-maxsize" in sys.argv else 256
enable_jscanvas_bitmap = "--enable-jscanvas-bitmap" in sys.argv

def Load_Resource():
    Resource = {}
    
    return Resource

def maimaiStart():
    pass

logging.info("Loading Window...")
root = webcv.WebCanvas(
    width = 1, height = 1,
    x = 0, y = 0,
    title = "MaimaiPlayer - Simulator",
    debug = "--debug" in sys.argv,
    resizable = False,
    frameless = "--frameless" in sys.argv,
    renderdemand = "--renderdemand" in sys.argv,
    renderasync = "--renderasync" in sys.argv,
    jslog = "--enable-jslog" in sys.argv,
    jslog_path = sys.argv[sys.argv.index("--jslog-path")] if "--jslog-path" in sys.argv else "./mmp-jslog-nofmt.js"
)

webdpr = root.run_js_code("window.devicePixelRatio;")
if webdpr != 1.0:
    lowquality = True
    lowquality_scale *= 1.0 / webdpr # ...?

if lowquality:
    root.run_js_code(f"lowquality_scale = {lowquality_scale};")

if "--window-host" in sys.argv:
    windll.user32.SetParent(root.winfo_hwnd(), eval(sys.argv[sys.argv.index("--window-host") + 1]))
if "--fullscreen" in sys.argv:
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.web.toggle_fullscreen()
else:
    if "--size" not in sys.argv:
        w, h = int(root.winfo_screenwidth() * 0.6), int(root.winfo_screenheight() * 0.6)
    else:
        w, h = int(eval(sys.argv[sys.argv.index("--size") + 1])), int(eval(sys.argv[sys.argv.index("--size") + 2]))
        
    winw, winh = (
        w if w <= root.winfo_screenwidth() else int(root.winfo_screenwidth() * 0.75),
        h if h <= root.winfo_screenheight() else int(root.winfo_screenheight() * 0.75)
    )
    root.resize(winw, winh)
    w_legacy, h_legacy = root.winfo_legacywindowwidth(), root.winfo_legacywindowheight()
    dw_legacy, dh_legacy = winw - w_legacy, winh - h_legacy
    dw_legacy *= webdpr; dh_legacy *= webdpr
    dw_legacy, dh_legacy = int(dw_legacy), int(dh_legacy)
    del w_legacy, h_legacy
    root.resize(winw + dw_legacy, winh + dh_legacy)
    root.move(int(root.winfo_screenwidth() / 2 - (winw + dw_legacy) / webdpr / 2), int(root.winfo_screenheight() / 2 - (winh + dh_legacy) / webdpr / 2))

root.run_js_code(f"lowquality_imjscvscale_x = {lowquality_imjscvscale_x};")
root.run_js_code(f"lowquality_imjs_maxsize = {lowquality_imjs_maxsize};")
root.run_js_code(f"enable_jscanvas_bitmap = {enable_jscanvas_bitmap};")
root.run_js_code(f"resizeCanvas({w}, {h});")
    
PHIGROS_X, PHIGROS_Y = 0.05625 * w, 0.6 * h
JUDGELINE_WIDTH = h * 0.0075
Resource = Load_Resource()

Thread(target=maimaiStart, daemon=True).start()
root.wait_for_close()

for item in [item for item in listdir(gettempdir()) if item.startswith("qfmmp_cctemp_")]:
    item = f"{gettempdir()}\\{item}"
    try:
        rmtree(item)
        logging.info(f"Remove Temp Dir: {item}")
    except Exception as e:
        logging.warning(e)

windll.kernel32.ExitProcess(0)