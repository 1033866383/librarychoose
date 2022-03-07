<template>
	<view class="pages">
    <my-custom bgColor="bg-gradual-blue" :isBack="false">
    	<block slot="content">首页</block>
    </my-custom>
    <view class="content">
     Home
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
      if (!this.vuex_hasLogin) {
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
