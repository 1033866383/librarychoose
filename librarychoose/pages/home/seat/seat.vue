<template>
	<view>
		<my-custom bgColor="bg-gradual-blue" :isBack="true">
		  <block slot="backText">返回</block>
		  <block slot="content">座位选择</block>
		</my-custom>
			<view class="title">
				<view class="text-cut" style="text-align: center;font-size: 20px;font-weight:bold;">{{library}}</view>
			</view>
				<view style="text-align: center;">
						<view class="test">
							<button type="primary" @click="onShowDatePicker('rangetime')">选择占用时间</button>
							<view> 占用座位时间: {{ value[1]? value[0] + "--" + value[1] : ""}}</view>
						</view>
						<mx-date-picker :show="showPicker" :type="type" :value="value" :show-tips="true" :begin-text="'开始学习'" :end-text="'结束学习'" :show-seconds="true" @confirm="onSelected" @cancel="onSelected" />
					</view>
					<view>
					</view>
					<view>
						<scroll-view scroll-y="true"  style="height: 348px;">
							<view style="text-align: center;">
									<view v-for="(item,l) in left">							
									<span style="float: left;">
									</span>
										<span value ='0' :checked="true" v-for="(item,r) in right">
											<image src="/static/unselected.png" style="width: 26px;height: 26px;" v-if="allseat[l][r] !== -1" @click="chooseseat(l, r)" v-show="(JSON.stringify(targetseat) !== JSON.stringify([l, r])) && (usingseat.indexOf(allseat[l][r]) === -1)"></image>
											<image src="/static/selected.png" style="width: 26px;height: 26px;" v-if="allseat[l][r] !== -1" @click="chooseseat(l, r)" v-show="(JSON.stringify(targetseat) === JSON.stringify([l, r])) && (usingseat.indexOf(allseat[l][r]) === -1)"></image>
											<image src="/static/bought.png" style="width: 26px;height: 26px;" v-if="allseat[l][r] !== -1" v-show="usingseat.indexOf(allseat[l][r]) !== -1"></image>
										</span>
									<br/>
	
								</view>
							</view>
							
						</scroll-view>
			<!-- 			<br/> -->
						<view style="text-align: center;">
								<span>可选<image src="/static/unselected.png" style="width: 26px;height: 26px;"></image></span>
								<span>选择<image src="/static/selected.png" style="width: 26px;height: 26px;"></image></span>
								<span>不可选<image src="/static/bought.png" style="width: 26px;height: 26px;"></image></span>
								
						</view>
							
						</view>
						<view>
							<button type="warn" class="footer" style="text-align: center; width: 95%;" @click="generprice">下一步</button>
						</view>
						
				</view>
</template>

<script>
	import MxDatePicker from "@/components/mx-datepicker/mx-datepicker.vue";
	import {
	  AllSeatInfo
	} from '@/api/seat.js'
	import{
		GenerPrice,
		AddGoods,
		UsingSeat
	}from '@/api/goods.js'
		export default {
			components: {
				MxDatePicker
			},
			data() {
				return {
					targetseat:[],
					library:uni.getStorageSync("library").name,
					left:[],
					right:[],
					allseat:[[]],
					checkva:"0",
					checkc:false,
					rangetime: ['2022/04/01 14:00:00','2022/04/01 15:00:00'],
					type: 'rangetime',
					value: '',
					showPicker: false,
					usingseat:[]
				}
			},
			methods: {
				generprice(){
					if(!this.value){
						uni.showToast({
						    title: "未择占用时间",
						    duration: 2000,
							icon:"error"
						});
						return
					}
					if(this.targetseat.length !== 2){
						uni.showToast({
						    title: "未选择座位",
						    duration: 2000,
							icon:"error"
						});
						return
					}
					var data = {seat:this.allseat[this.targetseat[0]][this.targetseat[1]], start_time: this.value[0].replace("/", "-").replace("/", "-").replace("/", "-"), end_time: this.value[1].replace("/", "-").replace("/", "-").replace("/", "-")}
					GenerPrice(data).then(res=>{
						console.log(res)
						if(res.msg !== 'success'){
								uni.showToast({
								    title: res.msg,
								    duration: 2000,
									icon:"error"
								});
						}else{
							uni.showModal({
							    title: '支付提示',
							    content: '您选择了' + this.library +"第" + (this.targetseat[1] + 1)+"列第" + (this.targetseat[0] + 1) + "排的座位，占用时间："+this.value[0] +"--" + this.value[1] + "  需要支付" + res.data + "元",
							    confirmText: "确认支付",
								success: function (res) {
							        if (res.confirm) {
							            console.log('用户点击确定');
										AddGoods(data).then(res=>{
											console.log(res)
											if(res.msg !== 'success'){
													uni.showToast({
													    title: res.msg,
													    duration: 2000,
														icon:"error"
													});
											}else{
												uni.redirectTo({
													url: '/pages/home/seat/paysuc/paysuc'
												});
											}
										}).then(
										UsingSeat(data.start_time, data.end_time).then(res=>{
											this.usingseat = res.data
										})
										)
							        } else if (res.cancel) {
							            console.log('用户点击取消');
							        }
							    }
							});
		
						}
					})
				},
				chooseseat(l, r){
					if(this.value.length !== 2){
						uni.showToast({
							    title: "请先选择占用时间",
							    duration: 2000,
								icon:"error"
							});
							return
						
					}
					if(JSON.stringify(this.targetseat) === JSON.stringify([l, r])){
						this.targetseat = []
					}else{
						this.targetseat = [l,r]
					}
					console.log(JSON.stringify(this.targetseat) === JSON.stringify([l, r]))
				},
				onShowDatePicker(type){//显示
					this.type = type;
					this.showPicker = true;
					this.value = this[type];
					UsingSeat(this.value[0].replace("/", "-").replace("/", "-").replace("/", "-"), this.value[1].replace("/", "-").replace("/", "-").replace("/", "-")).then(res=>{
						this.usingseat = res.data
					})
				},
				onSelected(e) {//选择
					this.showPicker = false;
					if(e) {
						this[this.type] = e.value; 
						this.value = e.value
						//选择的值
						console.log('value => '+ e.value);
						//原始的Date对象
						console.log('date => ' + e.date);
						UsingSeat(this.value[0].replace("/", "-").replace("/", "-").replace("/", "-"), this.value[1].replace("/", "-").replace("/", "-").replace("/", "-")).then(res=>{
							this.usingseat = res.data
						})
						console.log(this.usingseat)
					}
				},
				getseatinfo(){
				
					AllSeatInfo(null, uni.getStorageSync("library").id).then(res=>{
					let left = new Set()
					let right = new Set()
					let datas = null
					let allset = []
						res.data.forEach(x=>{
							left.add(x.position.left)
							right.add(x.position.right)
						})
							let l = Array.from(left)
							let r = Array.from(right)
				
							datas = res.data
							for(let i = 0; i<=l.length; i++){
								let rowset = []
								for(let k = 0; k <= r.length; k++){
									rowset.push(-1)
								}
								allset.push(rowset)
							}
							datas.forEach(t=>{
								allset[t.position.left][t.position.right] = t.id
							})
							this.left = l
							this.right = r
							this.allseat = allset
					})
				}
			},
			mounted() {
				this.getseatinfo()
			}
		}
	</script>
<style>
.test{
		text-align: center;
		padding: 10px 0;
	}
button{
	margin: 20upx;
	font-size: 28upx;
}
.footer{
	width:100%;
	position:fixed;
	bottom:0;
}
  
</style>
