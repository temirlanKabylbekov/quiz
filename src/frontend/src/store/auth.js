import Vue from 'vue';
import _ from 'lodash';

export default {
  namespaced: true,
  state: {
    user: null,
  },
  actions: {
    GET_WHOAMI({ commit }) {
      return Vue.http.get('whoami/')
        .then((response) => {
          if (response.ok && _.isObject(response.data)) {
            commit('SET_USER', response.data);
          }
        });
    },
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
  },
};
