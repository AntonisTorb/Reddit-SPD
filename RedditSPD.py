import argparse
from datetime import datetime
from io import BytesIO
import os
from pathlib import Path
import random
import subprocess
import time

from PIL import Image
import requests


class RedditSPD:


    def __init__(self) -> None:

        self.username = ""
        self.path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        self.image_path = ""
        self.video_path = ""
        self.selfpost_path = ""
        self.session = requests.session()
        self.retries = 5
        self.headers = {
            "headers_img": {
                "Accept": "image/avif,image/webp,*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "i.redd.it",
                "Referer": "https://www.reddit.com/",
                "Sec-Fetch-Dest": "image",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
            "headers_video": {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, identity",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "v.redd.it",
                "Origin": "https://old.reddit.com",
                "Range": "",
                "Referer": "https://old.reddit.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
            "headers_info": {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, identity",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "v.redd.it",
                "Range": "bytes=0-",
                "Referer": "https://old.reddit.com/",
                "Sec-Fetch-Dest": "video",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
            "headers_audio": {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, identity",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "v.redd.it",
                "Origin": "https://old.reddit.com",
                "Range": "bytes=0-899",
                "Referer": "https://old.reddit.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "TE": "trailers",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
            "headers_login": {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Length": "",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "DNT": "1",
                "Host": "old.reddit.com",
                "Origin": "https://old.reddit.com",
                "Referer": "https://old.reddit.com/r/gaming/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "TE": "trailers",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
            "headers_saved": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "old.reddit.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "TE": "trailers",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            }
        }


    def _get_request_with_retries(self, url: str, headers: dict[str,str], acceptable_codes: list) -> requests.Response | None:
        '''Perform request with retries if the request status code is not in the provided list and return the response.'''

        retries = self.retries
        r = self.session.get(url, headers=headers, stream=True)
        while retries and r.status_code not in acceptable_codes:
            retries -= 1
            time.sleep(2 - random.random())
            r = self.session.get(url, headers=headers, stream=True)
        if r.status_code not in acceptable_codes:
            raise ConnectionError("Response status code not in list.")
        return r
    

    def _get_image(self, img_url: str, id: str, title: str, author, url: str) -> None:
        '''Gets and saves the Image files. Files other than .gif are saved as .jpg in order to add metadata.'''

        img_data = self._get_request_with_retries(img_url, self.headers["headers_img"], [200])
        
        # Gif exception, can't save as .jpg and does not support metadata.
        img_extension = img_url.split(".")[-1]
        if img_extension.lower() == "gif":
            filepath  = self.image_path / f'{id}.gif'
            
        else:
            filepath  = self.image_path / f'{id}.jpg'

        i = 1
        while True:
            if not Path(filepath).exists():
                break
            if img_extension.lower() == "gif":
                filepath = self.image_path / f'{id}({i}).gif'
            else:
                filepath = self.image_path / f'{id}({i}).jpg'
            i += 1

        if img_extension.lower() == "gif":
            with open(filepath, "wb") as file:
                file.write(img_data.content)
            return

        im = Image.open(BytesIO(img_data.content)).convert("RGB")
        exif = im.getexif()
        comment = '{{"title": "{title}", "url": "{url}", "author": "{author}", "id": "{id}"}}'.format(title=title, url=url, author=author, id=id)
        exif[270] = title
        exif[40092] = comment.encode("utf-16")
        im.save(filepath, exif=exif)


    def _get_video(self, video_url, audio_url, id, title, author, url) -> None:
        '''Gets and saves the video and audio files, combines them, removes temporary files and adds metadata.'''

        # Resetting headers.
        self.headers["headers_video"]["Range"] = ""
        self.headers["headers_audio"]["Range"] = "bytes=0-899"
        
        # Just in case.
        if Path(self.video_path / f"_vid-{id}.mp4").exists():
            os.remove(self.video_path / f"_vid-{id}.mp4")
        if Path(self.video_path / f"_audio-{id}.mp4").exists():
            os.remove(self.video_path / f"_audio-{id}.mp4")
        
        # Get info on video content length.
        r_vid_info = self._get_request_with_retries(video_url, self.headers["headers_info"], [206])

        max_vid = int(r_vid_info.headers["Content-Length"])

        # Get video file in chunks or all at once depending on size.
        if max_vid > 2097152:
            parts = max_vid // 1048576 + 1
            for part in range(0, parts):
                start = part * 1048576 + 1 if part > 0 else 0
                end = (part+1) * 1048576 if (part+1) * 1048576 < max_vid else max_vid
                self.headers["headers_video"]["Range"] = f"bytes={start}-{end}"

                # Get video file.
                r_video = self._get_request_with_retries(video_url, self.headers["headers_video"], [206])

                with open(self.video_path / f"_video-{id}.mp4", "ab") as file:
                    file.write(r_video.content)
        else:
            self.headers["headers_video"]["Range"] = f"bytes=0-{max_vid}"

            # Get video file.
            r_video = self._get_request_with_retries(video_url, self.headers["headers_video"], [206])

            with open(self.video_path / f"_video-{id}.mp4", "wb") as file:
                file.write(r_video.content)

        # No Audio.
        if not audio_url:
            try:
                os.rename(self.video_path / f"_video-{id}.mp4", self.video_path / f"_{id}.mp4")
            except FileExistsError:
                replace = input(f"File '{id}.mp4' already exists. Overwrite? [y/N] ")
                if replace.lower() == "y":
                    os.remove(self.video_path / f"_{id}.mp4")
                    os.rename(self.video_path / f"_video-{id}.mp4", self.video_path / f"_{id}.mp4")
                else:
                    os.remove(self.video_path / f"_video-{id}.mp4")
            return

        # Get info on audio content length.
        r_aud_info = self._get_request_with_retries(audio_url, self.headers["headers_audio"], [206, 403])
        if r_aud_info.status_code == 403:
            audio_url = audio_url.replace("AUDIO_128", "audio")  # Older format.
            time.sleep(2)
            r_aud_info = self._get_request_with_retries(audio_url, self.headers["headers_audio"], [206])
        
        max_aud = int(r_aud_info.headers["Content-Range"].split("/")[1])

        # Get audio file in chunks or all at once depending on size.
        if max_aud > 2097152:
            parts = max_aud // 1048576 + 1
            for part in range(0, parts):
                start = part * 1048576 + 1 if part > 0 else 0
                end = (part+1) * 1048576 if (part+1) * 1048576 < max_aud else max_aud
                self.headers["headers_audio"]["Range"] = f"bytes={start}-{end}"

                # Get video file.
                r_audio = self._get_request_with_retries(audio_url, self.headers["headers_audio"], [206])

                with open(self.video_path / f"_audio-{id}.mp4", "ab") as file:
                    file.write(r_audio.content)
        else:
            self.headers["headers_audio"]["Range"] = f"bytes=0-{max_aud}"

            # Get audio file.
            r_audio = self._get_request_with_retries(audio_url, self.headers["headers_audio"], [206])

            with open(self.video_path / f"_audio-{id}.mp4", "wb") as file:
                file.write(r_audio.content)

        try:
            # Combine video and audio files.
            subprocess.run(
                f'ffmpeg -hide_banner -loglevel error -i "{self.video_path}\_video-{id}.mp4" -i "{self.video_path}\_audio-{id}.mp4" -map "0:0" -map "1:0" -c copy "{self.video_path}\_{id}.mp4"'
            )

            # Remove temporary files. 
            os.remove(self.video_path / f"_video-{id}.mp4")
            os.remove(self.video_path / f"_audio-{id}.mp4")
        except:
            raise Exception("FFMPEG error, leaving separate video and audio files.")
        
        try:
            # Add metadata to video file.
            comment = "{{'title': '{title}', 'url': '{url}', 'author': '{author}', 'id': '{id}'}}".format(title=title, url=url, author=author, id=id)
            subprocess.run(
                f'ffmpeg -hide_banner -loglevel error -i "{self.video_path}\_{id}.mp4" -c copy -metadata title="{title}" -metadata comment="{comment}" "{self.video_path}\{id}.mp4"'
            )
            os.remove(self.video_path / f"_{id}.mp4")
        except:
            os.rename(self.video_path / f"_{id}.mp4", self.video_path / f"{id}.mp4")
            raise Exception("FFMPEG error, can't add metadata.")


    def _determine_post_type(self, post: dict) -> str:
        '''Determines the type of the saved post and returns a representative string.'''

        # Gallery:
        try: 
            is_gallery = post["data"]["is_gallery"]
            if is_gallery:
                return "gallery"
        except KeyError:
            pass
        
        # Image:
        try:
            is_image = post["data"]["domain"] == "i.redd.it"
            if is_image:
                return "image"
        except KeyError:
            pass

        # Self:
        try:
            is_self = post["data"]["is_self"]
            if is_self:
                return "self"
        except KeyError:
            pass

        # Video:
        try:
            is_video = post["data"]["is_video"]
            if is_video:
                return "video"
        except KeyError:
            pass

        # Crosspost:
        if "crosspost_parent" in post["data"].keys():
            try:
                post = {"data": post["data"]["crosspost_parent_list"][0]}
                return self._determine_post_type(post)
            except IndexError:  # Sometimes link posts are marked as crossposts when they aren't...
                return "link"
        
        # Comment:
        try:
            if post["kind"] == "t1":
                return "comment"
        except KeyError:
            pass

        # Link:
        return "link"


    def _get_content(self, post: dict) -> None:
        '''Gets the content from the post and saves it according to it's type.'''

        post_type = self._determine_post_type(post)
        
        if post_type == "gallery":
            img_list = post["data"]["media_metadata"].keys()
            for img_id in img_list:
                img_extension = post["data"]["media_metadata"][img_id]["m"].split("/")[1]
                img_url= f'https://i.redd.it/{img_id}.{img_extension}'
                id = post["data"]["id"]
                title = post["data"]["title"]
                author = post["data"]["author"]
                url = f'https://reddit.com{post["data"]["permalink"]}'
                self._get_image(img_url, id, title, author, url)
        
        if post_type == "image":
            img_url= post["data"]["url"]
            id = post["data"]["id"]
            title = post["data"]["title"]
            author = post["data"]["author"]
            url = f'https://reddit.com{post["data"]["permalink"]}'
            self._get_image(img_url, id, title, author, url)

        if post_type == "self":
            id = post["data"]["id"]
            title = post["data"]["title"]
            author = post["data"]["author"]
            url = post["data"]["url"]
            content = post["data"]["selftext"]
            with open(self.selfpost_path / f'{id}.txt', "w") as file:
                content = f'{title = }\n{author = }\n{url = }\n\n{content}'
                file.write(content)

        if post_type == "video":
            id = post["data"]["id"]
            title = post["data"]["title"]
            author = post["data"]["author"]
            url = f'https://reddit.com{post["data"]["permalink"]}'
            video_url = post["data"]["secure_media"]["reddit_video"]["fallback_url"][:-16]
            has_audio = post["data"]["secure_media"]["reddit_video"]["has_audio"]
            if has_audio:
                audio_url = f"https://v.redd.it/{video_url.split('/')[3]}/DASH_AUDIO_128.mp4"
            else:
                audio_url = None
            self._get_video(video_url, audio_url, id, title, author, url)

        if post_type == "comment":
            title = post["data"]["link_title"]
            author = post["data"]["author"]
            body = post["data"]["body"]
            url = post["data"]["link_permalink"]

            content = f'{title = }\n{author = }\n{url = }\n\n{body}\n\n{"-"*50}\n\n'

            with open(self.path / "comments.txt", "a", encoding="utf-8") as file:
                file.write(content)

        if post_type == "link":
            id = post["data"]["id"]
            title = post["data"]["title"]
            author = post["data"]["author"]
            url = post["data"]["url"]
            
            content = f'{title = }\n{author = }\n{url = }\n\n{"-"*50}\n\n'
            
            with open(self.path / "link posts.txt", "a", encoding="utf-8") as file:
                file.write(content)
    

    def _create_directory_struct(self) -> None:
        '''Creates the directory structured required to save all post types.'''

        self.path = self.path / "Archive" /  self.username
        self.path.mkdir(parents=True, exist_ok=True)
        self.image_path = self.path / "Images"
        self.image_path.mkdir(exist_ok=True)
        self.video_path = self.path / "Videos"
        self.video_path.mkdir(exist_ok=True)
        self.selfpost_path = self.path / "Self Posts"
        self.selfpost_path.mkdir(exist_ok=True)


    def _login(self, username: str, password: str) -> requests.Response:
        '''Logs in on Reddit for the current session with the provided credentials.'''

        self.headers["headers_login"]["Content-Length"] = str(41 + len(username) + len(password))
        payload = {
            "op" : "login-main",
            "user" : f'{username}',
            "passwd" : f'{password}',
            "api_type" : "json"
        }
        login_url = f'https://old.reddit.com/api/login/{username}'

        return self.session.post(login_url, data=payload, headers=self.headers["headers_login"])


    def _get_saved_list(self) -> tuple[int, list[dict]]:
        '''Returns the amount of saved posts and a list of the saved posts for the user.'''

        total_saved = 0
        saved_list = []
        finished = False
        after = ""
        while not finished:
            if total_saved == 0:
                saved_url = f'https://old.reddit.com/user/{self.username}/saved.json'
            else:
                saved_url = f'https://old.reddit.com/user/{self.username}/saved.json?count={total_saved}&after={after}'
            saved_res = self._get_request_with_retries(saved_url, self.headers["headers_saved"], [200]).json()
            
            saved_list += saved_res["data"]["children"]
            total_saved += int(saved_res["data"]["dist"])
            after = saved_res["data"]["after"]
            
            if after is None:
                finished = True

        return total_saved, saved_list


    def start_dl(self, username: str, password: str, from_id: str | None = None, to_id: str | None = None) -> None:
        '''Starts the process of logging in, gathering the saved post pages and downloading 
        the content of each saved post from newest to oldest saved.
        '''
        
        self.username = username
        self._create_directory_struct()

        login_response = self._login(username, password)
        
        if login_response.status_code != 200:
            print("Error, cannot login! Please check provided credentials.")
            return

        total_saved, saved_list = self._get_saved_list()
        
        print(f'{total_saved} saved posts located.')
        
        archive_counter = 0
        pass_it = True if from_id is not None else False
        
        for index, post in enumerate(saved_list):
            if "id" in post["data"].keys():
                if post["data"]["id"] == from_id:
                    pass_it = False

            if not pass_it:
                try:
                    print(f'Getting data from [{index + 1}/{total_saved}]" {post["data"]["title"]}"...')
                except KeyError:  # Comment.
                    print(f'Getting data from [{index + 1}/{total_saved}]" {post["data"]["link_title"]}"...')
                try:
                    self._get_content(post)
                    archive_counter += 1
                except Exception as e:
                    print("Error getting above post. Please check 'error.log' for details.")
                    
                    timestamp = datetime.now()
                    if "permalink" in post["data"].keys():
                        link = post["data"]["permalink"]
                    else:
                        link = "N/A"
                    exception_name = type(e).__name__
                    exception_text = str(e)
                    
                    with open("error.log", "a") as file:
                        file.write(f'[{timestamp}]: {link} - {exception_name}: {exception_text}\n')
                    
            try:
                if post["data"]["id"] == to_id:
                    break
            except KeyError:
                pass
        
        print(f'Finished getting {archive_counter} saved posts for user "{self.username}".')
        self.username = ""
        self.session.close()
        self.session = requests.session()

        
if __name__ == "__main__":

    downloader = RedditSPD()

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, help="Reddit username.", required=True)
    parser.add_argument("-p", "--password", type=str, help="Reddit password.", required=True)
    parser.add_argument("-f", "--from_id", type=str, help="Reddit post id to start from (Optional).", required=False)
    parser.add_argument("-t", "--to_id", type=str, help="Reddit post id to end at. (Optional)", required=False)
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    from_id = args.from_id
    to_id = args.to_id

    downloader.start_dl(username, password, from_id, to_id)