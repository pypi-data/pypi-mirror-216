import setuptools

import versioneer

DESCRIPTION_FILES = ["pypi-intro.rst"]

long_description = []
import codecs
for filename in DESCRIPTION_FILES:
    with codecs.open(filename, 'r', 'utf-8') as f:
        long_description.append(f.read())
long_description = "\n".join(long_description)


setuptools.setup(
    name = "eso-downloader",
    version = versioneer.get_version(),
    packages = setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = [
        "attrs",
        "keyring",
        "platformdirs",
        "pyvo",
        "requests",
        "requests_toolbelt",
    ],
    python_requires = '>=3.7',
    author = "James Tocknell",
    author_email = "james.tocknell@mq.edu.au",
    description = "Downloader for public and proprietary ESO archive data",
    long_description = long_description,
    license = "3-clause BSD",
    keywords = "ESO archive download astronomy astropy",
    url = "https://eso_downloader.readthedocs.io",
    project_urls={
        'Documentation': 'https://eso-downloader.readthedocs.io',
        'Source': 'https://dev.aao.org.au/adacs/eso-downloader/',
        'Tracker': 'https://dev.aao.org.au/adacs/eso-downloader/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points = {
        'console_scripts': [
            "eso-downloader = eso_downloader.cli:main",
        ],
    },
    cmdclass=versioneer.get_cmdclass(),
)
