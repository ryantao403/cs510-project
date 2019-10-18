<template>
  <div class="main">
    <QueryInput />
    <DocumentTable />
        <div>
        <p>{{ msg }}</p>
      </div>
  </div>
</template>

<script>
import QueryInput from './QueryInput.vue'
import DocumentTable from './DocumentTable'
import axios from 'axios';

export default {
  name: 'Main',
  components: {
    QueryInput,
    DocumentTable
  },
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/results';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
