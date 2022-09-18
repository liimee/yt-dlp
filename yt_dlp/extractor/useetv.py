from .common import InfoExtractor
import re


class UseeTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)useetv.com/(?P<type>vodpremium/play|tvod|livetv)/(?P<id>.+)'
    _TESTS = [{
        'url': 'https://www.useetv.com/vodpremium/play/8135',
        'info_dict': {
            'id': '8135',
            'ext': 'mp4',
            'title': 'HAPPY COZY EPS 91',
            'description': 'Program variety show yang mengungkap soal gaya hidup, musik, viral media sosial dari sudut pandang milenial dengan games-games seru yang di pandu Zeva Magnolya dan Melki Bajai. Keseruan kali ini bersama Arafah dan Hilda.'
        }
    }, {
        'url': 'https://www.useetv.com/tvod/seatoday/1663434000/1663435800/all-about-coffee',
        'info_dict': {
            'id': 'seatoday/1663434000/1663435800/all-about-coffee',
            'ext': 'mp4',
            'title': 'All About Coffee'
        }
    }]

    def _real_extract(self, url):
        video_id, video_type = self._match_valid_url(url).group('id', 'type')
        webpage = self._download_webpage(url, video_id)

        formats = []
        if video_type == 'vodpremium/play':
            jwplayer_data = self._find_jwplayer_data(webpage)
            formats.extend(self._extract_m3u8_formats(jwplayer_data['file'], video_id, 'mp4', 'm3u8_native'))

            title = self._html_search_regex(r'<h3>(.+?)</h3>', webpage, 'title')
        else:
            url_re = re.compile(r'<source src="(?P<id>.+)" type="application/x-mpegURL">')
            m3u8_url = re.search(url_re, webpage).group('id')
            formats.extend(self._extract_m3u8_formats(m3u8_url, video_id, 'mp4', 'm3u8_native'))

            title = self._html_search_regex(r'<a href=".+" class=".+ live">.+<b>(.+)</b>.+</a>', webpage, 'title')

        description = self._html_search_regex(r'<div class="row video-description">(.+?)</div>', webpage, 'description', default=None)

        return {
            'id': video_id,
            'formats': formats,
            'title': title,
            'description': description,
            'ext': 'm3u8'
        }
