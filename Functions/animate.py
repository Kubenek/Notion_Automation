import time
import sys

def animate(done, text):
    while not done[0]:
        for symbol in ['|', '/', '-', '\\']:
            sys.stdout.write(f'\r{text} {symbol}')
            sys.stdout.flush()
            time.sleep(0.1)
