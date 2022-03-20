<template>
	<view class="w-100">
		<view class="bg-f1 h-100vh">
			<view class="pt-f left-0 w-100 p-0-32 bg-white z1000" :style="'height: 132rpx;top:0'">
				<view>
					<view class="fz-34 fw-b pt-20">
						{{filmName}}
					</view>
					<view class="mt-10 fz-28 color-666">
						{{time}}
					</view>
				</view>
			</view>
			<movable-area :style="'height:'+(seatRow*40+350)+'rpx;width: 750rpx;top:'+(rpxNum*132)+'px'" class="pt-f left-0">
				<movable-view :style="'width: 750rpx;height:'+(seatRow*40+350)+'rpx;'" :inertia="true" :scale="true" :scale-min="0.95"
				 :scale-max="4" direction="all" @change="onMove" @scale="onScale">
					<view class="Stage dp-f jc-c ai-c fz-22 color-333">
						
					</view>
					<!-- <view class="pt-f pa-v-2 b-d-1" :style="'height:'+seatRow*(20+seatSize*pxNum)+'rpx;top:165rpx;width:0'"></view> -->
					<view v-for="(item,index) in seatArray" :key="index" class="dp-f jc-c" :style="'width:'+boxWidth+'px;height:'+seatSize+'px;margin-top:2rpx;'">
						<view v-for="(seat,col) in item" :key="col" class="dp-ib" :style="'width:'+seatSize+'px;height:'+seatSize+'px;margin-left:2rpx;'"
						 @click="handleChooseSeat(index,col)">
							<view  v-if="seat.status=='0'" class="w-100 h-100"></view> 
							<image v-if="seat.status=='1'" class="w-100 h-100" src="/static/unselected.png" mode="aspectFit"></image>
							<image v-else-if="seat.status=='4'" class="w-100 h-100" src="/static/selected.png" mode="aspectFit"></image>
							<image v-else-if="seat.status=='2' || seat.status=='3'" class="w-100 h-100" src="/static/bought.png" mode="aspectFit"></image>
						</view>
					</view>
					<view class="pt-f bg-line br-15 over-h" :style="'left: '+(10-moveX/scale)+'px;top:40rpx;width:30rpx;'">
						<view class="w-100 dp-f ai-c jc-c fz-22 color-fff" :style="'height:'+seatSize+'px;margin-top:2rpx;'" v-for="(m,mindex) in mArr"
						 :key="mindex">{{m}}</view>
						<view :style="'height: 20rpx;'"></view>
					</view>
				</movable-view>
			</movable-area>
			<view class="pt-f bottom-bar left-0 dp-f fd-cr z1000">
				<view class="bg-white p-all-32">
					<!-- <view class="dp-f ai-c jc-c fz-28 color-333 mb-20" v-if="SelectNum===0">
						推荐选座
						<view style="width: 106rpx;height: 60rpx;" class="b-1 br-5 dp-f ai-c jc-c fz-28 ml-20" v-for="(n,numindex) in 4"
						 :key="n" @click="smartChoose(numindex+1)">
							{{numindex+1}}人
						</view>
					</view> -->
					<view class="dp-f ai-c fw-w fz-28 color-333 mb-20" v-if="selectedSeat!=null">
						<text>已选</text>
						<view class="p-all-10 b-1 br-5 dp-f ai-c jc-c fz-28 ml-20">
							{{selectedRow+'排'+selectedSeat.num+'座'}}
						</view>
					</view>
					<view style="width: 686rpx;height: 90rpx;" class="dp-f jc-c ai-c br-10 fz-34 color-fff" :class="selectedSeat!=null?'bg-red-1':'bg-unbtn'"
					 @click="buySeat">
						{{selectedSeat!=null?('确认座位'):'请选座位'}}
					</view>
				</view>
				<view class="dp-f jc-c ai-c mb-20 fz-28" v-if="showTis">
					<view class="dp-f jc-c ai-c m-0-10">
						<image :style="'width:'+20+'px;height:'+20+'px'" src="/static/unselected.png" mode="aspectFit"></image><span
						 class="ml-10">可选</span>
					</view>
					<view class="dp-f jc-c ai-c m-0-10">
						<image :style="'width:'+20+'px;height:'+20+'px'" src="/static/bought.png" mode="aspectFit"></image><span
						 class="ml-10">不可选</span>
					</view>
					<view class="dp-f jc-c ai-c m-0-10">
						<image :style="'width:'+20+'px;height:'+20+'px'" src="/static/selected.png" mode="aspectFit"></image><span
						 class="ml-10">选中</span>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>
