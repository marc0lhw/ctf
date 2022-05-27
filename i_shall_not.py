filename = '''/pack/Png/alpha.png
/pack/Png/beta.png
/pack/Png/delta.png
/pack/Png/easpq.png
/pack/Png/fmoews.png
/pack/Png/gama.png
/pack/Png/gkreoq.png
/pack/Png/htqows.png
/pack/Png/kgtre.png
/pack/Png/relwpq.png
/pack/Png/rfeko.png
/pack/Png/tplrpe.png
/pack/Png/true.png'''.split('\n')


cmds = '''/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/fmoews.png
/pack/Png/alpha.png
/
/pack/Png/relwpq.png
/pack/Png/beta.png
/
/pack/Png/fmoews.png
/pack/Png/alpha.png
/
/pack/Png/kgtre.png
/pack/Png/rfeko.png
/
/pack/Png/easpq.png
/pack/Png/rfeko.png
/
/pack/Png/fmoews.png
/pack/Png/alpha.png
/
/pack/Png/kgtre.png
/pack/Png/gkreoq.png
/
/pack/Png/kgtre.png
/pack/Png/tplrpe.png
/
/pack/Png/rfeko.png
/
/pack/Png/rfeko.png
/
/pack/Png/htqows.png
/pack/Png/rfeko.png
/
/pack/Png/htqows.png
/pack/Png/kgtre.png
/
/pack/Png/kgtre.png
/pack/Png/alpha.png
/
/pack/Png/kgtre.png
/pack/Png/htqows.png
/
/pack/Png/delta.png
/pack/Png/gkreoq.png
/
/pack/Png/easpq.png
/pack/Png/alpha.png
/
/pack/Png/gama.png
/pack/Png/delta.png
/
/pack/Png/gkreoq.png
/pack/Png/gkreoq.png
/
/pack/Png/gama.png
/pack/Png/gama.png
/
/pack/Png/easpq.png
/pack/Png/gkreoq.png
/
/pack/Png/gama.png
/pack/Png/beta.png
/
/pack/Png/gkreoq.png
/pack/Png/fmoews.png
/
/pack/Png/relwpq.png
/pack/Png/gkreoq.png
/
/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/easpq.png
/pack/Png/true.png
/
/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/easpq.png
/pack/Png/true.png
/
/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/easpq.png
/pack/Png/true.png
/
/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/easpq.png
/pack/Png/true.png
/
/pack/Png/htqows.png
/pack/Png/htqows.png
/
/pack/Png/easpq.png
/pack/Png/true.png
/
/pack/Png/kgtre.png
/pack/Png/alpha.png
/
/pack/Png/fmoews.png
/pack/Png/alpha.png
/
/pack/Png/relwpq.png
/pack/Png/beta.png
/
/pack/Png/easpq.png
/pack/Png/rfeko.png
/
/pack/Png/easpq.png
/pack/Png/relwpq.png
/
/pack/Png/kgtre.png
/pack/Png/rfeko.png
/
/pack/Png/relwpq.png
/pack/Png/kgtre.png
/
/pack/Png/easpq.png
/pack/Png/alpha.png
/
/pack/Png/rfeko.png
/'''.split('\n')

print cmds

charset = '0123456789abcdef'

cmd = ''
tt = ''
for i in cmds:
    if i != '/':
        tt += charset[filename.index(i)]
    else:
        cmd += chr(int(tt, len(filename)))
        tt = ''

print cmd
