
<template>
	<view class="content">
		
		<view class="userback">
			<img src="/static/icon.png">
			<view style="font-size: 30px;">
				{{user.name}}
			</view>
		</view>
		<view class="cu-list menu-avatar">			
			<view class="cu-item">								
				<view class="content">软件版本</view>												
				<view class="action">1.0.0</view>															
			</view>
			<view class="cu-item">
				<view class="content">软件版本</view>												
				<view class="action">1.0.0</view>															
			</view>			
			<view class="cu-item">
				<view class="content">个人积分: {{user.info.credit >= 51 ? user.info.credit + "(正常)" : user.info.credit + "(异常)"}}</view>																									 
			</view>
			<view class="cu-item"v-if="user.role === 1">
				
				<view class="content" @click="goaddlib">添加自习室</view>																									 
			</view>
		</view>		
		<my-component-tabar />
		<view class="btn-row">
					<button  type="default" style="color: #111111" @click="logout" >退出登录</button>
		</view>
	</view>
</template>
<script>
	import {
	  UserInfo
	} from '@/api/login.js'
	export default {
		data() {
			return {
				user:uni.getStorageSync("lifeData")
			}
		},
		methods:{
			logout(){
				uni.clearStorage()
				this.$u.route('/pages/login/login/index')
			},
			goaddlib(){
				// this.$u.route('/pages/login/login/index')
				uni.reLaunch({
					url: '/pages/account/addlibray/addlibray'
				});
			}
		},
		created() {
			UserInfo().then(x=>{
				let da = uni.getStorageSync("lifeData")
				da.info.credit = x.data.info.credit
				uni.setStorageSync("lifeData", da)
			})
		},
	}
</script>
<style>
	.userback {
		height: 216px;
		/* background-image: url('../../static/img/userback.png'); */
		background-repeat: no-repeat;
		background-size: 100%;
		text-align: center
	}

	.userback img {
		margin: auto;
		border-radius: 51px;
		margin-top: 21%;
		width: 97px;
		height: 97px;
	}
	.userName{
		color: #111111;
		font-size: 0.9rem;
	}
	.userOrgan{		
	}	
	uni-button[type=primary] {
	    margin: 0 4%;
	    background-image: linear-gradient(to top, #66b7f9,#1c82d4);
	}
	.cu-list.menu-avatar>.cu-item {	   
	    height: 37px;
	    background: none;
	}
	.cu-list.menu-avatar>.cu-item .content {	   
	    left: 18px;	    
	}
	.cu-list.menu-avatar>.cu-item .action {
	    width: 42px;	  
	}
	.cu-list.menu-avatar {	   
	    height: 195px;
	}
</style>

