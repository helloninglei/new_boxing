const config = {
    // 'baseUrl': location.host.indexOf('api') == 0 ? 'https://api.bituquanguan.com' : 'http://qa.bituquanguan.com',
    'baseUrl': location.pathname == '/share/' ? location.protocol+'//'+location.host :'http://qa.bituquanguan.com',
};

export default config;
