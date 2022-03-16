<template>
  <view class="content">
    <view class="header">
      <image src="/static/login/logo.png"></image>
    </view>
    <view class="cu-load load-modal" v-if="requestLoading">
      <view class="gray-text">加载中...</view>
    </view>
    <view class="list">
      <view class="list-call">
        <image class="img" src="/static/login/1.png"></image>
        <input class="biaoti" v-model="username" type="text" maxlength="20" placeholder="输入账号或邮箱" />
      </view>
      <view class="list-call">
        <image class="img" src="/static/login/2.png"></image>
        <input class="biaoti" v-model="password" type="text" maxlength="32" placeholder="输入密码" password="true" />
      </view>
    </view>
    <view class="dlbutton" hover-class="dlbutton-hover" @tap="$u.throttle(bindLogin, 1000)">
      <text>登录</text>
    </view>
    <view class="xieyi">
      <navigator url="/pages/login/register/index" open-type="navigate">注册账户</navigator>
    </view>
    <view class="oauth-row" v-if="hasProvider" v-bind:style="{top: positionTop + 'px'}">
      <view class="oauth-image" v-for="provider in providerList" :key="provider.value">
        <image :src="provider.image" @tap="oauth(provider.value)"></image>
      </view>
    </view>
  </view>
</template>

<script>
  import md5Libs from "uview-ui/libs/function/md5"
  import {
    MobileLogin
  } from '@/api/login.js'
  export default {
    onReady() {
      this.initPosition()
      // 加载第三方oauth
      // this.initProvider()
    },
    data() {
      return {
        requestLoading: false,
        username: '',
        password: '',
        providerList: [], //第三方oauthlist
        hasProvider: false, //是否有第三方授权
        positionTop: 0
      };
    },
    onLoad(option) {
      if (option.mobile) {
        this.account = option.mobile
      }
    },
    methods: {
      initProvider() {
        const filters = ['weixin', 'qq', 'sinaweibo'];
        uni.getProvider({
          service: 'oauth',
          success: (res) => {
            console.log(res.provider)
            if (res.provider && res.provider.length) {
              for (let i = 0; i < res.provider.length; i++) {
                if (~filters.indexOf(res.provider[i])) {
                  this.providerList.push({
                    value: res.provider[i],
                    image: '/static/img/' + res.provider[i] + '.png'
                  });
                }
              }
              this.hasProvider = true;
            }
          },
          fail: (err) => {
            console.error('获取服务供应商失败：' + JSON.stringify(err));
          }
        });
      },
      initPosition() {
        /**
         * 使用 absolute 定位，并且设置 bottom 值进行定位。软键盘弹出时，底部会因为窗口变化而被顶上来。
         * 反向使用 top 进行定位，可以避免此问题。
         */
        this.positionTop = uni.getSystemInfoSync().windowHeight - 100;
      },
      bindLogin() {
        /**
         * 请求手机号登录接口
         */
        const param = {
          "username":this.username,
		  "password":this.password
        }
        this.requestLoading = true
        MobileLogin(param).then(res => {
		  console.log(res)
		  if(res.data.token){
			uni.showToast({
			    title: res.msg,
			    duration: 2000
			});
			uni.setStorageSync("lifeData", res.data)
			uni.setStorageSync("token", res.data.token)
			this.toMain()
		  }else{
			  uni.showToast({
			      title: res.msg,
			      duration: 2000,
				  icon:"error"
			  });
		  }
		  
          this.requestLoading = false
          
        }).catch((err) => {
          console.log('error', err)
          this.requestLoading = false
        })
      },
      oauth(value) { // oauth授权登录
        uni.login({
          provider: value,
          success: (res) => {
            uni.getUserInfo({
              provider: value,
              success: (infoRes) => {
                /**
                 * 实际开发中，获取用户信息后，需要将信息上报至服务端。
                 * 服务端可以用 userInfo.openId 作为用户的唯一标识新增或绑定用户信息。
                 */
                this.toMain(infoRes.userInfo.nickName);
              }
            });
          },
          fail: (err) => {
            console.error('授权登录失败：' + JSON.stringify(err));
          }
        });
      },
      toMain() { //去首屏页面
        /**
         * 强制登录时使用reLaunch方式跳转过来
         * 返回首页也使用reLaunch方式
         */
        if (this.vuex_forcedLogin) {
          uni.reLaunch({
            url: '/pages/home/index'
          })
        } else {
          uni.navigateBack()
        }
      }
    }
  }
</script>

<style>
  .content {
    margin-top: var(--status-bar-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .header {
    width: 161rpx;
    height: 161rpx;
    background: rgba(63, 205, 235, 1);
    box-shadow: 0rpx 12rpx 13rpx 0rpx rgba(63, 205, 235, 0.47);
    border-radius: 50%;
    margin-top: 30rpx;
    margin-left: auto;
    margin-right: auto;
  }

  .header image {
    width: 161rpx;
    height: 161rpx;
    border-radius: 50%;
  }

  .list {
    display: flex;
    flex-direction: column;
    padding-top: 50rpx;
    padding-left: 70rpx;
    padding-right: 70rpx;
  }

  .list-call {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    height: 100rpx;
    color: #333333;
    border-bottom: 1rpx solid rgba(230, 230, 230, 1);
  }

  .list-call .img {
    width: 40rpx;
    height: 40rpx;
  }

  .list-call .biaoti {
    flex: 1;
    text-align: left;
    font-size: 32rpx;
    line-height: 32rpx;
    margin-left: 16rpx;
  }

  .dlbutton {
    color: #FFFFFF;
    font-size: 34rpx;
    width: 470rpx;
    height: 100rpx;
    background: linear-gradient(-90deg, rgba(63, 205, 235, 1), rgba(188, 226, 158, 1));
    box-shadow: 0rpx 0rpx 13rpx 0rpx rgba(164, 217, 228, 0.2);
    border-radius: 50rpx;
    line-height: 100rpx;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
    margin-top: 100rpx;
  }

  .dlbutton-hover {
    background: linear-gradient(-90deg, rgba(63, 205, 235, 0.9), rgba(188, 226, 158, 0.9));
  }

  .xieyi {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    font-size: 30rpx;
    margin-top: 80rpx;
    color: #FFA800;
    text-align: center;
    height: 40rpx;
    line-height: 40rpx;
  }

  .xieyi text {
    font-size: 24rpx;
    margin-left: 15rpx;
    margin-right: 15rpx;
  }

  .oauth-row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
  }

  .oauth-image {
    width: 100rpx;
    height: 100rpx;
    border: 1rpx solid #dddddd;
    border-radius: 100rpx;
    margin: 0 40rpx;
    background-color: #ffffff;
  }

  .oauth-image image {
    width: 60rpx;
    height: 60rpx;
    margin: 20rpx;
  }
</style>
