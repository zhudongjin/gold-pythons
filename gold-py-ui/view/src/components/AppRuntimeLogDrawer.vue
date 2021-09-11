<template>
  <div>
    <a-drawer
      placement="right"
      :width="640"
      :visible="visible"
      @close="onClose"
    >
      <div slot="title"><a-icon type="file-text" /> App运行日志输出</div>
      <div class="log-container">
        <p v-for="(item, i) in logList" :key="i">{{ item }}</p>
      </div>
      <a-button
        v-show="logList.length > 0"
        class="btn-clear"
        type="primary"
        icon="rocket"
        @click="clearLog"
      >
        清空
      </a-button>
    </a-drawer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
      logList: [],
    };
  },
  mounted() {
    // 注册接收日志
    window.receiveAppLog = this.receiveAppLog;
  },
  destroyed() {
    delete window["receiveAppLog"];
  },
  methods: {
    showDrawer() {
      this.visible = true;
    },
    onClose() {
      this.visible = false;
    },
    // app运行日志接收
    receiveAppLog(logMessage) {
      this.logList.push(logMessage);
      this.$nextTick(() => {
        let logContainer = document.querySelector(".log-container");
        logContainer.scrollTop = logContainer.scrollHeight;
      });
    },
    // 清理日志
    clearLog() {
      this.logList = [];
    },
  },
};
</script>
<style lang="scss" scoped>
/deep/ .ant-drawer-body {
  height: calc(100% - 55px);
  padding: 0px;
}
.log-container {
  height: 100%;
  background-color: #000;
  color: #ef0205;
  padding: 15px;
  font-size: 12px;
  line-height: 16px;
  font-family: "Courier New", Courier, monospace;
  overflow-y: auto;
  p {
    margin-bottom: 0.3em;
  }
}
.btn-clear {
  position: fixed;
  bottom: 10px;
  right: 10px;
}
</style>