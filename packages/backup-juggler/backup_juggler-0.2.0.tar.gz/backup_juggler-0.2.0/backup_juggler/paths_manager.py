from pathlib import Path


class Paths:
    """
    Model class for the Backup Juggler application.

    Attributes:
        _source: The source directory or file path.
        _destination: The destination directory.
        _total_size: The total size of the files to be copied.

    Methods:
        - source: Get the source path.
        - destination: Get the destination directory.
        - total_size: Get the total size of the files to be copied.

    Notes:
        - The total size calculation includes subdirectories and files within the source directory.
        - The total size is calculated only once during the initialization of the `Paths` instance.
    """

    def __init__(self, source: Path, destination: Path = None) -> None:
        """
        Initialize a `Paths` instance.

        Args:
            source: The source directory or file path.
            destination: The destination directory. Defaults to `None`.
        """

        self._source: Path = source
        self._destination: Path = destination
        if self.source.is_file():
            self._total_size: int = self.source.stat().st_size
        else:
            self._total_size: int = sum(
                src_file.stat().st_size
                for src_file in self.source.rglob('*.*')
            )

    @property
    def source(self) -> Path:
        """
        Get the source path.

        Returns:
            _source: The source path.
        """

        return self._source

    @property
    def destination(self) -> Path:
        """
        Get the destination directory.

        Returns:
            _destination: The destination directory.
        """

        return self._destination

    @property
    def total_size(self) -> int:
        """
        Get the total size of the files to be copied.

        Returns:
            _total_size: The total size in bytes.
        """

        return self._total_size
