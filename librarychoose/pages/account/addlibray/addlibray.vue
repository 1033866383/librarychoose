<template>
	<view>
		<my-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="backText">返回</block>
			<block slot="content">支付成功</block>
		</my-custom>
		
		 <form style="text-align: center;margin: 10px;">
		
		
				<view class="uni-form-item uni-column">
						<view class="title" style="font-size: 20px;">图书馆名称：</view>
						<input class="uni-input" v-model="form.name" focus placeholder="请输入图书馆名称" />
					</view>
					
				<view class="uni-form-item uni-column">
								<view class="title" style="font-size: 20px;">图书馆位置：</view>
								<input class="uni-input" v-model="form.position" focus placeholder="请输入图书馆位置" />
							</view>
							
				<view class="uni-form-item uni-column">
								<view class="title" style="font-size: 20px;">图书馆最大可容纳人数：</view>
								<input class="uni-input" v-model="form.max_seat" type="number" placeholder="请输入图书馆最大可容纳人数" />
							</view>
		 		<view class="uni-btn-v">
		 					<button @click="add">提交</button>
				</view>
				<view class="uni-btn-v">
							<button @click="goback">返回</button>
				</view>
		</form>
	</view>
</template>

<script>
	import {
	  AddLibrary
	} from '@/api/seat.js'
	export default {
		data() {
			return {
				form:{
					name:"",
					max_seat:"",
					position:""
				}
			}
		},
		methods: {
			goback(){
				uni.reLaunch({
					url: '/pages/account/index'
				});
			},
			add(){
				AddLibrary(this.form).then(x=>{
					if(x.msg !== "success"){
						uni.showToast({
						    title: x.msg,
						    duration: 2000,
							icon:"error"
						});
					}else{
						uni.showToast({
						    title: x.msg,
						    duration: 2000
						});
						this.form.name = ""
						this.form.position = ""
						this.form.max_seat = ""
					}
				})
			}
		}
	}
</script>

<style>
	.uni-form-item .title {
		padding: 20rpx 0;
	}
</style>
