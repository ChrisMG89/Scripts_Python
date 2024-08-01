# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

def get_ctk_theme():
    # Aquí especifica la ruta completa al archivo de tema personalizado
    theme_file = "C:\\Users\\chris\\Desktop\\Mis_aplicaciones\\Aplicaciones BBDD\\DataMaster\\orange_theme.json"
    
    # Carga el contenido del archivo del tema
    with open(theme_file, 'r') as f:
        theme = json.load(f)
    return theme

a = Analysis(['Data_Master.py'],
             pathex=[],
             binaries=[],
             datas=[('C:\\Users\\chris\\Desktop\\Mis_aplicaciones\\Aplicaciones BBDD\\DataMaster\\orange_theme.json', 'Data_Master')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='DataMaster',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='combined_icon.ico') 

def post_build():
    # Carga el tema personalizado después de que se haya construido la aplicación
    import customtkinter as ctk
    theme = get_ctk_theme()
    ctk.set_custom_color_theme(theme)

exe.post_build = post_build
