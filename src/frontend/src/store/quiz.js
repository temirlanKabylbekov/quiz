import Vue from 'vue';
import _ from 'lodash';

export default {
  namespaced: true,
  state: {
    quiz: {},
    stats: {},
  },
  getters: {
    quizHasPassed: state => !_.isUndefined(state.quiz.passed) && state.quiz.passed,
    getChoiceStats: state => (questionId, choiceId) => {
      const question = _.find(state.stats, el => el.question_id === questionId);
      if (!_.isUndefined(question)) {
        const choice = _.find(question.stats, el => el.choice === choiceId);
        if (!_.isUndefined(choice)) {
          return choice.percent;
        }
      }
      return 0;
    },
    getSelectedChoice: state => (questionId) => {
      const question = _.find(state.stats, el => el.question_id === questionId);
      if (!_.isUndefined(question)) {
        return question.choice_id;
      }
      return 0;
    },
  },
  actions: {
    GET_QUIZ({ commit, dispatch }, { quizId }) {
      return Vue.http.get(`question_list/${quizId}/`)
        .then((response) => {
          commit('SET_QUIZ', response.data);
          dispatch('GET_QUIZ_STATS', { quizId });
        });
    },
    GET_QUIZ_STATS({ commit }, { quizId }) {
      return Vue.http.get(`question_list/${quizId}/answer_stats/`)
        .then(response => commit('SET_QUIZ_STATS', response.data));
    },
    SET_QUIZ_ANSWERS({ dispatch }, { quizId, answers }) {
      return Vue.http.post(`question_list/${quizId}/set_answers/`, { answers })
        .then(() => {
          dispatch('GET_QUIZ', { quizId });
          dispatch('GET_QUIZ_STATS', { quizId });
        });
    },
  },
  mutations: {
    SET_QUIZ(state, quiz) {
      state.quiz = quiz;
    },
    SET_QUIZ_STATS(state, stats) {
      state.stats = stats;
    },
  },
};
