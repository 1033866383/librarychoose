<template>
  <view>
    <view class="cu-bar tabbar bg-white shadow foot">
      <view class="action" @click="NavChange" data-curbar="Home" data-cur="/pages/home/index">
        <view class='cuIcon-cu-image'>
          <image :src="'/static/tabbar/component' + [vuex_PageCur == 'Home'?'_cur':''] + '.png'"></image>
        </view>
        <view :class="vuex_PageCur=='Home'?'text-green':'text-gray'">首页</view>
      </view>
      <view class="action my-action" @click="NavChange" data-curbar="Account" data-cur="/pages/account/index">
        <view class='cuIcon-cu-image'>
          <image :src="'/static/tabbar/about' + [vuex_PageCur == 'Account'?'_cur':''] + '.png'"></image>
        </view>
        <view :class="vuex_PageCur=='Account'?'text-green':'text-gray'">我的</view>
      </view>
	  
    </view>
  </view>
</template>

<script>
  export default {
    components: {},
    mounted() {
      // 采用自定义tabbar，需首先隐藏原生tabbar。
      uni.hideTabBar()
    },
    data() {
      return {}
    },
    methods: {
      handlePageCur(pageCur) {
        this.$u.vuex('vuex_PageCur', pageCur)
      },
      NavChange: function(e) {
        this.handlePageCur(e.currentTarget.dataset.curbar)

        // tabar页面跳转需用switchTab方式，启用pages.json相关tabbar设置。
        uni.switchTab({
            url: e.currentTarget.dataset.cur
        });
      },
      navTo(e) {
        uni.navigateTo({
          url: e.currentTarget.dataset.cur
        })
      }
    }
  }
</script>

<style lang="scss" scoped>
  .my-action {
    height: 42px !important;

    .cuIcon-cu-image {
      height: 30px !important;
      padding-top: 3px;

      .cuIcon-edit {
        font-size: 22px;
        margin-bottom: 0px;
      }
    }
  }

  .my-add-action {
    padding-top: 4px;
  }
</style>
