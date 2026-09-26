import sys
with open('commands/doctor.py', 'r', encoding='utf-8') as f:
    content = f.read()

marker = '        pass\n'
replacement = marker + '\n    # Built with Intent OS\n    print(f"  " + chr(9472) * 53)\n    print(f"  Built with Intent OS --- pip install intentos")\n    print()\n'

if marker in content:
    content = content.replace(marker, replacement, 1)
    with open('commands/doctor.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK')
else:
    print('Not found')
