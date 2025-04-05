# -*- mode: python ; coding: utf-8 -*-

import os

# Obtener la ruta actual del proyecto
current_path = os.getcwd()

a = Analysis(
    ['Main.py'],
    pathex=[
        current_path,
        os.path.join(current_path, 'CapaLogica'),
        os.path.join(current_path, 'CapaDatos')
    ],
    binaries=[],
    datas=[
        ('CapaLogica', 'CapaLogica'),
        ('CapaDatos', 'CapaDatos')
    ],
    hiddenimports=[
        'mysql.connector',
        'mysql.connector.plugins.mysql_native_password',
        'pyodbc',
        'plyer.platforms.win.notification',  # Soporte para notificaciones en Windows
        'plyer.platforms.linux.notification', # Soporte para notificaciones en Linux (si se requiere)
        'plyer.platforms.macosx.notification' # Soporte para notificaciones en macOS (si se requiere)
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambia esto a False para ocultar la consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],  # Ruta del icono para el .exe
)

