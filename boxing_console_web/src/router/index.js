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
import Settlemanage     from 'page/settlemanage';
import Ordermanage      from 'page/ordermanage';
import Classdetail      from 'page/class_detail';
import Userdetail       from 'page/user_detail';
import Orderdetail      from 'page/order_detail';
import Boxerindentdetail from 'page/boxer_indent_detail';
import Walletlist       from 'page/walletlist';
import UseDialog        from 'components/useDialog';


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
                path: '/classall',
                component: Classmanage,
            },
            {
                path: '/ordermanage',
                component: Ordermanage,
            },
            {
                path: '/settlemanage',
                component: Settlemanage,
            },
            {
                path: '/classdetail',
                component: Classdetail,
            },
            {
                path: '/orderdetail',
                component: Orderdetail,
            },
            {
                path: '/userdetail',
                component: Userdetail,
            },
            {
                path: '/boxerindentdetail',
                component: Boxerindentdetail,
            },
            {
                path: '/walletlist',
                component: Walletlist,
            },
            {
                path: '/useDialog',
                component: UseDialog,
            },
        ]
    },
    
  
]
