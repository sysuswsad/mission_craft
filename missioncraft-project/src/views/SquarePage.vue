<template>
  <div class="waterfall-container">
    <vue-waterfall-easy
      v-on:click="checkProfile"
      v-bind:imgs-arr="missionData"
      v-bind:is-router-link="true"
      v-bind:gap="30"
      v-bind:img-width="320"
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
        <el-container>

          <el-header style="border-bottom: 1px solid #dcdfe6">
            <h4>
              这里是标题
            </h4>
          </el-header>

          <el-main class="mission-info-container">
            <el-row type="inline-flex" align="center" justify="space-between">
              <el-col v-bind:span="11" style="display: inline-flex">
                <i v-if="descriptionProps.value.type.localeCompare('问卷') === 0" class="material-icons blue">assignment</i>
                <i v-else class="material-icons green">directions_run</i>
                <strong>&nbsp;{{ descriptionProps.value.type }}</strong>
              </el-col>

              <el-col v-bind:span="2">
                <el-divider direction="vertical"></el-divider>
              </el-col>

              <el-col v-bind:span="11" style="display: inline-flex; justify-content: flex-end">
                <i class="material-icons gold">monetization_on</i>
                <span>&nbsp;{{ descriptionProps.value.reward }}</span>
              </el-col>
            </el-row>

            <el-row class="mission-desc-wrapper">
              我是很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的任务描述
            </el-row>
          </el-main>

          <el-footer class="mission-publisher-info-wrapper">
            <div class="publisher-avatar-wrapper">
              <el-image src="default-avatar.png" alt="avatar" fit="scale-down"></el-image>
            </div>
            <div class="publisher-username">这是一个比较长的用户名</div>
            <div>发布于 2020-01-01 12:13:24</div>
          </el-footer>

        </el-container>
      </template>

      <template v-slot:loading>
        <div v-loading="dataLoading"></div>
      </template>

    </vue-waterfall-easy>

    <el-dialog
      v-bind:visible.sync="profileVisible"
      v-bind:show-close="false"
      v-loading="profileLoading"
      ref="profileDialog"
      width="50%">

      <template v-slot:title>
        <el-row>
          <h3>任务详情</h3>
          <el-divider></el-divider>
        </el-row>
      </template>

      <template v-slot:footer>
        <el-button v-on:click="profileVisible = false">再看看</el-button>
        <el-button type="primary" v-on:click="acceptMission">接 受</el-button>
      </template>

      <template v-slot:default>
        <el-row type="flex" justify="center">

          <el-col v-bind:span="8">

            <el-row>
              <h4><i class="el-icon-user-solid"></i>&nbsp;发布者</h4>
            </el-row>

            <el-row v-bind:gutter="20" type="flex" justify="center">
              <el-col v-bind:span="7" style="display: flex; align-items: center">
                <el-image src="default-avatar.png" fit="contain" alt="avatar"></el-image>
              </el-col>
              <el-col v-bind:span="16">
                <el-row style="margin: 1rem 0">
                  <span>nickname</span>
                </el-row>
                <el-row style="margin: 1rem 0">
                  <strong>信誉积分？：213</strong>
                </el-row>
              </el-col>
            </el-row>

          </el-col>

          <el-col v-bind:span="2" style="display: flex; justify-content: center">
            <div class="vertical-divider"></div>
          </el-col>

          <el-col v-bind:span="15">
            <el-row>
              <h4><i class="el-icon-document"></i>&nbsp;任务描述</h4>
            </el-row>
            <el-row>
              <p>我是很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的任务描述</p>
            </el-row>
            <el-row>
              <p><i class="el-icon-coin"></i>&nbsp;任务报酬：{{ missionProfile.reward }}</p>
            </el-row>
          </el-col>

        </el-row>

        <el-divider></el-divider>

        <el-row type="flex" justify="center">
          <el-col v-bind:span="4">{{ missionProfile.createTime }}</el-col>
          <el-col v-bind:span="16">
            <el-slider
              v-bind:step="Math.floor(100 / timeDiff(missionProfile.createTime, missionProfile.deadline))"
              v-bind:value="passTime(missionProfile.createTime)"
              v-bind:format-tooltip="formatTooltip"
              disabled>
            </el-slider>
          </el-col>
          <el-col v-bind:span="4">{{ missionProfile.deadline }}</el-col>
        </el-row>

      </template>

    </el-dialog>
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
        { href: '#', type: '问卷', reward: 0.4 }
      ],
      dataLoading: true,
      profileLoading: false,
      profileVisible: false,
      missionProfile: {
        username: '',
        type: 0,
        avatar: '',
        title: '',
        createTime: '',
        deadline: '',
        description: '',
        reward: -1
      }
    }
  },

  methods: {
    test () {
      let temp = Math.random() > 0.5 ? { href: '#', type: '问卷', reward: 0.4 }
        : { href: '#', type: '其他', reward: 0.7 }
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
    },

    checkProfile (event, { index, value }) {
      event.preventDefault()
      this.profileVisible = true
    },

    acceptMission () {
      this.profileLoading = true
    },

    // --- same to ReceivedPage ---
    formatTooltip () {
      let startTime = Date.now()
      let endTime = new Date(this.endTime)
      let left = '剩余0天0时0分0秒'
      if (endTime.getTime() > startTime) {
        let msDiff = endTime.getTime() - startTime
        // compute day left
        let leftDay = Math.floor(msDiff / (1000 * 24 * 60 * 60))
        // hours left after computing day left
        let leaveForHour = msDiff % (1000 * 24 * 60 * 60)
        // compute hour left
        let leftHour = Math.floor(leaveForHour / (1000 * 60 * 60))
        let leaveForMinute = leaveForHour % (1000 * 3600)
        let leftMinute = Math.floor(leaveForMinute / (1000 * 60))
        let leaveForSecond = leaveForMinute % (1000 * 60)
        let leftSecond = Math.round(leaveForSecond / 1000)
        left = '剩余' + leftDay + '天' + leftHour + '时' + leftMinute + '分' + leftSecond + '秒'
      }
      return left
    },

    timeDiff (sTime, eTime) {
      let startTime = new Date(sTime)
      let endTime = new Date(eTime)
      let leftHour = 0
      if (endTime.getTime() > startTime.getTime()) {
        let msDiff = endTime.getTime() - startTime.getTime()
        leftHour = Math.floor(msDiff / (1000 * 3600))
      }
      return leftHour
    },

    passTime (startTime) {
      let nowTime = Date.now()
      let sTime = new Date(startTime)
      let passHour = 0
      if (nowTime > sTime.getTime()) {
        let msDiff = nowTime - sTime.getTime()
        passHour = Math.ceil(msDiff / (1000 * 3600))
      }
      return passHour * Math.floor(100 / this.$options.methods.timeDiff(startTime, this.endTime))
    }
    // --- ---
  }
}
</script>

<style scoped>
  .waterfall-container {
    height: 100%;
  }

  .filter-container {
    margin-bottom: 2.5rem;
    margin-left: 10rem;
    margin-right: 10rem;
  }

  .filter-container .filter-item {
    margin: 0;
  }

  .mission-info-container {
    padding: .75rem 1.25rem;
  }

  .mission-desc-wrapper {
    padding: 1.25rem 0;
  }

  .mission-publisher-info-wrapper {
    padding: .75rem 1.25rem;
    font-size: small;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .publisher-avatar-wrapper {
    width: 12%;
    border-radius: 50%;
  }

  .publisher-username {
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
  }

  .vertical-divider {
    width: 1px;
    display: inline-block;
    background-color: #DCDFE6;
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

  .material-icons.gold {
    color: #FFD700;
  }

  .material-icons.blue {
    color: #2b78fe;
  }

  .material-icons.green {
    color: #34a853;
  }
</style>
