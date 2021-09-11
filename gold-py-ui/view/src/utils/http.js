import axios from 'axios'

// 创建 axios 实例
const service = axios.create({
    baseURL: '/', // api base_url
    timeout: 2500 // 请求超时时间
})

// 添加请求拦截器
service.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    return config;
}, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    if (response.status === 200) {
        return response.data;
    } else {
        this.$message.warn('服务内部错误');
        return
    }
}, function (error) {
    // 对响应错误做点什么
    return Promise.reject(error);
});

export {
    service as axios
}