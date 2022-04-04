<template>
	<view class="pages">
    <my-custom bgColor="bg-gradual-blue" :isBack="false">
    	<block slot="content">共享自习室</block>
    </my-custom>
    <view class="content">
					<view class="flex solid-bottom padding align-start">
						 <image v-if="showpicture" class="img" src="/static/img/zxs.jpg" style="width: 100%; height: 150px; border-radius: 1%;" ></image>
						 <image v-if="!showpicture" class="img" src="/static/img/zxs.png" style="width: 100%; height: 150px; border-radius: 1%;" ></image>					
					</view>
					<view class="cu-bar bg-white  margin-top solid-bottom">
									<view class="action">
										<text class="cuIcon-title text-blue"></text>每一天都学有所成。
									</view>
								</view>
								<view class="bg-white">
									<view class="flex solid-bottom padding align-start" >
											<button class="cu-btn" style="width: 48%; height: 100px; background-color: #78E343;font-size:25px;color: #FFFFFF;margin-right: 1%;" @click="change('library')">自习室</button>
											<button class="cu-btn" style="width: 48%; height: 100px;background-color: #EBDC30;font-size:25px;color: #FFFFFF;margin-left: 1%;" @click="change('goods')">订单</button>										
									</view>
								
									<view class="cu-card article" >
												<view v-show="showlist === 'library'" class="cu-item shadow" v-for="(item,i) in alllibrary" @click="goseat(item)">
													<view class="title"><view class="text-cut">{{item.name}}</view></view>
													<view class="content" >
														<image src="/static/img/zxs.jpg" v-if="i % 2 === 0"></image>
														<image src="/static/img/1.jpg" v-if="i % 2 === 1"></image>
														<image src="/static/img/2.jpg" v-if="i % 2 === 4"></image>
														<image src="/static/img/3.jpg" v-if="i % 2 === 3"></image>
														<view class="desc">
															<view class="text-content"> 位置：{{item.position}}</view>
															<view>
																<view class="cu-tag bg-red light sm round">最大容纳人数：{{item.max_seat}}</view>
																<br/>
																<view class="cu-tag bg-green light sm round">营业时间：1:00-24:00</view>
															</view>
														</view>
													</view>
												</view>
												
												<view v-show="showlist === 'goods'" class="cu-item shadow" v-for="(item,i) in allgoods" @click="goscan(item)">
													<view class="title"><view class="text-cut">订单号：{{item.id}}</view></view>
													<view class="content" >
														

														
														<image src="/static/img/zxs.jpg" v-if="i % 2 === 0"></image>
														<image src="/static/img/1.jpg" v-if="i % 2 === 1"></image>
														<image src="/static/img/2.jpg" v-if="i % 2 === 4"></image>
														<image src="/static/img/3.jpg" v-if="i % 2 === 3"></image>
														<view class="desc">
															<view class="cu-tag bg-red light sm round">点击生成二维码,扫码入场</view>
															
															<view class="text-content"> 我的座位：{{item.library.name +":"+item.position.left+"排"+item.position.right+"列"}}</view>
															<view>
																<view class="cu-tag bg-green light sm round">开始时间：{{item.start_time}}</view>
																<br/>
																<view class="cu-tag bg-green light sm round">结束时间：{{item.end_time}}</view>
																
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
	import {
	  AllLibraryInfo
	} from '@/api/seat.js'
	import {
		AllGoodsInfo
	} from '@/api/goods.js'
	
	export default {
		data() {
			return {
				showlist:'library',
				showpicture:true,
				alllibrary:[],
				allgoods:[],
			}
		},
    methods: {
		goscan(item){
			uni.setStorageSync("goods", item.id)
			this.$u.route('/pages/home/scanner/scanner')
		},
		change(ty){
			this.showlist = ty
			console.log(this.showlist)
		},
		goseat(item){
			uni.setStorageSync("library", item)
			this.$u.route('/pages/home/seat/seat')
		},
      navTo(url,params) {
        if (url) {
          this.$u.route(url, params)
        }
      },
	  libraryinfo(){
		  AllLibraryInfo().then(res=>{
				this.alllibrary = res.data
		  })
	  },
	  goodsinfo(){
		  AllGoodsInfo().then(res=>{
			  this.allgoods = res.data
		  })
		  
	  }
    },
	created() {
	  if (uni.getStorageSync("lifeData") === null || uni.getStorageSync("lifeData") === undefined || uni.getStorageSync("lifeData") === "") {
	    this.$u.route('/pages/login/login/index')
	  }
	  this.showpicture = ((Math.floor(Math.random() * 10) + 1 % 2) === 2)
	  this.libraryinfo()
	  this.goodsinfo()
	},
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
