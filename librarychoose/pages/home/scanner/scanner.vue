<template>
	<view style="text-align: center;">
		<my-custom bgColor="bg-gradual-blue" :isBack="true">
		  <block slot="backText">返回</block>
		  <block slot="content">扫码入场</block>
		</my-custom>
		
		<image src="../../../static/scan.png" style="width: 200px;height: 200px;margin-top: 10%;"></image>
		<view style="margin-top: 10%;" @click="cancelgood">
			<button type="warn">取消订单</button>
		</view>
	</view>
</template>

<script>
	import {
	  CancelGoods
	} from '@/api/goods.js'
	
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			cancelgood(){
				  uni.showModal({
				          title: '提示信息',
				          content: '是否取消该订单？取消订单会对您的积分进行扣除,积分异常将无法再次预约座位',
				          cancelText: "否",
				          confirmText: "是",
				          confirmColor: '#F2C827',
				          cancelColor: '#9E9E9E',
				          success: function () {
							  CancelGoods(uni.getStorageSync("goods")).then(res=>{
								  if(res.msg !== "success"){
									uni.showToast({
									    title: res.msg,
									    duration: 2000,
										icon:"error"
									});
								  }else{
									uni.showToast({
									    title: res.msg,
									    duration: 2000
									});
									uni.reLaunch({
										url: '/pages/home/index'
									});
								  }
							  })
				          }
				        });
			}
		}
	}
</script>

<style>

</style>
