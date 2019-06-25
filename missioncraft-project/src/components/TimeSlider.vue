<template>
  <div>
    <el-row type="flex" align="middle">
      <el-col v-bind:span="5" style="text-align: center">{{ startTime }}</el-col>
      <el-col v-bind:span="14">
        <el-slider
            v-bind:step="Math.floor(100 / timeDiff(startTime, endTime))"
            v-bind:value="passTime(startTime, endTime, finishTime)"
            v-bind:format-tooltip="formatTooltip"
            disabled>
        </el-slider>
      </el-col>
      <el-col v-bind:span="5" style="text-align: center">{{ endTime }}</el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'TimeSlider',

  data () {
    return {
      deadline: ''
    }
  },

  props: {
    startTime: {
      type: String,
      default: ''
    },

    endTime: {
      type: String,
      default: ''
    },

    finNum: {
      type: Number,
      default: 0
    },

    missionState: {
      type: Number,
      default: 0
    },

    finishTime: {
      type: String,
      default: ''
    },

    orderState: {
      type: Number,
      default: 0
    }
  },

  created () {
    this.deadline = this.endTime
  },

  methods: {
    formatTooltip () {
      if (this.finNum !== 0 || this.orderState === 1) {
        return '已完成'
      } else if (this.missionState === 1 && this.finNum === 0 && this.orderState !== 2) {
        return '任务已结束或已取消（未完成）'
      } else if (this.orderState === 2) {
        return '任务已结束或已放弃（未完成）'
      }
      let startTime = Date.now()
      let eTime = new Date(this.deadline)
      let left = '任务未完成，已结束'
      if (eTime.getTime() > startTime) {
        let msDiff = eTime.getTime() - startTime
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

    passTime (startTime, endTime, finishTime) {
      let sTime = new Date(startTime)
      let nowTime = Date.now()
      let eTime = new Date(endTime)
      console.log(finishTime)
      if (this.finNum !== 0 || this.orderState === 1) {
        console.log(finishTime)
        let finTime = new Date(finishTime)
        let passHour = 0
        if (finTime.getTime() > sTime.getTime()) {
          let msDiff = finTime.getTime() - sTime.getTime()
          passHour = Math.ceil(msDiff / (1000 * 3600))
        }
        return passHour * (100.0 / this.timeDiff(startTime, endTime))
      } else if ((this.missionState === 1 && this.finNum === 0) || this.orderState === 2) {
        return 100
      }

      if (nowTime >= eTime.getTime()) {
        return 100
      }

      let passHour = 0
      if (nowTime > sTime.getTime()) {
        let msDiff = nowTime - sTime.getTime()
        passHour = Math.ceil(msDiff / (1000 * 3600))
      }
      return passHour * (100.0 / this.timeDiff(startTime, endTime))
    }
  }
}
</script>

<style scoped>

</style>
