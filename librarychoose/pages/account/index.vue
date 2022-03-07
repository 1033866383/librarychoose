<template>
	<view>
		<my-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">我的</block>
		</my-custom>
		我的
		<my-component-tabar />
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
