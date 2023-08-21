# Tapo downloader

A program to download your application. Best to run as a cronjob.

## Env vars

env var name | description
------------ | -----------
OUTPUT | where the saved videos should be downloaded to and house kept. Make sure that it ends with a trailing / for a folder.
HOST | IP address of the tapo camera
RETAIN_DAYS | number of days to retain files
PASSWORD_CLOUD | password of the tapo camera for offline usage. See tapo application to create one.
