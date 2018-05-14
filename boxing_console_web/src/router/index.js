import Index        from 'components/index';
import Login        from 'components/login';
import Viewer       from 'components/viewer';
import UserManage   from 'pages/usermanage';
import BoxingManage from 'pages/boxingmanage';
import BoxingList   from 'pages/boxinglist';
import AddBoxing    from 'pages/addboxing';


export default [
    {
        path: '',
        component: Login,
    },
    {
        path: '/login',
        component: Login,
    },
    {
        path: '/index',
        component: Index,
        children: [
            {
                path: '',
                component: UserManage,
            },
            {
                path: '/usermanage',
                component: UserManage,
            },
            {
                path: '/boxingmanage',
                component: BoxingManage,
            },
            {
                path: '/boxinglist',
                component: BoxingList,
            },
            {
                path: '/addboxing',
                component: AddBoxing,
            },
        ]
    },
    
  
]
