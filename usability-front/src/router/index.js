import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HeuristicTest from '../views/HeuristicOwner.vue'
import HeuristicCheck from '../views/HeuristicCheck.vue'
import HeuristicProblems from '../views/HeuristicProblems.vue'
import HeuristicEvaluation from '../views/HeuristicEvaluation.vue'
import HeuristicEvaluationResult from '../views/HeuristicEvaluationResult.vue'
import ChecklistDone from '../views/ChecklistDone.vue'
/////////////////////////////////////////////////////////////////
import { useAuthStore } from '../stores/useAuthStore';
import Login from '../views/Loguin_2.vue'
import Register from '../views/Register_2.vue'
import DesignTest from '../views/DesignTests.vue'
import DesignQuestions from '../views/DesignQuestions.vue'
import EvaluatorAccess from '../views/EvaluatorAccess.vue'
import EvaluatorStandardResponses from '../views/EvaluatorStandardResponses.vue'
import EvaluatorHeuristicResponses from '../views/EvaluatorHeuristicResponses.vue'
import ResponsesView from '../views/ResponsesView.vue'
/////////////////////////////////////////////////////////////////
            
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/pruebasheuristicas',
      name: 'pruebaheuristica',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: HeuristicTest,
      meta: { requiresAuth: true }
    },
    {
      path: '/heuristicproblems',
      name: 'heuristicproblems',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: HeuristicProblems
      ,
      meta: { requiresAuth: true }
    },
    {
      path: '/o/:ownerId/evaluacion',
      name: 'heuristicevaluation',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: HeuristicEvaluation
      ,
      meta: { requiresAuth: true }
    },
    
    {
      path: '/o/:idowner/checklist',
      component: HeuristicCheck,
      meta: { requiresAuth: false }
    },
    {
      path: '/encuestaterminada',
      component: ChecklistDone
      ,
      meta: { requiresAuth: true }
    },
    {
      path: '/o/:ownerId/resultadoevaluacion', 
      component: HeuristicEvaluationResult,
      meta: { requiresAuth: true }
    },
///////////////////////////////////////////////////////////////////////////
    {
      name:'Design_Test',
      path: '/designtest', 
      component: DesignTest,
      meta: { requiresAuth: true }
    },
    {
      name:'Design_Questions',
      path: '/designtest/:testId/questionnaires', 
      component: DesignQuestions,
      meta: { requiresAuth: true }
    },

    {
      name:'Evaluator_Access',
      path: '/designtests/access/',
      component: EvaluatorAccess,
      meta: {requiresAuth: true}
    },
    
    {
      name:'Evaluator_Standard_Responses',
      path: '/questionnaires/:testId/standardresponses', 
      component: EvaluatorStandardResponses,
      meta: { requiresAuth: true }
    },
    {
      name:'Evaluator_Heuristic_Responses',
      path: '/questionnaires/:testId/heuristicresponses', 
      component: EvaluatorHeuristicResponses,
      meta: { requiresAuth: true }
    },
    {
      path: '/responses/:testId',
      name: 'responses',
      component: ResponsesView
    },
    ///////////////////
    //register
    { path: '/register', component: Register },
    //loguin
    { path: '/login', component: Login },
  ]


})
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const useAuth = useAuthStore()

  if (requiresAuth && !useAuth.isLoggedIn) {
    next('/login');
  } else {
    next();
  }
});
export default router
