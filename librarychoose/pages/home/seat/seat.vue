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
											<image src="/static/unselected.png" style="width: 26px;height: 26px;" v-if="allseat[l][r] !== -1"></image>
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
							<button type="warn" class="footer" style="text-align: center; width: 95%;">下一步</button>
						</view>
						
				</view>
</template>

<script>
	import MxDatePicker from "@/components/mx-datepicker/mx-datepicker.vue";
	import {
	  AllSeatInfo
	} from '@/api/seat.js'
		export default {
			components: {
				MxDatePicker
			},
			data() {
				return {
					library:uni.getStorageSync("library").name,
					left:[],
					right:[],
					allseat:[[]],
					checkva:"0",
					checkc:false,
					rangetime: ['2022/01/01 14:00','2022/01/01 14:59'],
					type: 'rangetime',
					value: '',
					showPicker: false
				}
			},
			methods: {
				onShowDatePicker(type){//显示
					this.type = type;
					this.showPicker = true;
					this.value = this[type];
				},
				onSelected(e) {//选择
					this.showPicker = false;
					if(e) {
						this[this.type] = e.value; 
						//选择的值
						console.log('value => '+ e.value);
						//原始的Date对象
						console.log('date => ' + e.date);
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
