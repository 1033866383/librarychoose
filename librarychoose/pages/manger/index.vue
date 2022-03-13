<template>
	<view class="pages">
    <my-custom bgColor="bg-gradual-blue" :isBack="false">
    	<block slot="content">共享自习室</block>
    </my-custom>
    <view class="content">
     manger
    </view>
		<my-component-tabar />
	</view>
</template>

<script>
	export default {
		data() {
			return {}
		},
    mounted() {
      if (uni.getStorageSync("lifeData") === null || uni.getStorageSync("lifeData") === undefined || uni.getStorageSync("lifeData") === "") {
        this.$u.route('/pages/login/login/index')
      }
    },
    methods: {
      navTo(url,params) {
        if (url) {
          this.$u.route(url, params)
        }
      }
    }
	}
</script>

<style lang="scss" scoped>
  .pages {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
</style>
