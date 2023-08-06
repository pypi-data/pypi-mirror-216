from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='consumableai',
    version='1.0.2',
    packages=['consumableai'],
    entry_points={
        'console_scripts': [
            'consumableai=consumableai.cli:main',
        ],
    },
    scripts=['consumableai/cli.py'],
    install_requires=[
        'pandas',
        'pyyaml',
        "click",
        "psycopg2-binary",
        "requests",
        "pathlib"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
