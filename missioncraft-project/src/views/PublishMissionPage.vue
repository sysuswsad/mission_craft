<template>
  <div>
    <el-card style="position: relative">
      <div style="width: 50%">
        <el-col style="margin-bottom: 1rem">
          <span style="font-size: 20px; font-weight:bold">任务详情</span>
        </el-col>
        <el-form label-width="100px" class="description-form" v-model="descriptionFrom" ref="descriptionFrom">
          <el-form-item label="任务标题" required>
            <el-col v-bind:span="18">
              <el-input type="textarea" placeholder="例如：取快递" v-model="descriptionFrom.title"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="任务描述" required>
            <el-col v-bind:span="18">
              <el-input type="textarea" placeholder="请输入任务描述" v-model="descriptionFrom.description"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="任务截至时间">
            <el-col v-bind:span="8">
              <el-date-picker type="date" placeholder="选择日期" value-format="yyyy-MM-dd" v-model="descriptionFrom.date.date1" style="width: 100%;"></el-date-picker>
            </el-col>
            <el-col v-bind:span="0.1">-</el-col>
            <el-col v-bind:span="8">
              <el-time-picker placeholder="选择时间" value-format="hh:mm:ss" v-model="descriptionFrom.date.date2" style="width: 100%;"></el-time-picker>
            </el-col>
          </el-form-item>
        </el-form>
        <br>
        <br>
        <el-col style="margin-bottom: 1rem">
          <span style="font-size: 20px; font-weight:bold" class="tip">联系方式</span>
        </el-col>
        <el-form v-bind:model="contactWay" label-width="100px" ref="contactWay" v-bind:rules="rules">
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                label="电话"
                prop="phone">
                <el-input v-model="contactWay.phone" placeholder="电话号码" type="text" prefix-icon="el-icon-mobile-phone"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                      label="微信"
                      prop="weChat">
                <el-input v-model="contactWay.weChat" placeholder="微信" type="text" prefix-icon="el-icon-chat-dot-square"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                label="QQ"
                prop="qq">
                <el-input v-model="contactWay.qq" placeholder="QQ" type="text" prefix-icon="el-icon-position"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                label="其他"
                prop="other">
                <el-input v-model="contactWay.other" placeholder="其他" type="text" prefix-icon="el-icon-s-home"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      <div style="width:45%;height:100%;position:absolute;right:0;bottom:0">
        <el-image
          :src="url"
          fit="cover"
          style="position: absolute;bottom: 0"
        ></el-image>
      </div>
    </el-card>
    <el-card class="pay-card">
      <template v-slot:header>
        <span style="font-size: 20px; font-weight:bold">结算</span>
      </template>
      <el-form label-width="100px" v-bind:model="payForm" ref="payForm">
        <el-row>
          <el-col v-bind:span="12">
            <el-form-item
              label="报酬"
              prop="payment"
              v-bind:rules="[
                { required: true, message: '报酬不能为空', trigger: 'blur' },
                { pattern: /^[0-9]*$/, message: '输入必须是数字', trigger: ['blur', 'change'] }
               ]">
              <el-input v-model="payForm.payment" placeholder="报酬" type="text"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-button class="submit-button" type="primary" v-on:click="submit('payForm', 'contactWay')">提交</el-button>
    </el-card>
  </div>
</template>

<script>
import backend from './../backend'
export default {
  name: 'PublishMissionPage',
  data () {
    return {
      descriptionFrom: {
        description: '',
        title: '',
        date: {
          date1: '',
          date2: ''
        }
      },
      payForm: {
        payment: ''
      },
      contactWay: {
        phone: '',
        weChat: '',
        qq: '',
        other: ''
      },
      url: '',
      rules: {
        phone: [
          {
            pattern: /^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$/,
            message: '电话号码格式有误'
          }
        ],
        weChat: [
          {
            pattern: /^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}$/,
            message: '微信号格式有误'
          }
        ],
        qq: [
          {
            pattern: /^[1-9]\d{4,9}$/,
            message: 'QQ号格式有误'
          }
        ]
      }
    }
  },

  methods: {
    submit (formName, t) {
      this.$refs[formName].validate((valid) => {
        if (!valid) {
          return false
        } else {
          this.$refs[t].validate((valid1) => {
            if (!valid1) {
              return false
            } else {
              if (this.contactWay.weChat === '' && this.contactWay.phone === '' && this.contactWay.qq === '' && this.contactWay.other === '') {
                this.$message.error('至少填写一种联系方式')
              } else if (this.descriptionFrom.title === '' || this.descriptionFrom.description === '') {
                this.$message.error('任务描述或者任务标题不能为空')
              } else {
                this.$confirm('确定发布此任务?', '提示', {
                  confirmButtonText: '确定',
                  cancelButtonText: '取消',
                  type: 'warning'
                }).then(() => {
                  setTimeout(() => {
                    backend.postRequest('mission/',
                      {
                        type: '1',
                        deadline: this.descriptionFrom.date.date1 + ' ' + this.descriptionFrom.date.date2,
                        title: this.descriptionFrom.title,
                        description: this.descriptionFrom.description,
                        qq: this.contactWay.qq,
                        wechat: this.contactWay.weChat,
                        phone: this.contactWay.phone,
                        other_way: this.contactWay.other,
                        bounty: this.payForm.payment
                      })
                      .then((response) => {
                        this.$message({
                          type: 'success',
                          message: '发布成功!'
                        })
                        this.$router.push({ name: 'square' })
                      })
                      .catch(() => {
                      })
                  })
                }).catch(() => {
                  this.$message({
                    type: 'info',
                    message: '已取消删除'
                  })
                })
              }
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped>
  .pay-card {
    margin-top: 1rem;
  }

  .submit-button {
    margin-left: 100px;
  }

  .tip::after {
    vertical-align: text-bottom;
    content: '  注：至少填写一种联系方式';
    font-size: 10px;
    color: red;
  }
</style>
