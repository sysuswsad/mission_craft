<template>
  <div class="waterfall-container">
    <vue-waterfall-easy
      v-on:click="checkProfile"
      v-on:scrollReachBottom="fetchMissionRemotely"
      v-bind:imgs-arr="missionInfo"
      v-bind:is-router-link="true"
      v-bind:gap="30"
      v-bind:img-width="320"
      class="mission-waterfall"
      ref="waterfall">

      <template v-slot:waterfall-head>
        <el-card shadow="hover" class="filter-container" v-bind:body-style="{ padding: '1.5rem 4rem' }">
          <el-form class="mission-filter" v-bind:model="filter">

            <el-form-item label="任务类型" prop="type" class="filter-item">
              <el-checkbox-group v-model="filter.type" v-on:change="filterWithType">
                <el-checkbox label="0" name="type">问卷</el-checkbox>
                <el-checkbox label="1" name="type">其他</el-checkbox>
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
        </el-card>
      </template>

      <template v-slot:default="descriptionProps">
        <el-container>

          <el-header style="border-bottom: 1px solid #dcdfe6">
            <h4>
              {{ descriptionProps.value.title }}
            </h4>
          </el-header>

          <el-main class="mission-info-container">
            <el-row type="inline-flex" align="center" justify="space-between">
              <el-col v-bind:span="11" style="display: inline-flex">
                <i v-if="descriptionProps.value.type === 0" class="material-icons blue">assignment</i>
                <i v-else class="material-icons green">directions_run</i>
                <strong>&nbsp;{{ descriptionProps.value.type === 0 ? '问卷' : '其他' }}</strong>
              </el-col>

              <el-col v-bind:span="2">
                <el-divider direction="vertical"></el-divider>
              </el-col>

              <el-col v-bind:span="11" style="display: inline-flex; justify-content: flex-end">
                <i class="material-icons gold">monetization_on</i>
                <span>&nbsp;{{ descriptionProps.value.bounty }}</span>
              </el-col>
            </el-row>

            <el-row class="mission-desc-wrapper">
              {{ descriptionProps.value.description }}
            </el-row>
          </el-main>

          <el-footer class="mission-publisher-info-wrapper">
            <div class="publisher-avatar-wrapper">
              <el-image src="default-avatar.png" alt="avatar" fit="scale-down"></el-image>
            </div>
            <div class="publisher-username">{{ descriptionProps.value.username }}</div>
            <div>发布于 {{ descriptionProps.value.create_time }}</div>
          </el-footer>

        </el-container>
      </template>

      <template v-slot:loading>
        <div v-loading="dataLoading"></div>
      </template>

      <template v-slot:waterfall-over>
        <div>没有更多啦！</div>
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

        <!-- dialog used to confirm contact -->
        <el-dialog
          v-bind:visible.sync="contactConfirmVisible"
          v-bind:show-close="false"
          width="30%"
          append-to-body>

          <template v-slot:title>
            <el-row style="border-bottom: 1px solid #eeeeee">
              <h3>联系方式</h3>
            </el-row>
          </template>

          <template v-slot:footer>
            <el-button v-on:click="resetContact">取 消</el-button>
            <el-button type="primary" v-on:click="confirmAcceptance">确 认</el-button>
          </template>

          <template v-slot:default>
            <el-row>
              <strong>请确认您的联系方式：</strong>
            </el-row>
            <el-row style="margin-top: 1rem">
              <el-form v-bind:model="contactInfo" ref="contactForm" v-bind:rules="contactRules" label-width="80px">
                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model.number="contactInfo.phone"></el-input>
                </el-form-item>
                <el-form-item label="QQ" prop="qq">
                  <el-input v-model.number="contactInfo.qq"></el-input>
                </el-form-item>
                <el-form-item label="微信" prop="wechat">
                  <el-input v-model="contactInfo.wechat"></el-input>
                </el-form-item>
                <el-form-item label="其他" prop="others">
                  <el-input v-model="contactInfo.others"></el-input>
                </el-form-item>
              </el-form>
            </el-row>
          </template>

        </el-dialog>

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
                  <span>{{ missionProfile.username }}</span>
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
              <p>{{ missionProfile.description }}</p>
            </el-row>
            <el-row>
              <p><i class="el-icon-coin"></i>&nbsp;任务报酬：{{ missionProfile.bounty }}</p>
            </el-row>
          </el-col>

        </el-row>

        <el-divider></el-divider>

        <el-row style="margin-top: 40px">
          <TimeSlider
            v-bind:start-time="missionProfile.createTime"
            v-bind:end-time="missionProfile.deadline">
          </TimeSlider>
        </el-row>

      </template>
    </el-dialog>
  </div>
</template>

