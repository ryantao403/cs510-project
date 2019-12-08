import Vue from 'vue'
import Vuex from 'vuex'
import $ from 'jquery'
Vue.use(Vuex)

//const API_URL = 'http://yirant2.web.illinois.edu'
const API_URL = 'http://127.0.0.1:5000/'

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
                url: API_URL + '/search/query',
                data: {
                    query: query
                },
                success: (res) => {
                    state.commit('setDocuments', res)
                },
                error: (ex) => {
                    console.log(e)
                }
            })
        },
        markRelevance(state, payload) {
            $.ajax({
                type: "POST",
                url: API_URL + '/search/relevance',
                data: {
                    title: payload.title,
                    path: payload.path,
                    relevant: payload.relevant
                },
                success: (res) => {
                    console.log(res.title + ' ' + res.relevant)
                },
                error: (ex) => {
                    console.log(e)
                }
            })
        }
    }
})
