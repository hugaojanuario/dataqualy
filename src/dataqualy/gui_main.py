from multiprocessing import freeze_support

from dataqualy.gui import launch_gui


def main() -> None:
    """Entrada exclusiva do executável desktop."""
    freeze_support()
    launch_gui()


if __name__ == "__main__":
    main()


# @hugaojanuario
