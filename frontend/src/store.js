import Vue from 'vue'
import Vuex from 'vuex'
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
        setDummyDocuments(state) {
            state.documents = [
                {
                    title: 'Fake title',
                    link: 'https://google.com',
                    abstract: 'Fake abstract'
                }
            ]
        }
    }
})
