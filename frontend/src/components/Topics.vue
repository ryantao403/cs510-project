<template>
    <el-select v-model="selectedTopics" multiple placeholder="Topics">
    <el-option
      v-for="topic in topics"
      :key="topic"
      :label="topic"
      :value="topic">
    </el-option>
  </el-select>
</template>

<script>
  export default {
    data() {
      return {
        topics: ['machine translation', 'statistical machine translation', 'computational linguistics', 'sentiment analysis', 'natural language processing', 'dependency parsing', 'named entity recognition', 'question answering', 'speech tagging', 'neural machine translation', 'coreference resolution', 'information extraction', 'document summarization', 'domain adaptation', 'social media'],
        selectedTopics: []
      }
    },
    methods: {
      search() {
        this.$store.dispatch('search', this.query)
      }
    }
  }
</script>

<style scoped>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
</style>