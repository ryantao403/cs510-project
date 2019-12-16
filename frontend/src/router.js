import Vue from 'vue';
import Router from 'vue-router';
import Search from './components/Search.vue';
import Page from './components/Page.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: Search,
    },
    {
        path: '/doc/:id',
        name: 'doc',
        component: Page,
    }
  ],
});