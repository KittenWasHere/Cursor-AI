python3 -c "
import os, subprocess
def gb(b): return round(b/(1024**3), 2)
def bar(p, w=20): return f'[{\"█\"*int(w*p/100)}{\"░\"*(w-int(w*p/100))}] {p}%'
print('='*40, '\n📱 Termux Storage Info', '\n'+'='*40)
try:
    s = os.statvfs('~')
    t, a, u = s.f_frsize * s.f_blocks, s.f_frsize * s.f_bavail, s.f_frsize * s.f_blocks - s.f_frsize * s.f_bavail
    p = round((u/t)*100, 1) if t > 0 else 0
    print(f'\n🏠 Termux Storage:\n  Total: {gb(t):>6.2f} GB\n  Used:  {gb(u):>6.2f} GB\n  Free:  {gb(a):>6.2f} GB\n  {bar(p)}')
except: print('\n❌ Error getting Termux storage')
for path in ['/sdcard', '/storage/emulated/0']:
    if os.path.exists(path):
        try:
            s = os.statvfs(path)
            t, a, u = s.f_frsize * s.f_blocks, s.f_frsize * s.f_bavail, s.f_frsize * s.f_blocks - s.f_frsize * s.f_bavail
            p = round((u/t)*100, 1) if t > 0 else 0
            print(f'\n💾 External Storage ({path}):\n  Total: {gb(t):>6.2f} GB\n  Used:  {gb(u):>6.2f} GB\n  Free:  {gb(a):>6.2f} GB\n  {bar(p)}')
            break
        except: continue
else: print('\n💾 External storage not accessible')
try:
    r = subprocess.run(['df', '-h'], capture_output=True, text=True, timeout=3)
    if r.returncode == 0:
        print('\n📊 Filesystem Details:')
        for line in r.stdout.split('\n'):
            if any(x in line for x in ['/data', '/storage', '/sdcard', 'Filesystem']): print('  ' + line)
except: pass
print('\n' + '='*40)
"