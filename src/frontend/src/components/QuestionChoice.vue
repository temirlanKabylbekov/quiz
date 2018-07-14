<template>
  <div class="b-choice" :class="{'b-choice--selectable': !passed}" @click="onClick">
    <progress class="b-choice__progress g-progress progress is-large is-primary"
      :class="{'g-progress--show-value': passed, 'g-progress--selectness': checked}"
      :value="percent" :text="choice.text" max="100"></progress>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: {
    choice: { type: Object, required: true },
    questionId: { type: Number, required: true },
    checked: { type: Boolean, required: true },
  },
  computed: {
    percent() {
      if (this.passed) {
        return this.$store.getters['quiz/getChoiceStats'](this.questionId, this.choice.id);
      }
      return 0;
    },
    ...mapGetters({
      passed: 'quiz/quizHasPassed',
    }),
  },
  methods: {
    onClick() {
      this.$emit('choiceChecked', this.choice.id);
    },
  },
};
</script>

<style scoped>
.b-choice--selectable:hover {
  cursor: pointer;
}
.b-choice__progress {
  width: 30rem;
  margin: 1rem auto;
}
.b-choice__text {
  position: relative;
  top: 20px;
}

</style>
