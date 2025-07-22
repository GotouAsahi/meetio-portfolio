import { createStore } from 'vuex'

const store = createStore({
  state: {
    isLoggedIn: false,
    icon: null
  },
  mutations: {
    setLoggedIn(state) {
      state.isLoggedIn = true;
    },
    setLoggedOut(state) {
      state.isLoggedIn = false;
    },
    setIcon(state, icon) {
      state.icon = icon
    }
  },
  actions: {
    login({ commit }) {
      commit('setLoggedIn');
    },
    logout({ commit }) {
      commit('setLoggedOut');
    },
  },
  getters: {
    isAuthenticated: state => state.isLoggedIn,
  },
})

export default store