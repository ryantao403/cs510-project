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
                    id: 0,
                    title: 'Fake title 1',
                    link: 'https://google.com',
                    abstract: 'Fake abstract 1'
                },
                {
                    id: 1,
                    title: 'Fake title 2',
                    link: 'https://google.com',
                    abstract: 'Fake abstract 2'
                },
                {
                    id: 2,
                    title: 'Fake title 3',
                    link: 'https://google.com',
                    abstract: 'Fake abstract 3'
                }
            ]
            console.log('setDummyDocuments')
        }
    }
})
