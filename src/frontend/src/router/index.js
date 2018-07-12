import Vue from 'vue';
import Router from 'vue-router';

import QuizList from '@/components/QuizList';
import Quiz from '@/components/Quiz';
import ErrorPage from '@/components/ErrorPage';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'QuizList',
      component: QuizList,
    },
    {
      path: '/quiz/:id/',
      name: 'Quiz',
      component: Quiz,
    },
    {
      path: '*',
      name: 'ErrorPage',
      component: ErrorPage,
    },
  ],
});
