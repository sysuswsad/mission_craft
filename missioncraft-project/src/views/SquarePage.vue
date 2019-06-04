<template>
  <div class="waterfall-container">
    <vue-waterfall-easy
      v-bind:imgs-arr="missionData"
      v-bind:is-router-link="true"
      v-bind:gap="30"
      class="mission-waterfall"
      ref="waterfall">

      <template v-slot:waterfall-head>
        <el-card shadow="hover" class="filter-container" v-bind:body-style="{ padding: '1.5rem 4rem' }">
          <el-form class="mission-filter" v-model="filter">

            <el-form-item label="任务类型" prop="type" class="filter-item">
              <el-checkbox-group v-model="filter.type" v-on:change="filterWithType">
                <el-checkbox label="问卷" name="type"></el-checkbox>
                <el-checkbox label="其他" name="type"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>

            <el-form-item label="最低报酬" prop="reward" class="filter-item">
              <el-input-number
                placeholder="请输入数字"
                size="small"
                v-model="filter.minReward"
                v-bind:controls="false"
                v-bind:min="0">
              </el-input-number>
              <el-button type="text" style="margin-left: 10px" v-on:click="filterWithMin">确定</el-button>
              <el-button type="text" v-on:click="resetFilterWithMin">重置</el-button>
            </el-form-item>

          </el-form>
          <el-button v-on:click="test">+</el-button>
        </el-card>
      </template>

      <template v-slot:default="descriptionProps">
        <div class="mission-info">
          <p>第{{ descriptionProps.index + 1 }}</p>
          <p>{{ descriptionProps.value.type }}</p>
          <p>{{ descriptionProps.value.reward }}</p>
        </div>
      </template>

      <template v-slot:loading>
        <div v-loading="dataLoading"></div>
      </template>

    </vue-waterfall-easy>
  </div>
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
      minConfirmDisable: false,
      allData: [],
      missionData: [
        { href: 'login', type: '问卷', reward: 0.4 }
      ],
      dataLoading: true
    }
  },

  methods: {
    test () {
      let temp = Math.random() > 0.5 ? { href: 'login', type: '问卷', reward: 0.4 }
        : { href: 'login', type: '其他', reward: 0.7 }
      this.missionData.push(temp)
      this.allData = this.missionData
    },

    filterWithType (newVal) {
      this.missionData =
        this.allData.filter(mission => newVal.includes(mission.type))

      if (this.filter.minReward !== 0) {
        this.filterWithMin()
      }
    },

    filterWithMin () {
      if (this.filter.minReward === 0) {
        this.resetFilterWithMin()
      } else {
        this.missionData =
          this.missionData.filter(mission => mission.reward >= this.filter.minReward, this)
      }
    },

    resetFilterWithMin () {
      this.missionData = this.allData
      this.filter.minReward = 0
    }
  }
}
</script>

<style scoped>
  .waterfall-container {
    height: 100%;
  }

  .mission-info {
    padding: .618rem 1rem;
  }

  .filter-container {
    margin-bottom: 2.5rem;
    margin-left: 10rem;
    margin-right: 10rem;
  }

  .filter-container .filter-item {
    margin: 0;
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
    transition: transform .2s ease;
  }

  .mission-waterfall a:hover {
    transform: translateY(-8px);
  }
</style>
