import { createStore } from 'vuex';

export default createStore({
  state: {
    user: {
      role: null,
      username: null,
      supervisor: null,
      dept: null,
      email: null,
      position: null,
      id: null,
    },
    isAuthenticated: false,
  },
  mutations: {
    setRole(state, role) {
      state.user.role = role;  // Update the user role in the state
      state.isAuthenticated = true;
    },
    setUsername(state, username) {
      state.user.username = username;
    },
    setSupervisor(state, supervisor) {
      state.user.supervisor = supervisor;
    },
    setDept(state, dept) {
      state.user.dept = dept;
    },
    setEmail(state, email) {
      state.user.email = email;
    },
    setPosition(state, position) {
      state.user.position = position;
    },
    setId(state, user_id) {
      state.user.id = user_id;
    },
    logoutUser(state) {
      state.user = {
        role: null,
        username: null,
        supervisor: null,
        dept: null,
        email: null,
        position: null,
        user_id: null,
      };
      
      state.isAuthenticated = false; // Reset authenticated status
    },
  },
  actions: {
    login({ commit }, { role, username, supervisor, dept, email, position, userid }) {
      // Store the role and other user information retrieved from the backend upon login
      commit('setRole', role);
      commit('setUsername', username);
      commit('setSupervisor', supervisor);
      commit('setDept', dept);
      commit('setEmail', email);
      console.log('Setting user with position:', position);
      commit('setPosition', position);
      console.log('Setting user with ID:', userid);
     commit('setId', userid);
    },

    logout({ commit }) {
      commit('logoutUser'); // Call the logout mutation
    },
  },
  getters: {
    userRole: (state) => state.user.role,
    username: (state) => state.user.username,
    supervisor: (state) => state.user.supervisor,
    dept: (state) => state.user.dept,
    email: (state) => state.user.email,
    position: (state) => state.user.position,
    isAuthenticated: (state) => state.isAuthenticated,
    id:(state) => state.user.id,
}});
