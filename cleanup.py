import signal
import sys
import time

_cleanup_callback = None


def set_cleanup_callback(cc):
    global _cleanup_callback
    signal.signal(signal.SIGINT, signal_handler)
    _cleanup_callback = cc


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    if _cleanup_callback:
        print('Cleaning up...')
        _cleanup_callback()
    print('Now exit.')
    sys.exit(0)
