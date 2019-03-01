# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import determine_ext


# Sample URL: https://vev.io/76369znzyk3d
class VevioIE(InfoExtractor):
    IE_NAME = 'vevio'
    IE_DESC = 'Previously known as theVideo'
    # _VALID_URL = r'(?:https?:\/\/)?(?:www\.)?vev\.io\/(?P<id>[a-zA-Z0-9-_]+)'

    # _VALID_URL = r'''https?://(?:www\.)?
    #     (?:
    #         vev\.io|
    #         thevideo\.me
    #     )
    #     /(?P<id>[a-zA-Z0-9-_]+)'''

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

        self.report_extraction(video_id)
        # TODO more code goes here, for example ...
        title = self._html_search_regex(r'<title>(.+?)</title>', webpage, 'title')
        print(title)

        video_url = self._html_search_regex(r'<video.+src="(.+)"><\/video>', webpage, 'video_url')
        print(video_url)

        return {
            'id': video_id,
            'title': title,
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
            'description': self._og_search_description(webpage),
            'uploader': self._search_regex(r'<div[^>]+id="uploader"[^>]*>([^<]+)<', webpage, 'uploader', fatal=False),
            'url': video_url,
            'ext': determine_ext(title, None) or determine_ext(url, 'mp4'),
            # TODO more properties (see youtube_dl/extractor/common.py)
        }