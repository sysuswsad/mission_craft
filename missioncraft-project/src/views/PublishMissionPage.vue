<template>
  <div>
    <el-card style="position: relative">
      <div style="width: 50%">
        <template>
          <el-select v-model="missionType" placeholder="请选择任务类型">
            <el-option
                    v-for="item in types"
                    v-bind:key="item.value"
                    v-bind:label="item.label"
                    v-bind:value="item.value"
            >
              <span>{{ item.label }}</span>
            </el-option>
          </el-select>
        </template>
        <br>
        <br>
        <el-col style="margin-bottom: 1rem">
          <span style="font-size: 20px; font-weight:bold">任务详情</span>
        </el-col>
        <el-form label-width="100px" class="description-form" >
          <el-form-item label="任务描述">
            <el-col v-bind:span="18">
              <el-input type="textarea" placeholder="请输入任务描述"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="任务截至时间">
            <el-col v-bind:span="8">
              <el-date-picker type="date" placeholder="选择日期" v-model="date.date1" style="width: 100%;"></el-date-picker>
            </el-col>
            <el-col v-bind:span="0.1">-</el-col>
            <el-col v-bind:span="8">
              <el-time-picker placeholder="选择时间" v-model="date.date2" style="width: 100%;"></el-time-picker>
            </el-col>
          </el-form-item>
        </el-form>
        <br>
        <br>
        <el-col style="margin-bottom: 1rem">
          <span style="font-size: 20px; font-weight:bold" class="tip">联系方式</span>
        </el-col>
        <el-form v-bind:model="contactWay" label-width="100px">
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                      label="电话"
                      v-bind:rules="{message: '请输入电话号码'}">
                <el-input v-model="contactWay.phone" placeholder="电话号码" type="text" prefix-icon="el-icon-mobile-phone"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                      label="微信"
                      v-bind:rules="{message: '请输入微信'}">
                <el-input v-model="contactWay.weChat" placeholder="微信" type="text" prefix-icon="el-icon-chat-dot-square"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                      label="QQ"
                      v-bind:rules="{message: '请输入QQ'}">
                <el-input v-model="contactWay.qq" placeholder="QQ" type="text" prefix-icon="el-icon-position"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col v-bind:span="18">
              <el-form-item
                      label="其他"
                      v-bind:rules="{message: '请输入其他联系方式'}">
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
      <el-form label-width="100px">
        <el-row>
          <el-col v-bind:span="12">
            <el-form-item
                    label="报酬"
                    v-bind:rules="{message: '请输入报酬'}">
              <el-input v-model="payment" placeholder="报酬" type="text"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-button class="submit-button" type="primary">提交</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'PublishMissionPage',
  data () {
    return {
      missionType: '',
      payment: '',
      types: [
        {
          value: 0,
          label: '取快递'
        },
        {
          value: 1,
          label: '线下辅导'
        }
      ],
      contactWay: {
        phone: '',
        weChat: '',
        qq: '',
        other: ''
      },
      date: {
        date1: '',
        date2: ''
      },
      url: 'http://img06.tooopen.com/images/20170620/tooopen_sy_214616016323.jpg'
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
