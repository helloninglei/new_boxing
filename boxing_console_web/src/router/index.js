import Index            from 'components/index';
import Login            from 'components/login';
import UserManage       from 'pages/usermanage';
import BoxingManage     from 'pages/boxingmanage';
import BoxingList       from 'pages/boxinglist';
import AddBoxing        from 'pages/addboxing';
import Financemanage    from 'pages/financemanage';
import Paymentlist      from 'pages/paymentlist';
import Precentlist      from 'pages/precentlist';
import Boxerindentify   from 'pages/boxerindentify';


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
            {
                path: '/financemanage',
                component: Financemanage,
            },
            {
                path: '/paymentlist',
                component: Paymentlist,
            },
            {
                path: '/precentlist',
                component: Precentlist,
            },
            {
                path: '/boxerindentify',
                component: Boxerindentify,
            },
        ]
    },
    
  
]
