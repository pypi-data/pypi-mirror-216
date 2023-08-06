'''Download Webtoons from Naver Post.
'''
import re
from pathlib import Path
import time
from itertools import count
import asyncio
import json
from async_lru import alru_cache
import demjson3
from bs4 import BeautifulSoup
# from WebtoonScraper.Scraper import Scraper
from WebtoonScraper.Scraper import Scraper

class NaverGameScraper(Scraper):
    '''Scrape webtoons from Naver Post.'''
    def __init__(self, pbar_independent=False, short_connection=False):
        super().__init__(pbar_independent, short_connection)
        self.BASE_URL = 'https://game.naver.com/original_series'
        if not short_connection:
            self.IS_STABLE_CONNECTION = True

    @alru_cache(maxsize=4)
    async def get_webtoon_data(self, titleid):
        url = f'https://apis.naver.com/nng_main/nng_main/original/series/{titleid}'
        webtoon_raw_data = await self.get_internet(get_type='requests', url=url)
        webtoon_raw_data = webtoon_raw_data.json()
        title = webtoon_raw_data['content']['seriesName']
        thumbnail = webtoon_raw_data['content']['seriesImage']['verticalLogoImageUrl']
        return title, thumbnail

    @alru_cache(maxsize=4)
    async def get_episode_data(self, titleid, episode_max_limit=500):
        
        # 여러 시즌을 하나로 통합
        content_raw_data = []
        for season in count(1):
            url = f'https://apis.naver.com/nng_main/nng_main/original/series/{titleid}/seasons/{season}/contents?direction=NEXT&pagingType=CURSOR&sort=FIRST&limit={episode_max_limit}'
            res = await self.get_internet(get_type='requests', url=url)
            res = res.json()
            if not res['content']:
                break
            content_raw_data += res['content']['data']
        
        # 부제목, 이미지 데이터 불러옴
        episodes_data = {}
        for i, episode in enumerate(content_raw_data, 1):
            # print(episode['feedId'])
            subtitle = episode['feed']['title']
            # print(json.loads(episode['feed']['contents']))
            content_json_data = json.loads(episode['feed']['contents'])
            image_urls = []
            for image_url in content_json_data['document']['components']:
                try:
                    image_urls.append(image_url['src'])
                except KeyError:
                    pass
            episodes_data[i] = {'subtitle': subtitle, 'image_urls': image_urls}
        
        return episodes_data

    async def get_title(self, titleid, file_acceptable=True):
        title, _ = await self.get_webtoon_data(titleid)
        if file_acceptable:
            title = self.get_acceptable_file_name(title)
        return title

    async def save_webtoon_thumbnail(self, titleid, title, thumbnail_dir):
        _, image_url = await self.get_webtoon_data(titleid)
        image_extension = self.get_file_extension(image_url)
        image_raw = await self.get_internet(get_type='requests', url=image_url)
        image_raw = image_raw.content
        Path(f'{thumbnail_dir}/{title}.{image_extension}').write_bytes(image_raw)

    async def get_all_episode_no(self, titleid, attempt):
        episodes_data = await self.get_episode_data(titleid)
        return list(episodes_data)

    async def get_subtitle(self, titleid, episode_no, file_acceptable):
        episodes_data = await self.get_episode_data(titleid)
        subtitle = episodes_data[episode_no]['subtitle']
        if file_acceptable:
            subtitle = self.get_acceptable_file_name(subtitle)
        return subtitle

    async def get_episode_images_url(self, titleid, episode_no, attempt=3):
        episodes_data = await self.get_episode_data(titleid)
        return episodes_data[episode_no]['image_urls']
    
if __name__ == '__main__':
    # np = NaverPost()
    # np.download_one_webtoon(625402, 19803452)

    # wt = NaverPost()
    # asyncio.run(wt.get_data(625402, 19803452))

    # wt = NaverPost()
    # wt.member_no = 19803452
    # print(asyncio.run(wt.get_episode_images_url(577056, 2)))

    # from NaverPost import NaverPostScraper
    wt = NaverGameScraper()
    # wt.download_one_webtoon(614921, 19803452)
    # wt.download_one_webtoon(577056, 19803452)
    # wt.download_one_webtoon(625402, 19803452)
    # wt.set_folders('webtoon')
    # wt.download_one_webtoon(31)
    wt.download_one_webtoon(5)