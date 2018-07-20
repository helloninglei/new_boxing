function getApi() {
    if (location.pathname === '/share/') {
        return location.protocol + '//' + location.host;
    } else {
        return 'http://qa.bituquanguan.com';
    }
}

const config = {
    'baseUrl': location.host.indexOf('api') === 0 ? 'https://api.bituquanguan.com' : getApi(),
};

export default config;