<script>
	/*
	 *特别声明：
	 * 该页面的逻辑及思路来自作者[houzisbw](https://github.com/houzisbw)的vue选座项目github地址[点击](https://github.com/houzisbw/MeiTuanCinemaSmartChoose)。
	 * 本人只针对uni-app做了样式及逻辑适配。
	 * 感谢原作者[houzisbw](https://github.com/houzisbw), 如有侵权, 请举报
	 * 
	 */
	// import {urlRequestWithUserId} from '../../js/http.js'
	import {
	  AllLibraryInfo
	} from '@/api/seat.js'
	export default {
		data() {
			return {
				filmName:'',
				time:'',
				detailId:'',
				scaleMin:1,//h5端为解决1无法缩小问题，设为0.95
				boxWidth: 400, //屏幕宽度px
				space: ' ', //空格
				seatArray: [], //影院座位的二维数组,0为非座位，1为未购座位，2或3为已购座位(红色),4为已选座位(绿色),一维行，二维列
				seatRow: 0, //影院座位行数
				seatCol: 0, //影院座位列数
				seatSize: 20, //座位尺寸
				moveX: 0, //水平移动偏移量
				scale: 1, //放大倍数
				minRow: 0, //从第几行开始排座位
				minCol: 0, //从第几列开始排座位
				showTis: true, //显示选座提示
				seatList: [], //接口获取的原始位置
				mArr: [], //左侧排数提示
				optArr: [], //选中的座位数组。
				isWXAPP:false,
				selectedSeat:null,//选中的座位
				selectedRow:0 //选中的行，跳过过道
			};
		},
		computed: {
			aPrice() {
				return this.SelectNum * 36
			},
			rpxNum() {
				return this.boxWidth / 750
			},
			pxNum() {
				return 750 / this.boxWidth
			},
		},
		onLoad: function(option)  {
			this.detailId = option.detailId
			//获取宽度
			var that = this
			uni.getSystemInfo({
				success: function(e) {
					that.boxWidth = e.screenWidth
					//#ifdef H5
					this.scaleMin = 0.95
					//#endif
				}
			})
			this.initData()
		},
		methods: {
			initData: function() {
				uni.showLoading({
					title:"正在加载座位"
				})
				var param = {
					film_detail_id:this.detailId
				}
				var that = this;
				urlRequestWithUserId("后台地址",param,"POST",function(res){
					that.filmName = res.data.film_name;
					that.time = res.data.film_date + "  " + res.data.film_start_time + " - " + res.data.film_end_time
					that.seatArray = res.data.filmSeat
					that.seatRow = that.seatArray.length;//行数量
					that.seatCol = that.seatArray[0].length;//列数量
					//设置座位大小
					that.seatSize = that.boxWidth > 0 ?
						parseInt(parseInt(that.boxWidth, 10) / (that.seatCol + 1), 10) :
						parseInt(parseInt(414, 10) / (that.seatCol + 1), 10)
					// console.log(that.seatArray)
					
					//左侧导航条
					let arr = that.seatArray.slice()
					let mArr = []
					var num = 1;
					for(let i in arr){
						var flag = false;
						for(let m in arr[i]){
							if(arr[i][m].num!=''){
								//一行里只要有num不是空的则需要显示序号
								flag = true;
							}
						}
						if(flag){
							mArr.push(num++)
						}else{
							mArr.push('')
						}
					}
					that.mArr = mArr
				})
				
				uni.hideLoading();
			},
			//放大缩小事件
			onScale: function(e) {
				this.showTis = false
				// this.moveX=-e.detail.x
				let w = this.boxWidth * 0.5
				let s = 1 - e.detail.scale
				this.moveX = w * s
				this.scale = e.detail.scale
				if (s > 0 || s === 0) {
					this.showTis = true
				}
			},
			//移动事件
			onMove: function(e) {
				this.showTis = false
				this.moveX = e.detail.x
			},
			//选定且购买座位
			buySeat: function() {
				uni.showLoading({
					title:"正在为您确认座位"
				})
				if (this.selectedSeat == null) {
					return
				}
				var param = {
					film_detail_id:this.detailId,
					row:this.selectedSeat.row,
					column:this.selectedSeat.column,
					seat:this.selectedRow + '排' + this.selectedSeat.num + '座'
				}
				urlRequestWithUserId("后台地址",param,"POST",function(res){
					uni.hideLoading();
					if(res.errorCode==200){
						uni.navigateTo({
							url:'./seatSuccess?order_id='+res.data.order_id+'&order_number=' + res.data.order_number + '&film_name='+res.data.film_name + '&film_time='+res.data.film_time + '&seat_number=' + res.data.seat_number
						})
					}
				})
			},
			//处理座位选择逻辑
			handleChooseSeat: function(row, col) {
				let seatStatus = this.seatArray[row][col].status;
				let newArray = this.seatArray;
				//如果是已购座位，直接返回
				if (seatStatus == '0' || seatStatus == '2' || seatStatus=='3') return
				//如果是已选座位点击后变未选
				if(seatStatus=='4'){
					newArray[row][col].status = '1'
					this.selectedSeat=null
					this.selectedRow = 0
				}else if (seatStatus == '1') {
					newArray[row][col].status = '4'
					//上一个选中的要置为未选中
					if(this.selectedSeat!=null){
						newArray[this.selectedSeat.row-1][this.selectedSeat.column-1].status = '1';
					}
					this.selectedSeat = newArray[row][col];
					//计算行，去掉过道
					let rowNum = 0;
					for(var i=0;i<=row;i++){
						var flag = false;//是否是座位标识
						for(var j=0;j<newArray[i].length;j++){
							if(newArray[i][j].num!=''){
								flag = true;//只要有座位，就置为true
							}
						}
						if(flag){
							++rowNum
						}
					}
					this.selectedRow = rowNum;
				}
				//必须整体更新二维数组，Vue无法检测到数组某一项更新,必须slice复制一个数组才行
				this.seatArray = newArray.slice();
			},
			//处理已选座位数组
			getOptArr: function(item, type) {
				// let optArr = this.optArr
				let optArr = [];
				if (type === 1) {
					optArr.push(item)
					this.
					//上一个选中的置为未选中
					this.selectedSeat = item;
				} else if (type === 0) {
					let arr = []
					optArr.forEach(v => {
						if (v.SeatCode !== item.SeatCode) {
							arr.push(v)
						}
					})
					optArr = arr
				}
				this.optArr = optArr.slice()
			},
			//推荐选座,参数是推荐座位数目，
			smartChoose: function(num) {
				console.log('num===', num)
				// 先重置
				this.resetSeat()
				//找到影院座位水平垂直中间位置的后一排
				let rowStart = parseInt((this.seatRow - 1) / 2, 10) + 1;
				//先从中间排往后排搜索
				let backResult = this.searchSeatByDirection(rowStart, this.seatRow - 1, num);
				if (backResult.length > 0) {
					this.chooseSeat(backResult);
					this.SelectNum += num
					return
				}
				//再从中间排往前排搜索
				let forwardResult = this.searchSeatByDirection(rowStart - 1, 0, num);
				if (forwardResult.length > 0) {
					this.chooseSeat(forwardResult);
					this.SelectNum += num
					return
				}
				//提示用户无合法位置可选
				alert('无合法位置可选!')
			
			},
			
			//搜索函数,参数:fromRow起始行，toRow终止行,num推荐座位数
			searchSeatByDirection: function(fromRow, toRow, num) {
				/*
				 * 推荐座位规则
				 * (1)初始状态从座位行数的一半处的后一排的中间开始向左右分别搜索，取离中间最近的，如果满足条件，
				 *    记录下该结果离座位中轴线的距离，后排搜索完成后取距离最小的那个结果座位最终结果，优先向后排进行搜索，
				 *    后排都没有才往前排搜，前排逻辑同上
				 *
				 * (2)只考虑并排且连续的座位，不能不在一排或者一排中间有分隔
				 *
				 * */

				/*
				 * 保存当前方向搜索结果的数组,元素是对象,result是结果数组，offset代表与中轴线的偏移距离
				 * {
				 *   result:Array([x,y])
				 *   offset:Number
				 * }
				 *
				 */
				let currentDirectionSearchResult = [];

				let largeRow = fromRow > toRow ? fromRow : toRow,
					smallRow = fromRow > toRow ? toRow : fromRow;

				for (let i = smallRow; i <= largeRow; i++) {
					//每一排的搜索,找出该排里中轴线最近的一组座位
					let tempRowResult = [],
						minDistanceToMidLine = Infinity;
					for (let j = 0; j <= this.seatCol - num; j++) {
						//如果有合法位置
						if (this.checkRowSeatContinusAndEmpty(i, j, j + num - 1)) {
							//计算该组位置距离中轴线的距离:该组位置的中间位置到中轴线的距离
							let resultMidPos = parseInt((j + num / 2), 10);
							let distance = Math.abs(parseInt(this.seatCol / 2) - resultMidPos);
							//如果距离较短则更新
							if (distance < minDistanceToMidLine) {
								minDistanceToMidLine = distance;
								//该行的最终结果
								tempRowResult = this.generateRowResult(i, j, j + num - 1)
							}
						}
					}
					//保存该行的最终结果
					currentDirectionSearchResult.push({
						result: tempRowResult,
						offset: minDistanceToMidLine
					})
				}

				//处理后排的搜索结果:找到距离中轴线最短的一个
				//注意这里的逻辑需要区分前后排，对于后排是从前往后，前排则是从后往前找
				let isBackDir = fromRow < toRow;
				let finalReuslt = [],
					minDistanceToMid = Infinity;
				if (isBackDir) {
					//后排情况,从前往后
					currentDirectionSearchResult.forEach((item) => {
						if (item.offset < minDistanceToMid) {
							finalReuslt = item.result;
							minDistanceToMid = item.offset;
						}
					});
				} else {
					//前排情况，从后往前找
					currentDirectionSearchResult.reverse().forEach((item) => {
						if (item.offset < minDistanceToMid) {
							finalReuslt = item.result;
							minDistanceToMid = item.offset;
						}
					})
				}

				//直接返回结果
				return finalReuslt
			},

			/*辅助函数，判断每一行座位从i列到j列是否全部空余且连续
			 *
			 */
			checkRowSeatContinusAndEmpty: function(rowNum, startPos, endPos) {
				let isValid = true;
				for (let i = startPos; i <= endPos; i++) {
					if (this.seatArray[rowNum][i].type !== 0) {
						isValid = false;
						break;
					}
				}
				return isValid
			},
			//辅助函数：返回每一行的某个合理位置的座位数组
			generateRowResult: function(row, startPos, endPos) {
				let result = [];
				for (let i = startPos; i <= endPos; i++) {
					result.push([row, i])
				}
				return result
			},
			//辅助函数:智能推荐的选座操作
			chooseSeat: function(result) {
				let opt = this.optArr
				let oldArray = this.seatArray.slice();
				for (let i = 0; i < result.length; i++) {
					//选定座位
					oldArray[result[i][0]][result[i][1]].type = 1
					this.optArr.push(oldArray[result[i][0]][result[i][1]])
				}
				this.seatArray = oldArray;
			},
		}
	}
