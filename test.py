import os
import sys
from pathlib import Path

# 1. 检查 Python 架构
print(f"Python: {sys.version} ({'64-bit' if sys.maxsize > 2**32 else '32-bit'})")

# 2. 检查 PySide6 路径
try:
    from PySide6 import QtCore
    print(f"✅ PySide6 loaded: {QtCore.__file__}")
    print(f"✅ Qt version: {QtCore.qVersion()}")
    
    # 3. 检查关键 DLL 是否可访问
    pyside_dir = Path(QtCore.__file__).parent
    dlls = ["Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll"]
    for dll in dlls:
        p = pyside_dir / dll
        print(f"{'✅' if p.exists() else '❌'} {dll}: {p}")
    
    # 4. 检查平台插件
    plugins = pyside_dir / "plugins" / "platforms" / "qwindows.dll"
    print(f"{'✅' if plugins.exists() else '❌'} qwindows.dll: {plugins}")

except Exception as e:
    print(f"❌ ImportError: {e}")
    import traceback
    traceback.print_exc()