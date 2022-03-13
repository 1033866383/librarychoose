<template>
	<view class="pages">
    <my-custom bgColor="bg-gradual-blue" :isBack="false">
    	<block slot="content">共享自习室</block>
    </my-custom>
    <view class="content">
					<view class="flex solid-bottom padding align-start">
						 <image v-if="showpicture" class="img" src="/static/img/zxs.jpg" style="width: 100%; height: 150px; border-radius: 1%;"></image>
						 <image v-if="!showpicture" class="img" src="/static/img/zxs.png" style="width: 100%; height: 150px; border-radius: 1%;"></image>					
					</view>
					<view class="cu-bar bg-white  margin-top solid-bottom">
									<view class="action">
										<text class="cuIcon-title text-blue"></text>每一天都学有所成。
									</view>
								</view>
								<view class="bg-white">
									<view class="flex solid-bottom padding align-start" >
											<button class="cu-btn" style="width: 48%; height: 100px; background-color: #78E343;font-size:25px;color: #FFFFFF;margin-right: 1%;">自习室</button>
											<button class="cu-btn" style="width: 48%; height: 100px;background-color: #EBDC30;font-size:25px;color: #FFFFFF;margin-left: 1%;">订单</button>										
									</view>
								
									<view class="cu-card article" >
												<view class="cu-item shadow" v-for="(item,i) in ['1','2','3']">
													<view class="title"><view class="text-cut">图书馆名称</view></view>
													<view class="content">
														<image src="/static/img/zxs.jpg"></image>
														<view class="desc">
															<view class="text-content"> 位置：</view>
															<view>
																<view class="cu-tag bg-red light sm round">最大容纳人数：10</view>
																<br/>
																<view class="cu-tag bg-green light sm round">营业时间：1:00-24:00</view>
															</view>
														</view>
													</view>
												</view>
			
											</view>
											<br/><br/>
								</view>
    </view>
		<my-component-tabar />
	</view>
</template>

<script>
	export default {
		data() {
			return {
				showpicture:true
			}
		},
    mounted() {
      if (uni.getStorageSync("lifeData") === null || uni.getStorageSync("lifeData") === undefined || uni.getStorageSync("lifeData") === "") {
        this.$u.route('/pages/login/login/index')
      }
	  this.showpicture = ((Math.floor(Math.random() * 10) + 1 % 2) === 2)
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
