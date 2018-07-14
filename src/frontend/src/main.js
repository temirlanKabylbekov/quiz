// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuex from 'vuex';
import { sync } from 'vuex-router-sync';
import * as Cookies from 'js-cookie';
import VueResource from 'vue-resource';

import App from './App';
import router from './router';
import store from './store';

import './assets/main.css';

sync(store, router);
Vue.config.productionTip = false;

Vue.use(Vuex);
Vue.use(VueResource);

Vue.http.interceptors.push((request, next) => {
  const token = Cookies.get('csrftoken');
  request.headers.set('X-CSRFToken', token);

  next();
});

Vue.http.options.root = '/api/v1';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
});
