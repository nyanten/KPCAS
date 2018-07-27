# -*- mode: python -*-

block_cipher = None


a = Analysis(['KPCAS_beta.py'],
             pathex=['/Users/nyanten/Documents/Documents /killtime2/RealPython/OC'],
             binaries=[],
             datas=[],
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
          name='KPCAS_beta',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='kp.icns')
app = BUNDLE(exe,
             name='KPCAS_beta.app',
             icon='kp.icns',
             bundle_identifier=None)
