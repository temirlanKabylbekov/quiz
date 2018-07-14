<template>
  <article class="b-question">
    <header class="b-question__text">{{ question.text }}</header>
    <QuestionChoice v-for="choice in question.choices" :key="choice.id"
      :choice="choice" :questionId="question.id" :checked="checkChoice(choice.id)"
      @choiceChecked="choiceChecked">
      </QuestionChoice>
  </article>
</template>

<script>
import { mapGetters } from 'vuex';

import QuestionChoice from '@/components/QuestionChoice';

export default {
  props: {
    question: { type: Object, required: true },
  },
  data() {
    return {
      checkedChoice: null,
    };
  },
  computed: {
    ...mapGetters({
      passed: 'quiz/quizHasPassed',
    }),
  },
  methods: {
    choiceChecked(choiceId) {
      this.checkedChoice = choiceId;
      this.$emit('questionAnswered', this.question.id, choiceId);
    },
    checkChoice(choiceId) {
      if (this.passed) {
        return choiceId === this.$store.getters['quiz/getSelectedChoice'](this.question.id);
      }
      return this.checkedChoice === choiceId;
    },
  },
  components: {
    QuestionChoice,
  },
};
</script>

<style scoped>
.b-question {
  margin: 2rem auto;
  padding: 1rem;
  background: #E8E8E8;
  width: 32rem;
}
  .b-question__text {
    font-size: 1.5rem;
  }

</style>
