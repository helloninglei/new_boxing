import Index            from 'components/index';
import Login            from 'components/login';
import UserManage       from 'page/usermanage';
import BoxingList       from 'page/boxinglist';
import AddBoxing        from 'page/addboxing';
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
import Boxbeanlist      from 'page/boxbeanlist';
import UseDialog        from 'components/useDialog';
import BannerManage     from 'page/bannermanage';
import BannerContent    from 'page/bannercontent';
import Cropper          from 'components/cropper';
import Map1             from 'components/map';
import Admin            from 'page/admin';
import Report           from 'page/report';
import Hotvideo         from 'page/hot_videos';
import Hotvideodetail   from 'page/hot_video_detail';
import AccoundRecord    from 'page/accound_record';
import InfoList         from 'page/infolist';
import InfoDetail       from 'page/info_detail';
import BoxBean          from 'page/boxBean';

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
                path: '/boxinglist',
                component: BoxingList,
            },
            {
                path: '/addboxing',
                component: AddBoxing,
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
                path: '/boxbeanlist',
                component: Boxbeanlist,
            },
            {
                path: '/useDialog',
                component: UseDialog,
            },
            {
                path: '/bannermanage',
                component: BannerManage,
            },
            {
                path: '/bannercontent',
                component: BannerContent,
            },
            {
                path: '/cropper',
                component: Cropper,
            },
            {
                path: '/map',
                component: Map1,
            },
            {
                path: '/admin',
                component: Admin,
            },
            {
                path: '/report',
                component: Report,
            },
            {
                path: '/hotvideo',
                component: Hotvideo,
            },
            {
                path: '/hotvideodetail',
                component: Hotvideodetail,
            },
            {
                path: '/accound_record',
                component: AccoundRecord,
            },
            {
                path: '/infoList',
                component: InfoList,
            },
            {
                path: '/infodetail',
                component: InfoDetail,
            },
            {
                path: '/boxBean',
                component: BoxBean,
            },
        ]
    },
    
  
]
