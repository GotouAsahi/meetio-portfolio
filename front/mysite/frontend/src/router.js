import { createRouter, createWebHistory } from 'vue-router';
import { nextTick } from 'vue';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import PostDetails from './components/portfolio/PostDetails';
import PostEdit from './components/portfolio/PostEdit';
import TopList from './components/portfolio/TopList';
import PostList from './components/portfolio/PostList'
import UserShow from './components/portfolio/UserShow';
import PostView from './components/portfolio/PostView';
import ChangePassword from './components/portfolio/ChangePassword';
import SchoolUser from './components/portfolio/SchoolUser';
import JudgeTop from './components/judge/JudgeTop';
import JudgeIndex from './components/judge/JudgeIndex';
import JudgeForm from './components/judge/JudgeForm';
import JudgeContest from './components/judge/JudgeContest';
import DraftList from './components/portfolio/DraftList';
import DraftEdit from './components/portfolio/DraftEdit';
import HelpPage from './components/HelpPage';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'TopList',
      path: '/',
      component: TopList
    },
    {
      name: 'SignupForm',
      path: '/signup',
      component: SignupForm,
    },
    {
      name: 'LoginForm',
      path: '/login',
      component: LoginForm,
    },
    {
      name: 'PostDetails',
      path: '/portfolio/:id',
      component: PostDetails
    },
    {
      name: 'PostEdit',
      path: '/portfolio/edit/:id',
      component: PostEdit
    },
    {
      name: 'UserShow',
      path: '/user/:id',
      component: UserShow
    },
    {
      name: 'PostView',
      path: '/portfolio/new',
      component: PostView
    },
    {
      name: 'ChangePassword',
      path: '/user/password',
      component: ChangePassword
    },
    {
      name: 'SchoolUser',
      path: '/search/user',
      component: SchoolUser
    },
    {
      name: 'PostList',
      path: '/search/:key',
      component: PostList,
      props: true
    },
    {
      name: 'JudgeTop',
      path: '/skill',
      component: JudgeTop
    },
    {
      name: 'JudgeIndex',
      path: '/skill/:key',
      component: JudgeIndex,
      props: true
    },
    {
      name: 'JudgeForm',
      path: '/skill/form/:group_id/:id',
      component: JudgeForm
    },
    {
      name: 'JudgeContest',
      path: '/skill/contest/:id',
      component: JudgeContest
    },
    {
      name: 'DraftList',
      path: '/portfolio/draft/:id',
      component: DraftList
    },
    {
      name: 'DraftEdit',
      path: '/portfolio/draft/edit/:id',
      component: DraftEdit
    },
    {
      name: 'HelpPage',
      path: '/help',
      component: HelpPage
    },
  ],
});

router.beforeEach((to, from, next) => {
  // タイミングの調整のために非同期で処理する
  // 次のループでスクロールをトップに戻す
  nextTick(() => {
    window.scrollTo(0, 0);
  });
  next();
});

export default router;
