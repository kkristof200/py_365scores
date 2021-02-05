import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = '365scores'

setuptools.setup(
    name="365scores",
    version="1.0.7",
    author="Kristof",
    description="365scores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_365scores",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsoncodable',
        'kcu',
        'ksimpleapi',
        'simple-multiprocessing'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)