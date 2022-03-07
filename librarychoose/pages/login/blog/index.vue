<template>
  <view>
    <my-custom bgColor="bg-gradual-blue" :isBack="true">
      <block slot="backText">返回</block>
      <block slot="content">软件用户协议</block>
    </my-custom>
    <web-view :webview-styles="webviewStyles" :src="articleurl"></web-view>
  </view>
</template>

<script>
  export default {
    data() {
      return {
        articleurl: '',
        webviewStyles: {
          progress: {
            color: '#FF7200'
          }
        }
      };
    },
    onLoad(options) {
      this.articleurl = 'http://www.baidu.com/';
    }
  }
</script>

<style>

</style>
