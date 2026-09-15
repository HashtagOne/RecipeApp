import { createRouter, createWebHistory} from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import PublicFeedView from '../views/PublicFeedView.vue'
import RecipeFormView from '../views/RecipeFormView.vue'
import RecipeDetailView from '../views/RecipeDetailView.vue'
import { isLoggedIn, authReady } from '../auth.js'
import { watch } from 'vue'

const router = createRouter({
    history: createWebHistory('/Recipe-App/'),
    routes: [
        {
            path: '/login',
            component: LoginView
        },
        {
            path: '/register',
            component: RegisterView
        },
        {
            path: '/',
            component: PublicFeedView
        },
        {
            path: '/dashboard',
            component: DashboardView,
            meta: { requiresAuth: true }
        },
        {
            path: '/recipes/new',
            component: RecipeFormView,
            meta: { requiresAuth: true }
        },
        {
            path: '/recipes/:id/edit',
            component: RecipeFormView,
            meta: { requiresAuth: true }
        },
        {
            path: '/recipes/:id',
            component: RecipeDetailView
        },
    ]
})

router.beforeEach(async (to, from) => {
    if (!authReady.value) {
        await new Promise(resolve => {
            const stop = watch(authReady, (val) => {
                if (val) {
                    stop()
                    resolve()
                }
            })
        })
    }

    if (to.meta.requiresAuth && !isLoggedIn.value) {
        return '/login'
    }
})

export default router