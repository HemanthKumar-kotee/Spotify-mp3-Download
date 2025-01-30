from setuptools import setup, find_packages

requires = [
    'flask',
    'youtube_dl',
    'pathlib',
    'requests_html',
    'beautifulsoup4',
    'requests',
    'spotipy'
]

setup(
    name = 'SpotifyDownload',
    version = '1.0',
    keywords = 'web flask',
    description = 'An Application that get your Spotify songs and download the YoutubeMp3 version',
    packages = find_packages(),
    include_package_data = True,
    install_requires = requires

)