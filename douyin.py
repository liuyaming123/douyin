import requests
import os
import time
import re
import random
from fake_useragent import UserAgent
from log import logger


class DouYin:
    """
    抓取抖音分享链接里的用户信息和视频信息
    """
    user_info_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?'  # 用户信息
    video_list_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'  # 用户视频列表
    video_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?'  # 单个视频信息

    def __init__(self, user_share_link):
        self.user_share_link = user_share_link
        self.sec_uid = self.get_sec_uid()
        self.user_info = self.get_user_info()
        self.download_dir = ''

        '''设置下载目录'''
        self.nickname = self.user_info['nickname']
        self.unique_id = self.user_info['unique_id']
        logger.info(f'nickname: {self.nickname}, unique_id: {self.unique_id}')
        path = f"{self.nickname}_{self.unique_id}"
        self.set_download_dir(os.path.join(self.download_dir, path))

    @property
    def headers(self):
        return {"user-agent": UserAgent(verify_ssl=False).random}

    def set_download_dir(self, path):
        if not os.path.exists(path=path):
            os.mkdir(path=path)
        else:
            logger.info('directory exist')
        os.chdir(path=path)

    def get_sec_uid(self):
        short_url = re.findall('[a-z]+://[\S]+', self.user_share_link, re.I | re.M)[0]
        start_page = requests.get(url=short_url, headers=self.headers, allow_redirects=False)
        location = start_page.headers['location']
        self.sec_uid = re.findall('(?<=sec_uid=)[a-zA-Z0-9_-]+', location)[0]
        return self.sec_uid

    def get_user_info(self):
        params = {'sec_uid': self.sec_uid}
        data = requests.get(DouYin.user_info_url, params=params, headers=self.headers).json()
        return data['user_info']

    @staticmethod
    def get_cursor_list():
        start_date = '2017-01-01 00:00:01'  # 抓取开始时间
        day_gap = 15  # 间隔时间
        one_day = 86400  # 60 * 60 * 24
        start = int(time.mktime(time.strptime(start_date, "%Y-%m-%d %H:%M:%S")))
        ct = time.time()
        cl = []
        while start < ct:
            end = start + one_day * day_gap
            cl.append((start, end))
            start = end
        return cl

    def get_aweme_param_list(self):
        return [
            {
                'sec_uid': self.sec_uid,
                'count': 100,
                'min_cursor': t1 * 1000,
                'max_cursor': t2 * 1000,
                'aid': 1128,
                '_signature': 'PtCNCgAAXljWCq93QOKsFT7QjR'
            }
            for t1, t2 in self.get_cursor_list()
        ]

    @staticmethod
    def gtime(ts):
        ts = int(str(ts)[:-3])
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    def get_user_video_list(self):
        """获取用户视频列表"""
        v_sum = 0
        for p in self.get_aweme_param_list():
            data = requests.get(DouYin.video_list_url, params=p, headers=self.headers).json()
            aweme_num = len(data['aweme_list'])

            if aweme_num > 0:
                v_sum += aweme_num
                logger.info(f"video_num: {aweme_num}, "
                            f"min_cursor: {self.gtime(p.get('min_cursor'))}, "
                            f"max_cursor: {self.gtime(p.get('max_cursor'))}, param: {p}")

            time.sleep(random.random())
            for i in data['aweme_list']:
                aweme_id = i['aweme_id']
                video_url = i['video']['play_addr']['url_list'][0]
                uri = i['video']['play_addr']['uri']
                # logger.info(f'video_uri: {uri}')
                self.download_video(aweme_id, video_url)

        logger.info(f'aweme_count: {self.user_info["aweme_count"]}, download_count: {v_sum}, nickname: {self.nickname}')

    def get_one_video(self, aweme_id):
        pass

    def download_video(self, aweme_id, video_url):
        """视频下载"""
        start = time.time()
        logger.info('    {} ===>downloading'.format(aweme_id))
        with open(aweme_id + '.mp4', 'wb') as v:
            try:
                v.write(requests.get(url=video_url, headers=self.headers).content)
                end = time.time()
                cost = end - start
                logger.info(f'    {aweme_id} ===>downloaded ===>cost {round(cost, 3)}s')
            except Exception as e:
                logger.error(f'download error: {e}')

    def upload_video(self):
        """视频上传"""
        pass


if __name__ == '__main__':
    share_url_list = [
        'https://v.douyin.com/YhCx9Px/',  # 川味盐太婆
        'https://v.douyin.com/YhXxEn8/',  # 张卫平
        'https://v.douyin.com/Yhq95HC/',  # 篮球🏀先生
        'https://v.douyin.com/Y6XsxTE/',  # Ray-周锐
    ]

    for share_url in share_url_list:
        d = DouYin(share_url)
        d.get_user_video_list()
