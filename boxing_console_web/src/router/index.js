import Index            from 'components/index';
import Login            from 'components/login';
import UserManage       from 'page/usermanage';
import BoxingManage     from 'page/boxingmanage';
import BoxingList       from 'page/boxinglist';
import AddBoxing        from 'page/addboxing';
import Financemanage    from 'page/financemanage';
import Paymentlist      from 'page/paymentlist';
import Precentlist      from 'page/precentlist';
import Boxerindentify   from 'page/boxerindentify';
import Classmanage      from 'page/classmanage';
import Classdetail      from 'page/classdetail1';
import Userdetail       from 'page/userdetail';
import Walletlist       from 'page/walletlist';


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
                path: '/index',
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
            {
                path: '/classmanage',
                component: Classmanage,
            },
            {
                path: '/classdetail',
                component: Classdetail,
            },
            {
                path: '/userdetail',
                component: Userdetail,
            },
            {
                path: '/walletlist',
                component: Walletlist,
            },
        ]
    },
    
  
]
