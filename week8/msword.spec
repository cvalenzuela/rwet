# -*- mode: python -*-

block_cipher = None


a = Analysis(['msword.py', 'msword.spec'],
             pathex=['/Users/cristobalvalenzuela/Dropbox/itp/spring2017/rwet/work/week8'],
             binaries=[],
             datas=[('data/supreme.conversations.txt', 'data')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='msword',
          debug=True,
          strip=False,
          upx=True,
          console=True , icon='app.icns')
app = BUNDLE(exe,
             name='msword.app',
             icon='app.icns',
             bundle_identifier=None)
