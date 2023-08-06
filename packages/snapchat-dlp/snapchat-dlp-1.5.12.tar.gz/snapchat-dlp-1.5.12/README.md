<p>
  <div align="center">
  <h1>
    Snapchat Public Stories Downloader<br /> <br />
    <!-- <a href="https://pypi.python.org/pypi/snapchat-dlp">
      <img
        src="https://img.shields.io/pypi/v/snapchat-dlp.svg?cacheSeconds=360"
        alt="Python Package"
      />
    </a>
    <a href="https://pypi.python.org/pypi/snapchat-dlp">
      <img
        src="https://img.shields.io/pypi/wheel/snapchat-dlp"
        alt="Python Wheel"
      />
    </a>
    <a href="https://pypi.python.org/pypi/snapchat-dlp">
      <img
        src="https://img.shields.io/github/workflow/status/skyme5/snapchat-dlp/build?cacheSeconds=360"
        alt="CI"
      />
    </a>
    <a href="https://codecov.io/gh/skyme5/snapchat-dlp">
      <img
        src="https://img.shields.io/codecov/c/github/skyme5/snapchat-dlp?cacheSeconds=360"
        alt="Code Coverage"
      />
    </a>
    <a href="https://codecov.io/gh/skyme5/snapchat-dlp">
      <img
        src="https://img.shields.io/pypi/pyversions/snapchat-dlp"
        alt="Python Versions"
      />
    </a>
    <a href="https://github.com/psf/black">
      <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="The Uncompromising Code Formatter"
      />
    </a>
    <a href="https://pepy.tech/project/snapchat-dlp">
      <img
        src="https://static.pepy.tech/badge/snapchat-dlp"
        alt="Monthly Downloads"
      />
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img
        src="https://img.shields.io/badge/License-MIT-blue.svg"
        alt="License: MIT"
      />
    </a> -->
  </h1>
</p>

### Installation

Install using pip,

```bash
pip install snapchat-dlp
```

Install from GitHub,

```bash
pip install git+git://github.com/Walmann/snapchat-dlp
```

Unix users might want to add `--user` flag to install without requiring `sudo`.

### Usage

```text

usage: snapchat-dlp [-h] [-c | -u] [-i BATCH_FILENAME] [-P DIRECTORY_PREFIX]
                   [-s] [-d] [-l MAX_NUM_STORY] [-j MAX_WORKERS] [-t INTERVAL]
                   [--sleep-interval INTERVAL] [-q]
                   [username [username ...]]

positional arguments:
  username              At least one or more usernames to download stories
                        for.

optional arguments:
  -h, --help            show this help message and exit
  -c, --scan-clipboard  Scan clipboard for story links
                        ('https://story.snapchat.com/<s>/<username>').
  -u, --check-for-update
                        Periodically check for new stories.
  -i BATCH_FILENAME, --batch-file BATCH_FILENAME
                        Read usernames from batch file (one username per
                        line).
  -P DIRECTORY_PREFIX, --directory-prefix DIRECTORY_PREFIX
                        Location to store downloaded media.
  -s, --scan-from-prefix
                        Scan usernames (as directory name) from prefix
                        directory.
  -d, --dump-json       Save metadata to a JSON file next to downloaded
                        videos/pictures.
  -l MAX_NUM_STORY, --limit-story MAX_NUM_STORY
                        Set maximum number of stories to download.
  -j MAX_WORKERS, --max-concurrent-downloads MAX_WORKERS
                        Set maximum number of parallel downloads.
  -t INTERVAL, --update-interval INTERVAL
                        Set the update interval for checking new story in
                        seconds. (Default: 10m)
  --sleep-interval INTERVAL
                        Sleep between downloads in seconds. (Default: 1s)
  -q, --quiet           Do not print anything except errors to the console.

```
