# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'ofx_currency_converter.py', os.path.join(HOMEPATH,'support\\removeTK.py')],
             pathex=['C:\\Documents and Settings\\Administrator\\Desktop\\ofx_currency_converter'])

a.datas += [('templates/template.ofx', 'C:\\Documents and Settings\\Administrator\\Desktop\\ofx_currency_converter\\templates\\template.ofx',  'DATA'),]

pyz = PYZ(a.pure)
exe = EXE(TkPKG(), pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'ofx_currency_converter.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True )
