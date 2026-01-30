import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import VueLazyLoad from 'vue3-lazyload'
import loadingImage from './assets/img/loading.svg'

const app = createApp(App)

app.use(router)
app.use(i18n)
app.use(VueLazyLoad, {
  loading: loadingImage,
})
app.mount('#app')
