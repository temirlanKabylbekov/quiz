import Vue from 'vue';

export default {
  namespaced: true,
  state: {
    quiz_list: {},
  },
  actions: {
    GET_QUIZ_LIST({ commit }) {
      return Vue.http.get('question_list/')
        .then((response) => {
          commit('SET_QUIZ_LIST', response.data);
        });
    },
  },
  mutations: {
    SET_QUIZ_LIST(state, quizList) {
      state.quiz_list = quizList.results;
    },
  },
};
