<template>
  <div class="b-quiz-list">
    <header class="b-quiz-list__header">Список опросов</header>
    <table class="b-quiz-list__table table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Дата создания</th>
        </tr>
      </thead>
      <tbody>
        <tr class="b-quiz" :class="{'b-quiz--passed': quiz.passed}"
            v-for="quiz in quizList" :key="quiz.id">
          <td><a :href="quiz.url" class="g-link">{{ quiz.name }}</a></td>
          <td>{{ quizDate(quiz) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import moment from 'moment';

export default {
  computed: {
    ...mapState({
      quizList: state => state.quizlist.quiz_list,
    }),
  },
  methods: {
    quizDate(quiz) {
      moment.locale('ru');
      return moment(quiz.created).format('D MMMM, h:mm:ss');
    },
  },
  beforeMount() {
    this.$store.dispatch('quizlist/GET_QUIZ_LIST');
  },
};
</script>

<style scoped>
.b-quiz-list {
  display: flex;
  justify-content: center;
  flex-direction: column;
}
  .b-quiz-list__header {
    align-self: center;
    font-size: 2.5rem;
    margin-bottom: 2rem;
  }
  .b-quiz-list__table {
    align-self: center;
  }
    .b-quiz:hover {
      background: #00d1b2;
    }
      .b-quiz--passed {
        color: black;
        opacity: 0.4;
      }
</style>