</script>

<style lang="scss" scoped>
	.p-all-10{
		padding: 10rpx;
	}
	.ml-10 {
		margin-left: 10rpx;
	}

	.m-0-10 {
		margin: 0 10rpx;
	}

	.bg-unbtn {
		background-color: #f9abb3;
	}

	.bg-red-1 {
		background-color: #F45664;
	}

	.br-10 {
		border-radius: 10rpx;
	}

	.ml-20 {
		margin-left: 20rpx;
	}

	.mb-20 {
		margin-bottom: 20rpx;
	}

	.p-all-32 {
		padding: 32rpx;
	}

	.fd-cr {
		flex-direction: column-reverse;
		/* 主轴方向从下到上,默认从左到右 */
	}

	.bottom-bar {
		bottom: var(--window-bottom);
	}

	.color-fff {
		color: #fff
	}

	.br-15 {
		border-radius: 15rpx;
	}

	.over-h {
		overflow: hidden;
	}

	.dp-ib {
		display: inline-block;
	}

	.mt-20 {
		margin-top: 20rpx;
	}

	.pa-v-2 {
		/* 定位垂直对齐 */
		left: 50%;
		transform: translateX(-50%)
	}

	.b-d-1 {
		border: 1px dashed #e5e5e5;
	}

	.w-100 {
		width: 100%;
	}

	.h-100 {
		height: 100%;
	}

	.bg-f1 {
		background-color: #f1f1f1;
	}

	.h-100vh {
		height: 100vh;
	}

	.pt-f {
		position: fixed;
	}

	.left-0 {
		left: 0;
	}

	.p-0-32 {
		padding: 0 32rpx;
	}

	.pt-20 {
		padding-top: 20rpx;
	}

	.bg-white {
		background-color: #fff;
	}

	.z1000 {
		z-index: 1000;
	}

	.fz-34 {
		font-size: 34rpx;
	}

	.fw-b {
		font-weight: bold;
	}

	.mt-10 {
		margin-top: 10rpx;
	}

	.fz-28 {
		font-size: 28rpx;
	}

	.color-666 {
		color: #666666
	}

	.dp-f {
		display: flex;
	}

	.jc-c {
		justify-content: center;
	}

	.ai-c {
		align-items: center;
	}

	.fz-22 {
		font-size: 22rpx;
	}

	.color-333 {
		color: #333333
	}

	.m-0-a {
		margin: 0 auto;
	}

	.mt-48 {
		margin-top: 48rpx;
	}

	.fz-20 {
		font-size: 20rpx;
	}

	.color-999 {
		color: #999999
	}

	.b-1 {
		border: 1px solid #CCCCCC;
	}

	.br-5 {
		border-radius: 5rpx;
	}

	.Stage {
		background-color: #dddddd;
		width: 380rpx;
		height: 34rpx;
		transform: perspective(34rpx) rotateX(-10deg);
		margin: 0 auto;
	}

	.bg-line {
		background-color: rgba(0, 0, 0, 0.3);
	}

	.sel-seat {
		background: url('/static/selected.png') center center no-repeat;
		background-size: 100% 100%;
	}
	
	.unsel-seat {
		background: url('/static/unselected.png') center center no-repeat;
		background-size: 100% 100%;
	}
	
	.bought-seat {
		background: url('/static/bought.png') center center no-repeat;
		background-size: 100% 100%;
	}
</style>
