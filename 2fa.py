#!/usr/bin/env python

import os
import subprocess

OATHTOOL = 'oathtool'
KEY_DIR = os.path.join(os.environ['HOME'], '.2fa')

def main(args):
    mode = 'otp'
    keyname = 'default'
    for a in args:
        keyname = a

    try:
        key, last_seq = load_key(keyname)
    except IOError:
        mode = 'addkey'

    if mode == 'otp':
        print gen_otp(key, last_seq)
        save_key(keyname, seq=last_seq+1)

    elif mode == 'addkey':
        add_key(keyname)

def load_key(keyname):
    key = open(os.path.join(KEY_DIR, keyname, 'key')).readline().strip()
    seq = int(open(os.path.join(KEY_DIR, keyname, 'seq')).readline().strip())
    return key, seq

def save_key(keyname, key=None, seq=None):
    if not os.path.exists(KEY_DIR):
        os.mkdir(KEY_DIR)
        subprocess.check_call(['chmod', '700', KEY_DIR])
    if not os.path.exists(os.path.join(KEY_DIR, keyname)):
        os.mkdir(os.path.join(KEY_DIR, keyname))
    if key:
        open(os.path.join(KEY_DIR, keyname, 'key'), 'w').write(key)
    if seq is not None:
        open(os.path.join(KEY_DIR, keyname, 'seq'), 'w').write(str(seq))

def add_key(keyname):
    print 'Adding a key for "%s" profile.' % (keyname)
    key = raw_input('Paste the shared AES key from SSO: ')
    key = key.strip().replace(' ', '')
    seq = 0
    save_key(keyname, key, seq)
    return key, seq

def gen_otp(key, seq):
    text = subprocess.check_output([OATHTOOL, '-c', str(seq), key])
    return text.strip()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

