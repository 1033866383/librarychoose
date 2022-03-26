<template>
	<view>
		<my-custom bgColor="bg-gradual-blue" :isBack="true">
		  <block slot="backText">返回</block>
		  <block slot="content">支付成功</block>
		</my-custom>
		<view style="text-align: center; margin-top: 20%;">
			<image src="/static/paysuc.jpg" style="width: 100px;height: 100px;"></image>
			<button style="width: 80%;margin-top: 10%;" @click="go">继续</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			go(){
				uni.reLaunch({
					url: '/pages/home/index'
				});
			}
		}
	}
</script>

<style>

</style>
