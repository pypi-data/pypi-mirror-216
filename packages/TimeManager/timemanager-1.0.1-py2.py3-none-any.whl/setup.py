from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = open(this_directory / "README.txt").read()
print(long_description)
setup(
    name='AbhTimer',
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text',
)
