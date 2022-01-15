import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metadata_mp3",
    version="1.1",
    license="MIT",
    description="small package to manage MP3 metadata using mutagen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bartek56/metadata_mp3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['mutagen'],
    python_requires='>=3.6',
)
