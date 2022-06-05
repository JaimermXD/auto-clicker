import argparse
from pynput import mouse
from pynput import keyboard

from autoclicker import AutoClicker


def parse_button(arg, parser):
    button = None

    try:
        button = mouse.Button[arg]
    except KeyError:
        parser.error(f"invalid mouse button: {arg}")

    return button


def parse_key(arg, parser):
    key = None

    try:
        key = keyboard.Key[arg]
    except KeyError:
        try:
            keyboard.HotKey.parse(arg)
            key = keyboard.KeyCode(char=arg)
        except ValueError:
            parser.error(f"invalid key: {arg}")

    return key


def parse_args():
    parser = argparse.ArgumentParser(prog="auto-clicker", description="Automatically click mouse buttons or press keys")
    parser.add_argument("-m", "--mouse", help="set the mouse button to click")
    parser.add_argument("-k", "--key", help="set the key to press")
    parser.add_argument("-t", "--toggle", help="set the key to toggle the program")
    parser.add_argument("-x", "--exit", help="set the key to exit the program")
    parser.add_argument("-d", "--delay", type=int, help="set the delay between each mouse click or key press (in milliseconds)")
    args = parser.parse_args()

    button = None
    press_key = None
    toggle_key = None
    exit_key = None
    delay = None

    if args.mouse is not None and args.key is not None:
        parser.error("cannot both click a mouse button and press a key")

    if args.mouse is None and args.key is None:
        button = mouse.Button.left

    if args.mouse is not None:
        button = parse_button(args.mouse, parser)

    if args.key is not None:
        press_key = parse_key(args.key, parser)

    if args.toggle is None:
        toggle_key = parse_key("x", parser)
    else:
        toggle_key = parse_key(args.toggle, parser)

    if args.exit is None:
        exit_key = parse_key("z", parser)
    else:
        exit_key = parse_key(args.exit, parser)

    if args.delay is None:
        delay = 1
    else:
        if args.delay < 1:
            parser.error("delay must be greater than or equal to 1")

        delay = args.delay

    return button, press_key, toggle_key, exit_key, delay


def main():
    args = parse_args()
    button, press_key, toggle_key, exit_key, delay = args
    print(f"Button        {button}")
    print(f"Key to press  {press_key}")
    print(f"Toggle key    {toggle_key}")
    print(f"Exit key      {exit_key}")
    print(f"Delay         {delay} ms")

    if button is not None:
        auto_clicker = AutoClicker(button, delay)
    else:
        auto_clicker = AutoClicker(press_key, delay, False)

    auto_clicker.start()

    def on_press(key_pressed):
        if key_pressed == toggle_key:
            auto_clicker.toggle()
        elif key_pressed == exit_key:
            auto_clicker.exit()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
