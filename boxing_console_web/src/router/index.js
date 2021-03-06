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
import Album            from 'page/album';
import Report           from 'page/report';
import Hotvideo         from 'page/hot_videos';
import Hotvideodetail   from 'page/hot_video_detail';
import AccoundRecord    from 'page/accound_record';
import InfoList         from 'page/infolist';
import Metchlist        from 'page/metchlist';
import Battlelist        from 'page/battlelist';
import Boxerlist         from 'page/boxerlist';
import InfoDetail       from 'page/info_detail';
import BoxBean          from 'page/boxBean';
import Dynamic          from 'page/dynamic';
import SensitiveWord    from 'page/sensitive_words';
import AlbumDetail      from 'page/album_detail';
import BoxerDetail      from 'page/boxer_detail';
import Feedback         from 'page/feedback';
import Versionlist         from 'page/versionlist';
import VersionDetail         from 'page/version_detail';


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
                path: '/album',
                component: Album,
            },
            {
                path: '/albumdetail',
                component: AlbumDetail,
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
                path: '/metchlist',
                component: Metchlist,
            },
            {
                path: '/battlelist',
                component: Battlelist,
            },
            {
                path: '/boxerlist',
                component: Boxerlist,
            },
            {
                path: '/boxerdetail',
                component: BoxerDetail,
            },
            {
                path: '/versionlist',
                component: Versionlist,
            },
            {
                path: '/versiondetail',
                component: VersionDetail,
            },
            {
                path: '/boxBean',
                component: BoxBean,
            },
            {
                path: '/dynamic',
                component: Dynamic,
            },
            {
                path: '/sensitiveword',
                component: SensitiveWord,
            },
            {
                path: '/feedback',
                component: Feedback,
            },
        ]
    },
    
  
]
