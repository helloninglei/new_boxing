import Trends from 'page/trends';
import Download from 'page/download';
import InfoDetail from 'page/infoDetail';
import HotVideo from 'page/hotVideo';
import CourseDetail from 'page/courseDetail';

export default [
    {
        path: '/trends/:id',
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
        path: '/infoDetail/:id',
        component: InfoDetail,
        meta: {
            title: '资讯详情'
        }
    },
    {
        path: '/hotVideo/:userId/:id',
        component: HotVideo,
        meta: {
            title: '热门视频',
            desc: '1111'
        }
    },
    {
        path: '/courseDetail/:id',
        component: CourseDetail,
        meta: {
            title: '课程详情'
        }
    },
]
