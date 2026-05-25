import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000
})

request.interceptors.response.use(
  (resp) => resp.data,
  (err) => {
    console.error('[RCS-Demo API ERROR]', err)
    return Promise.reject(err)
  }
)

export default request
