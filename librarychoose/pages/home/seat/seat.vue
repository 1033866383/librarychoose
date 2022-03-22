<template>
	<view>
			<view class="title">
				<view class="text-cut" style="text-align: center;">北大图书馆-作为选择</view>
			</view>
				<view style="text-align: center;">
						<view class="test">
							<button type="primary" @click="onShowDatePicker('rangetime')">选择占用时间</button>
							<view> 占用座位时间: {{ value[1]? value[0] + "--" + value[1] : ""}}</view>
						</view>
						<mx-date-picker :show="showPicker" :type="type" :value="value" :show-tips="true" :begin-text="'开始学习'" :end-text="'结束学习'" :show-seconds="true" @confirm="onSelected" @cancel="onSelected" />
						
					</view>
					<view>
					<view style="text-align: center;">
							<view v-for="(item,i) in [1,1,1,1,1,1,1,1,1,1]">
								<checkbox style="transform:scale(1)" :checked="true" v-for="(item,i) in [1,1,1,1,1,1,1,1,1,1]"/>
								<br/>
							</view>
					</view>
					</view>
						<button type="warn" class="footer">下一步</button>
				</view>
</template>

<script>
	import MxDatePicker from "@/components/mx-datepicker/mx-datepicker.vue";
		export default {
			components: {
				MxDatePicker
			},
			data() {
				return {
					showPicker: false,
					rangetime: ['2022/01/01 14:00','2022/01/01 14:59'],
					type: 'rangetime',
					value: ''
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
				}
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
