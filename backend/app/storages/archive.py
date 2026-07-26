import io
import zipfile


class ZipExtractor:
    def extract(
        self,
        archive: bytes,
    ) -> dict[str, bytes]:

        result = {}

        with zipfile.ZipFile(io.BytesIO(archive)) as zip_file:
            for filename in zip_file.namelist():
                result[filename] = zip_file.read(filename)

        return result
