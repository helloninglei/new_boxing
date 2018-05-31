import Trends from 'page/trends';
import Download from 'page/download';


export default [
    {
        path: '/trends/:id',
        component: Trends,
        meta: {
            title: '首页入口'
        }
    },
    {
        path: '/download',
        component: Download,
    },
]
