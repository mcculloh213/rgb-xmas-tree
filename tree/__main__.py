from tree import TreeController

if __name__ == "__main__":
    import signal
    import sys

    controller = TreeController()

    # noinspection PyUnusedLocal
    def exit_handler(sig, frame):
        print("\nStopping CTC")
        controller.exit()
        controller.sleep()
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGHUP, exit_handler)

    print("Starting CTC")
    controller.run()