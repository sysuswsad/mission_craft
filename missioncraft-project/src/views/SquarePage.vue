<template>
  <vue-waterfall-easy
    v-bind:imgs-arr="missionData"
    v-bind:is-router-link="true"
    v-bind:gap="30"
    class="mission-waterfall"
    ref="waterfall">

    <template v-slot:waterfall-head>
      <el-card shadow="hover" class="filter-container" v-bind:body-style="{ padding: '2rem 3.23rem' }">
        <el-form class="mission-filter" v-model="filter">
          <el-form-item label="任务类型" prop="type">
            <el-checkbox-group v-model="filter.type">
              <el-checkbox label="问卷" name="type"></el-checkbox>
              <el-checkbox label="其他" name="type"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="最低报酬" prop="reward">
            <el-input-number
              placeholder="请输入数字"
              v-model="filter.minReward"
              v-bind:controls="false"
              v-bind:min="0">
            </el-input-number>
          </el-form-item>
        </el-form>
        <el-button v-on:click="test">+</el-button>
      </el-card>
    </template>

    <template v-slot:default="descriptionProps">
      <div class="mission-info">
        <p>第{{ descriptionProps.index + 1 }}</p>
        <p>{{ descriptionProps.value.href }}</p>
      </div>
    </template>

    <template v-slot:loading>
      <div v-loading="dataLoading"></div>
    </template>

  </vue-waterfall-easy>
</template>

<script>
import VueWaterfallEasy from 'vue-waterfall-easy/src/vue-waterfall-easy/vue-waterfall-easy'
export default {
  name: 'SquarePage',
  components: { VueWaterfallEasy },

  data () {
    return {
      filter: {
        type: ['问卷', '其他'],
        minReward: null
      },
      missionData: [
        { href: 'login' }
      ],
      dataLoading: true
    }
  },

  methods: {
    test () {
      this.missionData.push({ href: 'login' })
    }
  },

  created () {
    this.missionData = this.missionData.concat([{ href: 'login' }, { href: 'login' }])
  }
}
</script>

<style scoped>
  .mission-info {
    padding: .618rem 1rem;
  }

  .filter-container {
    margin-bottom: 2.5rem;
    margin-left: 7rem;
    margin-right: 7rem;
  }
</style>

<style>
  ::-webkit-scrollbar {
    display: none !important;
  }

  /* waterfall card style */
  .mission-waterfall a {
    text-decoration: none;
    color: grey;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04) !important;
    transition: transform .1s ease;
  }

  .mission-waterfall a:hover {
    transform: translateY(-5px);
  }
</style>
