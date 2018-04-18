# -*- mode: python -*-

block_cipher = None


a = Analysis(['passthief.py'],
             pathex=['/home/zvonimir/Desktop/Exploits/passthief/src'],
             binaries=[],
             datas=[],
# First standard then 3rd party
             hiddenimports=['os','sys','argparse','urlparse','platform','importlib','colorama','sqlite3','xml.etree.ElementTree','win32crypt','modules','binascii','subprocess','base64','hashlib'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['modules'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='passthief',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
