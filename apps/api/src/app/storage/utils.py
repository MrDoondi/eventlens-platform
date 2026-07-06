from pathlib import Path
from uuid import uuid4

from PIL import Image


def generate_filename(
    original_filename: str,
) -> str:
    extension = Path(
        original_filename,
    ).suffix.lower()

    return f"{uuid4()}{extension}"


def generate_thumbnail(
    source: Path,
    destination: Path,
    size: tuple[int, int] = (400, 400),
) -> None:

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with Image.open(source) as image:

        image.thumbnail(size)

        image.save(
            destination,
            optimize=True,
            quality=85,
        )