<template>
  <div id="detail-container">
    <el-card>
      <template v-slot:header>
        <h2>hhh</h2>
      </template>
      <div>
        <h1>发布者</h1>
        <el-col v-bind:span="8" v-bind:offset="10">
          <img id="img-container" v-bind:src=url alt="加载失败" v-on:click="showInfo"/>
          <div id="username-container">caixukun</div>
        </el-col>
        <div v-for="(index, value) in contactWay" v-bind:key="value">
          <el-row v-if="contactWay[value] !== emptyStr" id="contact-container">
            <el-col v-bind:span="8" v-bind:offset="9" v-if="value === 'phone'">
              <span>{{ '手机号码：' + contactWay[value] }}</span>
            </el-col>
            <el-col v-bind:span="8" v-bind:offset="9" v-if="value === 'weChat'">
              <span>{{ '微信：' + contactWay[value] }}</span>
            </el-col>
            <el-col v-bind:span="8" v-bind:offset="9" v-if="value === 'qq'">
              <span>{{ 'qq：' + contactWay[value] }}</span>
            </el-col>
            <el-col v-bind:span="8" v-bind:offset="9" v-if="value === 'other'">
              <span>{{ '其他联系方式：' + contactWay[value] }}</span>
            </el-col>
          </el-row>
        </div>
        <el-divider></el-divider>
        <h1>任务详情</h1>
        <el-row>
          <el-col v-bind:span="20" v-bind:offset="2" style="background-color: #2a98dd">caixukun...</el-col>
        </el-row>
        <el-row v-bind:gutter="20" style="margin-top: 30px">
          <el-col v-bind:span="5" style="padding-left: 50px">{{ startTime }}</el-col>
          <el-col v-bind:span="14">
            <el-slider v-bind:step="Math.floor(100 / timeDiff(startTime, endTime))"
                       v-bind:value="passTime(startTime)"
                       v-bind:format-tooltip="formatTooltip"
                       disabled></el-slider>
          </el-col>
          <el-col v-bind:span="5">{{ endTime }}</el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'OtherMissionsDetailPage',
  data () {
    return {
      url: 'https://oj.vmatrix.org.cn/img/default-avatar.b6541da3.png',
      contactWay: {
        phone: '17878787878',
        weChat: 'we-chat',
        qq: '',
        other: ''
      },
      emptyStr: '',
      startTime: '2019-06-09 00:00:00',
      endTime: '2019-06-10 23:59:59'
    }
  },
  methods: {
    showInfo () {
      console.log('show info')
    },

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

  }
}
</script>

<style scoped>
  #detail-container {
    margin: 0 50px 0 50px;
  }

  #img-container {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    cursor: pointer;
  }

  #username-container {
    margin: 0 0 10px 15px;
    font-weight: bold;
  }

  #contact-container {
    margin-bottom: 10px;
  }
</style>
