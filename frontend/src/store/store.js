import { createStore } from 'vuex';

export default createStore({
  state: {
    user: {
      role: null,  // Store user's role (e.g., 'HR', 'Manager', etc.)
    },
  },
  mutations: {
    setRole(state, role) {
      state.user.role = role;  // Update the user role in the state
    },
  },
  actions: {
    login({ commit }, { role }) {
      // Store the role retrieved from the backend upon login
      commit('setRole', role);
    },
  },
  getters: {
    userRole: (state) => state.user.role,  // Access the current user role
  },
});