<script>
import VueWaterfallEasy from 'vue-waterfall-easy/src/vue-waterfall-easy/vue-waterfall-easy'
import $backend from '../backend'
import TimeSlider from '../components/TimeSlider'
export default {
  name: 'SquarePage',
  components: {TimeSlider, VueWaterfallEasy },

  data () {
    function validateEmpty (_this) {
      return _this.contactInfo.phone.toString().length === 0 && _this.contactInfo.qq.toString().length === 0 &&
        _this.contactInfo.wechat.length === 0 && _this.contactInfo.others.length === 0
    }

    const validatePhoneAndQQ = (rule, value, callback) => {
      if (validateEmpty(this))
        callback(new Error('请至少填写一项'))

      if (value.toString().length > 0 && !Number.isInteger(value)) {
        callback(new Error('请输入数字'))
      } else {
        callback()
      }
    }

    const validateOthers = (rule, value, callback) => {
      if (validateEmpty(this)) {
        callback(new Error('请至少填写一项'))
      } else {
        callback()
      }
    }

    return {
      filter: {
        type: ['0', '1'],
        minReward: null
      },
      missionInfo: [],
      dataLoading: true,
      profileLoading: false,
      profileVisible: false,
      contactConfirmVisible: false,
      contactInfo: {
        phone: '',
        qq: '',
        wechat: '',
        others: ''
      },
      contactRules: {
        phone: [{ validator: validatePhoneAndQQ, trigger: 'blur' }],
        qq: [{ validator: validatePhoneAndQQ, trigger: 'blur' }],
        wechat: [{ validator: validateOthers, trigger: 'blur' }],
        others: [{ validator: validateOthers, trigger: 'blur' }]
      },
      missionProfile: {
        id: '',
        username: '',
        type: 0,
        avatar: '',
        title: '',
        createTime: '',
        deadline: '',
        description: '',
        bounty: -1
      }
    }
  },

  methods: {
    filterWithType (typeVal) {
      this.missionInfo =
        this.allMissionInfo.filter(mission =>
          typeVal.includes(mission.type.toString()) && mission.bounty >= this.filter.minReward, this)
    },

    filterWithMin () {
      this.filterWithType(this.filter.type)
    },

    resetFilterWithMin () {
      this.missionInfo =
        this.allMissionInfo.filter(mission => this.filter.type.includes(mission.type.toString()), this)
      this.filter.minReward = 0
    },

    checkProfile (event, { index, value }) {
      event.preventDefault()

      this.missionProfile.id = value.idMissionInfo
      this.missionProfile.username = value.username
      this.missionProfile.type = value.type
      this.missionProfile.avatar = value.avatar
      this.missionProfile.title = value.title
      this.missionProfile.createTime = value.create_time
      this.missionProfile.deadline = value.deadline
      this.missionProfile.description = value.description
      this.missionProfile.bounty = value.bounty

      this.profileVisible = true
    },

    acceptMission () {
      if (this.missionProfile.type === 1) {
        this.contactInfo.phone = this.$store.state.userInfo.phone
        this.contactInfo.qq = this.$store.state.userInfo.qq
        this.contactInfo.wechat = this.$store.state.userInfo.wechat

        this.contactConfirmVisible = true
      } else {
        $backend.postRequest('order/', {
          mission_id: this.missionProfile.id
        }).then(response => {
          this.$confirm(`您已成功领取任务 ${this.missionProfile.title} ！是否立即前往填写问卷？`, '领取成功', {
            confirmButtonText: '前 往',
            cancelButtonText: '稍 后',
            type: 'success'
          }).then(() => {
            this.profileVisible = false

            this.$router.push({
              name: 'answerQuestionnaire',
              params: {
                missionId: this.missionProfile.id,
                orderId: response.data.data.order_id
              }
            })
          })
        }).catch(error => {
          console.log(error)
          this.$message.error('出错了，请稍后重试')
        })
      }
    },

    confirmAcceptance () {
      this.$refs.contactForm.validate().then(() => {
        console.log(`mission ID: ${this.missionProfile.id}`)
        return $backend.postRequest('order/', {
          mission_id: this.missionProfile.id,
          phone: this.contactInfo.phone,
          qq: this.contactInfo.qq,
          wechat: this.contactInfo.wechat,
          other_way: this.contactInfo.others
        })
      }).catch(() => {
        return false
      }).then(response => {
        console.log(`response: ${response}`)
        if (typeof response === 'boolean' && !response) {
          return
        }

        this.contactConfirmVisible = false
        this.profileVisible = false

        this.$alert(`您已成功领取任务 ${this.missionProfile.title} ！可前往我的领取查看详情`, '领取成功')
      }).catch(error => {
        console.log(error)
        this.contactConfirmVisible = false
        this.$message.error('出错了，请稍后重试')
      })
    },

    resetContact () {
      this.contactConfirmVisible = false
      this.$refs.contactForm.resetFields()
    },

    fetchMissionRemotely (limit = 20) {
      return this.$store.dispatch('fetchMissionRemotely', {
        create_time: this.currentOldestMissionCreateTime,
        limit: limit
      }).then(noMoreMissions => {
        this.filterWithType(this.filter.type)

        if (noMoreMissions) {
          this.$refs.waterfall.waterfallOver()
        }
      })
    }
  },

  computed: {
    allMissionInfo () {
      return this.$store.state.missionInfo
    },

    currentOldestMissionCreateTime () {
      const missionInfo = this.$store.state.missionInfo
      if (missionInfo.length > 0) {
        return missionInfo[missionInfo.length - 1].create_time
      } else {
        return ''
      }
    }
  },

  watch: {
    contactInfo: {
      handler () {
        this.$refs.contactForm.clearValidate()
      },
      deep: true
    }
  },

  created () {
    this.fetchMissionRemotely().then(() => {
      this.missionInfo = this.allMissionInfo
    })
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
