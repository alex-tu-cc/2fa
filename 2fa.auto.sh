#!/bin/bash
#
# If you have your 2fa.py data files on a USB disk, this can be used to
# make it type in your next passcode for you.  After setting up 2fa.py to
# get its data from USB and creating a profile called 'usb', bind a hotkey
# in your window manager to run this script.
#
# Then when you need a new passcode, simply do the following:
#   - Plug in your USB disk.
#   - Press the hotkey you configured.
#   - Remove your USB disk.
# The passcode will be entered for you into whatever window is focused.
#
# Requires the 'xmacro' package in Ubuntu.
#

PROFILE=usb  # set your default profile here
if [ x"$1" != x ]; then PROFILE="$1" ; fi

sleep 0.5  # to give the user time to release the hotkey
xmacroplay-keys :0 $(2fa $PROFILE | sed 's/\([0-9]\)/\1 /g;' ; echo Return) \
  > /dev/null 2>/dev/null
