import Vue from 'vue';
import Vuex from 'vuex';
import auth from './auth';
import quiz from './quiz';
import quizlist from './quizlist';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    quiz,
    quizlist,
  },
  strict: true,
});
