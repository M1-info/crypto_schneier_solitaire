from multiprocessing import Process

from ui.UISolitary import UISolitary

def main():
    UI = UISolitary()
    process_wait = Process(target=UI.on_wait_for_deck)
    process_wait.start()
    process_ui = Process(target=UI.run_ui, args=(process_wait,))
    process_ui.start()

if __name__ == "__main__":
    main()