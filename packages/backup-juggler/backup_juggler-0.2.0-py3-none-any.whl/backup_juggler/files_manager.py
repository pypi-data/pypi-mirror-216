import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from backup_juggler.paths_manager import Paths
from backup_juggler.progress_viewer import ProgressViewer

console = Console()


class FileCopier:
    """
    Controller class for the Backup Juggler application.

    Attributes:
        _paths: The `Paths` instance.
        _viewer: The `ProgressViewer` instance.

    Methods:
        - _copy_to: Copy files from source to destination.
        - _copy_file: Copy a single file from source to destination.
    """

    def __init__(self, paths: Paths, viewer: ProgressViewer) -> None:
        """
        Initialize a `FileCopier` instance.

        Args:
            paths: The `Paths` instance.
            viewer: The `ProgressViewer` instance.
        """

        self._paths: Paths = paths
        self._viewer: ProgressViewer = viewer

    def _copy_to(self) -> None:
        """
        Copy files from the source directory to the destination directory.

        Recursively copies files from the source directory to the destination directory,
        preserving the directory structure. If the source is a file, it will be copied directly
        to the destination. If the source is a directory, all files within the directory (including
        subdirectories) will be copied to corresponding paths in the destination.
        """

        if self._paths.source.is_file():
            with self._viewer._pbar:
                src_file: Path = self._paths.source
                dst_file: Path = (
                    self._paths.destination / src_file.stem / src_file.name
                )
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                self._copy_file(src_file, dst_file)
        else:
            with self._viewer._pbar:
                for src_file in self._paths.source.rglob('*.*'):
                    dst_file: Path = (
                        self._paths.destination
                        / self._paths.source.stem
                        / src_file.relative_to(self._paths.source)
                    )
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    self._copy_file(src_file, dst_file)

    def _copy_file(self, src_file: Path, dst_file: Path) -> None:
        """
        Copy a single file from the source to the destination.

        Args:
            src_file: The path of the source file.
            dst_file: The path of the destination file.

        Copies a single file from the source path to the destination path. The file contents are
        read in chunks and written to the destination file. Progress updates are sent to the
        associated `ProgressViewer` instance to update the progress bar.
        """

        with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                dst.write(chunk)
                self._viewer._update(len(chunk))
        os.utime(
            dst_file, (src_file.stat().st_atime, src_file.stat().st_mtime)
        )
        os.chmod(dst_file, src_file.stat().st_mode)


def calculates_size(sources: list[Path]) -> None:
    """
    Calculate the total size of the given source directories.

    Args:
        sources: A list of source directories or file paths.

    This function calculates the total size of the given source directories or files.
    It iterates through the provided list of `Path` objects and sums up the sizes
    of all the sources. The result is then displayed in a human-readable format.

    The size is calculated in bytes and converted to the appropriate unit (B, KB, MB, GB, TB)
    to improve readability. The function automatically selects the most appropriate unit based on the size.

    Examples:
        >>> sources = [Path('path/to/source1'), Path('path/to/source2')]
        >>> calculates_size(sources)
    """

    sources_size = 0
    for source in sources:
        if not source.exists():
            raise FileNotFoundError(f'{source.name} does not exist.')
        model = Paths(source)
        sources_size += model.total_size

    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0

    while sources_size >= 1024 and unit_index < len(size_units) - 1:
        sources_size /= 1024
        unit_index += 1

    size_message = f'Total size: {sources_size:.2f} {size_units[unit_index]}'
    panel = Panel(size_message, expand=False)
    console.print(panel)


def backup(source: Path, destination: Path) -> None:
    """
    Perform a file backup operation from the source path to the destination path.

    Args:
        source: The source directory or file path.
        destination: The destination directory.

    Initiates a file backup operation by creating instances of `Paths`, `ProgressViewer`,
    and `FileCopier` classes. The file copying is performed by calling the `do_copy` method
    of the `FileCopier` instance.

    Raises:
        FileNotFoundError: If a source file or directory does not exist.
    """

    if not source.exists():
        raise FileNotFoundError(f'{source.name} does not exist.')

    paths = Paths(source, destination)
    viewer = ProgressViewer(paths)
    Copier = FileCopier(paths, viewer)
    Copier._copy_to()
    completed_message = (
        f'Backup completed successfully: {source.name} -> {destination.name}'
    )
    panel = Panel(completed_message, border_style='green')
    console.print(panel)


def parallel_backups(sources: list[Path], destinations: list[Path]) -> None:
    """
    Perform multiple file backup operations in parallel.

    Args:
        sources: A list of source directories or file paths.
        destinations: A list of destination directories.

    Examples:
        >>> sources = [Path('path/to/source1'), Path('path/to/source2')]
        >>> destinations = [Path('path/to/destination1'), Path('path/to/destination2')]
        >>> parallel_backups(sources, destinations)

    Initiates multiple file backup operations in parallel using `ThreadPoolExecutor` from
    the `concurrent.futures` module. The `backup` function is submitted as a task to the executor
    for each combination of source and destination paths. The function waits for all tasks to complete
    before returning.
    """
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(backup, source, destination)
            for source in sources
            for destination in destinations
        ]
        for future in as_completed(futures):
            future.result()
