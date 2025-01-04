import sys
import threading

def excepthook(etype, value, tb):
    # will be fast to load this module
    import traceback
    import time
    import os.path
    from ctypes import windll
    
    try:
        if isinstance(etype, KeyboardInterrupt) or KeyboardInterrupt in etype.mro():
            print("^C")
            windll.kernel32.ExitProcess(0)
        
        errortext = "".join(traceback.format_exception(etype, value, tb))
        errorfile = f"error_{time.time()}.txt"
        with open(errorfile, "w", encoding="utf-8") as f:
            f.write(errortext)
        
        print(errortext, end="")
        windll.user32.MessageBoxW(
            0, f"很抱歉, MaimaiPlayer 发生了错误\n已生成错误文件到: {os.path.abspath(errorfile)}\n请将错误文件发送给开发者以获得帮助\nhttps://github.com/qaqFei/MaimaiPlayer\n\n\n{errortext}",
            "MaimaiPlayer 发生错误", 0x00000010 | 0x00010000
        )
        windll.kernel32.ExitProcess(0)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        windll.kernel32.ExitProcess(0)

sys.excepthook = excepthook
threading.excepthook = lambda x: excepthook(x.exc_type, x.exc_value, x.exc_traceback)
