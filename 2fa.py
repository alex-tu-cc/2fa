#!/usr/bin/env python

"""2fa.py, an easy wrapper for oathtool, to generate one-time passwords.
Manages AES key storage and sequence counting.
"""

import os
import subprocess  # Requires Python 2.7

OATHTOOL = 'oathtool'
KEY_DIR = os.path.join(os.environ['HOME'], '.2fa')

def main(args):
    mode = 'otp'
    keyname = 'default'
    for a in args:
        if a.startswith('-'):
            return usage()
        else:
            keyname = a

    try:
        key, last_seq = load_key(keyname)
    except IOError:
        mode = 'addkey'

    if mode == 'otp':
        print gen_otp(key, last_seq)
        save_key(keyname, seq=last_seq+1)

    elif mode == 'addkey':
        key, seq = add_key(keyname)
        if key:
            print 'Your first OTP is: %s' % (gen_otp(key, seq))
            save_key(keyname, seq=seq+1)

def usage():
    print 'Usage: 2fa [NAME]'
    print 'Generates the next passcode in the sequence for the NAME profile.'
    print '(will create a new profile on first use)'
    print 'NAME is optional; will be "default" if not specified.'
    print 'Key and sequence data are stored in ~/.2fa/'

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
    usage()
    print
    print 'Creating profile "%s".' % (keyname)
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

