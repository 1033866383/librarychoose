<template>
	<view style="text-align: center;">
		<my-custom bgColor="bg-gradual-blue" :isBack="true">
		  <block slot="backText">返回</block>
		  <block slot="content">扫码入场</block>
		</my-custom>
		
		<image src="../../../static/scan.png" style="width: 200px;height: 200px;margin-top: 10%;"></image>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
