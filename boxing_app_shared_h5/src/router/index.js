import Trends from 'page/trends';
import Download from 'page/download';
import InfoDetail from 'page/infoDetail';
import HotVideo from 'page/hotVideo';
import CourseDetail from 'page/courseDetail';

export default [
    {
        path: '/messages/:id',
        component: Trends,
        meta: {
            title: '拳城出击'
        }
    },
    {
        path: '/download',
        component: Download,
    },
    {
        path: '/game_news/:id/:inApp',
        component: InfoDetail,
        meta: {
            title: '拳城出击'
        }
    },
    {
        path: '/hot_videos/:userId/:id',
        component: HotVideo,
        meta: {
            title: '拳城出击',
            desc: '1111'
        }
    },
    {
        path: '/boxers/:id',
        component: CourseDetail,
        meta: {
            title: '拳城出击'
        }
    },
]
