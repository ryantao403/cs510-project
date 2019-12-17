import Vue from 'vue'
import Vuex from 'vuex'
import $ from 'jquery'
Vue.use(Vuex)

//const API_URL = 'http://yirant2.web.illinois.edu'
const API_URL = 'http://127.0.0.1:5000/'

export default new Vuex.Store({
    state: {
        documents: [],
        selectedTopics: [],
        docRecommendation: [],
        doc: {},
	    suggestions: [],
        dummy: 'dummy'
    },
    mutations: {
        setDocuments (state, documents) {
            state.documents = documents
        },
        setSelectedTopics(state, topics) {
            //console.log('selected: ', topics)
            state.selectedTopics = topics
        },
    	setSuggestions(state, suggestions) {
    	    state.suggestions = suggestions
    	},
        setDocRecommendation(state, recommendation){
            state.docRecommendation = recommendation.recommendation
            state.doc = recommendation.paper
        },
    },
    getters: {
        filteredDocuments: state => {
            if(state.selectedTopics.length == 0) {
                return state.documents
            } else {
                return state.documents.filter(doc => state.selectedTopics.includes(doc.area))
            }
        },
    	matchedSuggestions: state => {
    	    return state.suggestions
    	},
        recommendedDocs: state =>{
            return state.docRecommendation
        }
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
        },
	    getSuggests(state, payload) {
	       $.ajax({
                type: "POST",
                url: API_URL + '/search/suggest',
                data: {
                    query: payload.query
                },
                success: (res) => {
                    state.commit('setSuggestions', res)
		    payload.callback(res)
                },
                error: (ex) => {
                    console.log(e)
                }
            })
	    },
        getDocRecommendation(state, payload){
            $.ajax({
                type: "POST",
                url: API_URL + '/search/recommend',
                data: {
                    path: payload.path
                },
                success: (res) => {
                    state.commit('setDocRecommendation', res)
                },
                error: (ex) => {
                    console.log(e)
                }
            })
        }
    }
})
