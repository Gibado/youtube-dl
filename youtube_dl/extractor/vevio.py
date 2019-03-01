# coding: utf-8
from __future__ import unicode_literals

from youtube_dl.extractor.openload import PhantomJSwrapper
from .common import InfoExtractor
from ..utils import determine_ext, get_element_by_id


# Sample URL: https://vev.io/76369znzyk3d
class VevioIE(InfoExtractor):
    IE_NAME = 'vevio'
    IE_DESC = 'Previously known as theVideo'
    _USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    _VALID_URL = r'''(?x)
                    https?://
                        (?P<host>
                            (?:www\.)?
                            (?:
                                vev\.(?:io)|
                                thevideo\.(?:me)
                            )
                        )/
                        (?P<id>[a-zA-Z0-9-_]+)
                    '''


    _TEST = {
        'url': 'https://vev.io/76369znzyk3d',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '76369znzyk3d',
            'ext': 'mp4',
            'title': 'Adventure Time S09E08 The First Investigation 720p',
            'thumbnail': r're:^https?://.*\.png$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }

    def _real_extract(self, url):
        # mobj = re.match(self._VALID_URL, url)
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        formatted = webpage.encode(encoding='UTF-8', errors='replace')
        fileName = "C:/tmp/" + video_id + ".html"
        f = open(fileName, "w+")
        f.write(formatted)
        f.close()


        headers = {
            'User-Agent': self._USER_AGENT,
        }

        phantom = PhantomJSwrapper(self, required_version='2.0')
        webpage, _ = phantom.get(url, html=webpage, video_id=video_id, headers=headers)

        formatted = webpage.encode(encoding='UTF-8', errors='replace')
        fileName = fileName + "-phantom.html"
        f = open(fileName, "w+")
        f.write(formatted)
        f.close()

        print("phantom processed")

        # print(webpage)

        self.report_extraction(video_id)
        # TODO more code goes here, for example ...
        title = self._html_search_regex(r'<title>(.+?)</title>', webpage, 'title')
        print(title)

        # video_url = self._html_search_regex(r'src="(.+)"><\/video>', webpage, 'video_url')
        # print(video_url)
        video_url = get_element_by_id('vjs_video_3_html5_api', webpage)
        print(video_url)

        return {
            'id': video_id,
            'title': title,
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
            # 'description': self._og_search_description(webpage),
            # 'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            'url': video_url,
            'ext': determine_ext(title, None) or determine_ext(url, 'mp4'),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }