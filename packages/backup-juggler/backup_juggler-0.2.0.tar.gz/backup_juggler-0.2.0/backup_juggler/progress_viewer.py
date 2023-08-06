from typing import Any

from tqdm import tqdm

from backup_juggler.paths_manager import Paths


class ProgressViewer:
    """
    View class for the Backup Juggler application.

    Attributes:
        _pbar: The progress bar instance.

    Methods:
        - _update: Update the progress bar with the given chunk size.

    Notes:
        - The progress bar is created using the `tqdm` library.
        - The progress bar updates are performed in the `_update` method.
    """

    def __init__(self, paths: Paths) -> None:
        """
        Initialize a `ProgressViewer` instance.

        Args:
            paths: The `Paths` instance.
        """

        self._pbar: Any = tqdm(
            total=paths.total_size,
            unit='B',
            unit_scale=True,
            desc=f'Copying {paths.source.name} to {paths.destination.name}',
        )

    def _update(self, chunk_size: int) -> None:
        """
        Update the progress bar with the given chunk size.

        Args:
            chunk_size: The size of the chunk to update the progress.
        """

        self._pbar.update(chunk_size)
