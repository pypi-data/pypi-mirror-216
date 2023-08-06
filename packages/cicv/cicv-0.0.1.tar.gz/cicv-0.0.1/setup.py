from setuptools import setup

setup(
    name='cicv',
    version='0.0.1',
    author='Max Chang',
    author_email='p513817@gmail.com',
    description='A common interface for opencv',
    packages=['cicv'],
    install_requires=[
        "opencv-python",
        # List any dependencies your package requires
    ],
)