<template>
  <ErrorPage v-if="show404" />
  <div v-else class="b-quiz">
    <header class="b-quiz__header b-quiz-header">
      <a href="/" class="b-quiz-header__return-back g-link">Вернуться к списку опросов</a>
      <p class="b-quiz-header__title">{{ quiz.name }}</p>
    </header>
    <SingleQuestion class="b-quiz__question"
      v-for="question in quiz.questions" :key="question.id" :question="question"
      @questionAnswered="questionAnswered"></SingleQuestion>
    <a class="b-quiz__submit button is-large"
       :class="{'b-quiz__submit--hidden': quiz.passed, 'is-loading': isLoading}"
       :disabled="disabled" @click="sendAnswers">Завершить</a>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import _ from 'lodash';

import ErrorPage from '@/components/ErrorPage';
import SingleQuestion from '@/components/SingleQuestion';

export default {
  data() {
    return {
      show404: false,
      isLoading: false,
      disabled: true,
      answers: [],
    };
  },
  computed: {
    ...mapState({
      quiz: state => state.quiz.quiz,
    }),
  },
  methods: {
    sendAnswers() {
      if (this.disabled) {
        return;
      }
      this.isLoading = true;
      this.$store.dispatch('quiz/SET_QUIZ_ANSWERS', { quizId: this.quiz.id, answers: JSON.stringify(this.answers) })
        .then(() => {
          this.isLoading = false;
        });
    },
    questionAnswered(questionId, choiceId) {
      this.setAnswerForQuestion(questionId, choiceId);
    },
    initAnswers() {
      _.forEach(this.quiz.questions, (el) => {
        this.answers.push({ question: el.id, choice: null });
      });
    },
    setAnswerForQuestion(questionId, choiceId) {
      const index = _.findIndex(this.answers, { question: questionId });
      this.answers[index].choice = choiceId;
      this.disabled = !_.isUndefined(_.find(this.answers, { choice: null }));
    },
  },
  mounted() {
    this.$store.dispatch('quiz/GET_QUIZ', { quizId: this.$route.params.id })
      .then(() => {
        this.show404 = false;
        this.initAnswers();
      })
      .catch(() => {
        this.show404 = true;
      });
  },
  components: {
    ErrorPage,
    SingleQuestion,
  },
};
</script>

<style scoped>
.b-quiz__submit {
  background: #00d1b2;
}
.b-quiz__submit--hidden {
  display: none;
}

  .b-quiz-header__return-back {
    display: block;
    margin-bottom: 3rem;
    font-size: 1rem;
  }
  .b-quiz-header__return-back:hover {
    color: #00d1b2;
  }
  .b-quiz-header__title {
    font-size: 2rem;
  }

</style>
