from distutils.core import setup
from pathlib import Path

here = Path(__file__).resolve().parent
requirements = [
    stripped_line
    for line in (here / "requirements.txt").read_text().splitlines()
    if (stripped_line := line.strip())
]

description = (
    "A Python library to translate type annotations to `hypothesis` strategies"
)

setup(
    name="type_to_strategy",
    version="0.0.0",
    author="Gorka Eraña",
    requires_python=">3.10",
    description=description.strip(),
    package_dir={"type_to_strategy": "src"},
    install_requires=requirements,
)
