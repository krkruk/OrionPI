from bin.main import Main
import os


if __name__ == "__main__":
    absolute_path = os.path.abspath(__file__)
    directory = os.path.dirname(absolute_path)
    os.chdir(directory)

    Main().run()
