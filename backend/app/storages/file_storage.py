from pathlib import Path


class FileStorage:
    def __init__(
        self,
        base_path: str,
    ):
        self.base_path = Path(base_path)

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save(
        self,
        filename: str,
        content: bytes,
    ) -> str:
        file_path = self.base_path / filename

        file_path.write_bytes(content)

        return str(file_path)

    async def read(
        self,
        path: str,
    ) -> str:
        return Path(path).read_text()
