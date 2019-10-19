import Vue from 'vue'
import Vuex from 'vuex'
import $ from 'jquery'
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        documents: [],
        dummy: 'dummy'
    },
    mutations: {
        setDocuments (state, documents) {
            state.documents = documents
        },        
    },
    actions: {
        search(state, query){
            $.ajax({
                type: "POST",
                url: '/search/query',
                data: {
                    query: query
                },
                success: (res) => {
                    state.commit('setDocuments', res)
                }
            })
        }
    }
})
