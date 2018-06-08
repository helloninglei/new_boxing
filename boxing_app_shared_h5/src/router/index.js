import Trends from 'page/trends';
import Download from 'page/download';
import InfoDetail from 'page/infoDetail';
import HotVideo from 'page/hotVideo';

export default [
    {
        path: '/messages/:id',
        component: Trends,
        meta: {
            title: '动态详情'
        }
    },
    {
        path: '/download',
        component: Download,
    },
    {
        path: '/game_news/:id',
        component: InfoDetail,
        meta: {
            title: '资讯详情'
        }
    },
    {
        path: '/hot_videos/:userId/:id',
        component: HotVideo,
        meta: {
            title: '热门视频',
            desc: '1111'
        }
    },
]
