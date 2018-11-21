# Youtube Transcription downloader

A fast downloader for youtube transcripts.
Download transcripts from:
  - Specific video
  - Playlist
  - List of videos.

## Dependencies
Depending on the browser you want to use check the [Selenium Driver Documentation](https://selenium-python.readthedocs.io/installation.html#drivers) and ensure you have the required drivers.
Tested python 2 & 3

## Running

```
$ youtube-transcript-downloader.py [-h] [--output OUTPUT] [--wait WAIT]
                           [--language LANGUAGE] [--retries RETRIES] [--quiet]
                           [--browser [0-3]]
                           link
Arguments:
  link                 Full path to target, could be url or local file (urls
                       separated by lines). If url start with "http".

optional arguments:
  -h, --help           show this help message and exit
  --output OUTPUT      Output file, if none given it will be printed to
                       standart output.
  --wait WAIT          Maximum waiting time in seconds in between actions.
  --language LANGUAGE  Prefered caption language. If not found then get auto-
                       generated.
  --retries RETRIES    Number of retries if error happens.
  --quiet              Don't show browser window.
  --browser [0-3]      Which browser to use. 
                        0: Firefox
                        1: Chrome 
                        2: Ie
                        3: Opera

```