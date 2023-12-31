# Reddit SPD
Reddit SPD, or Reddit Saved Post Downloader, is a CLI tool that can be used to download the content of your Reddit saved posts. This has been created for and tested on Windows, it might not work on Linux based systems.

## Requirements

In order to get video files, merge the audio, and add metadata, [FFMPPEG](https://ffmpeg.org/) is required. You can find several tutorials on YouTube on how to install it (I personally use [this build](https://github.com/yt-dlp/FFmpeg-Builds/releases/tag/latest) from the yt-dlp project).

Of course, a recent version of [Python](https://www.python.org/) needs to be installed as well. If your version supports `f-strings`, then it should be fine, but you will need to install a newer version if it does not.

## Parameters:
    -h, --help                            show this help message and exit
    -u USERNAME, --username USERNAME      Reddit username.
    -p PASSWORD, --password PASSWORD      Reddit password.
    -f FROM_ID, --from_id FROM_ID         Reddit post id to start from (Optional).
    -t TO_ID, --to_id TO_ID               Reddit post id to end at (Optional).

## How to use

With Python and FFMPEG installed, open a terminal/CMD/PowerShell window and navigate to the directory containing the `RedditSPD.py` file, with the following command for example: `cd "path/"`

Make sure you install all the dependancies of the project with the command:

        pip install -r requirements.txt

In order to start the process you need to provide your Reddit `username` and `password` to the application. You can do this from the command line, by typing in the following command and replacing your credentials:

        python RedditSPD.py -u "username" -p "password"

Shortly afterwards, the file structure that will contain the downloaded posts will be created, you will be logged in, and the download(s) will start.

If you want to skip downloading a few posts, you can specify the starting and /or finishing Reddit post ID (you can get it from the post ULR) by using the following optional parameters:

        python RedditSPD.py -u "username" -p "password" -f "starting post id" -t "final post id"

After the application has finished downlaoding your posts (you will get a final message confirming it), check inside the `Archive` directory to find a folder with your Reddit username containing all the downloaded data. The data is separated to `Images`, `Videos` and `Self` posts in diferent folders. You can also find 2 files, `comments.txt` and `links.txt` containing all the saved comments and links.

Please note that if an Image or Video originated outside of Reddit's own hosting services, like `Imgur` for example, you will get the link to that content in the `links.txt` file instead of the content itself.

## Image and Video Metadata

Metadata for images and videos include the Reddit post `title`, `url`, `author username` and `post id`, provided as `title` and `comment` metadata in the files. The comment metadata in particular is provided in a `json` format, so it can be easily extracted and used by another application if needed.

When it comes to images, if the image is in a `gif` format, unfortunately the metadata tags are not supported, so no metadata is preserved (looking for a solution on this, one option is converting them to `mp4` and add metadata with FFMPEG). Other image types are saved in the `jpeg` format, which supports the metadata tags.

For videos, metadata is added with `FFMPEG`.

## Videos and FFMPEG

Other than addding metadata, there is another reason that FFMPEG is a requirement for downloading Reddit Videos.

Video and audio is provided seperately by Reddit. In order to combine the two in a single video file we need another dependancy. FFMPEG is the most efficient in doing this. It is also one of the most useful and widespread tools used for video editing, so it seems like the best choice. In case you want to use a different tool or application to combine the files, if FFMPEG is not instaled in your system, both seperate audio and video files will be preserved, so you can combine them as you wish.

## Errors

If the application encounters any errors, an `error.log` file will be created. You can submit an issue and attach the log, so I can try and fix the issue, or you can fix it yourself and submit a pull request with the fix. Feel free to choose either approach!

## Future ideas
- Add ability to download media from popular hosting services (for example `Imgur`).
- Improve the structure of the `comments.txt` and `links.txt` files, as the content can be annoying to use with another application to extract data.
- Currently no metadata is being added to `.gif` images, as the format does not support it. Find some solution.
- ~~Improve documentation with further info on metadata for images and videos.~~
- Refactoring/ bug fixes.

## Thank you and enjoy!