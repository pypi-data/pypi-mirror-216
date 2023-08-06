import os
import click
import pandas as pd
from tabulate import tabulate
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ParquetFileEventHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            self.print_parquet_file()

    def print_parquet_file(self):
        try:
            df = pd.read_parquet(self.file_path)
            os.system('clear')
            print(tabulate(df.head(5), headers='keys', tablefmt='grid'))
        except Exception as e:
            print(f"Error reading Parquet file: {e}")

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def read_parquet(file_path):
    """Read a Parquet file and continuously display its contents."""
    event_handler = ParquetFileEventHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            event_handler.print_parquet_file()
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    read_parquet()