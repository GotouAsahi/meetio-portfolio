import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import App from './App.vue'
import router from './router'
import './index.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCookies from 'vue-cookies'
import mavonEditor from "mavon-editor";
import "mavon-editor/dist/css/index.css";
import SimpleTypeahead from "vue3-simple-typeahead";
import 'vue3-simple-typeahead/dist/vue3-simple-typeahead.css';
import store from './store'
import VueChartJs from 'vue-chartjs'
import vue3GoogleLogin from 'vue3-google-login'

library.add(fas, far, fab)

axios.defaults.baseURL = process.env.NODE_ENV === 'production'
  ? 'http://184.73.208.222'  // 本番環境のAPIのベースURL
  : 'http://localhost:8000';

createApp(App)
  .use(router)
  .use(VueAxios, axios)
  .use(VueCookies)
  .use(mavonEditor)
  .use(SimpleTypeahead)
  .use(store)
  .use(VueChartJs)
  .use(vue3GoogleLogin, {
    clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID
  })
  .component('font-awesome-icon', FontAwesomeIcon)
  .mount('#app')