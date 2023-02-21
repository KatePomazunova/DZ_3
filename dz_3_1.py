import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging


parser = argparse.ArgumentParser(description="App for sort")
parser.add_argument("-s", "--source", required=True)
parser.add_argument("-o", "--output", required="dist")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

folders = []

def grabs_folder(path: Path):
    for el in path.iterdir():
        threads=[]
        if el.is_dir():
            folders.append(el)
            th = Thread(target=grabs_folder, args=(el,))
            print(th)
            th.start()
            threads.append(th)
            print(threads)

    [th.join() for th in threads]
            

def sort_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = "new" + el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logging.error(e)
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    grabs_folder(base_folder)

    threads=[]

    for folder in folders:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print(f'-------Sorted files copied to {output_folder}-------')