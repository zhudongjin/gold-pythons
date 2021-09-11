<template>
  <div>
    <a-page-header
      class="components-page-header"
      title="蜜蜂帐号"
      sub-title="支付宝能开3个号，每天1000毛轻松到手"
      :backIcon="false"
      @back="() => null"
    >
    </a-page-header>
    <a-layout class="components-page-content">
      <a-layout-content>
        <div class="table-operations">
          <a-button type="primary" icon="redo" @click="refreshDataList">
            列表刷新
          </a-button>
          <a-button type="primary" icon="upload" @click="drawOutToAlipay">
            提现到支付宝
          </a-button>
          <div style="float: right">
            <a-button icon="plus" @click="toAddAccount">
              添加蜜蜂账号
            </a-button>
          </div>
        </div>
        <a-table
          :columns="columns"
          :data-source="dataList"
          :rowKey="(record, index) => index"
          :pagination="false"
          :loading="dataListLoading"
        >
          <span slot="customUserName"><a-icon type="mobile" /> 用户名</span>
          <span slot="customCnName"
            ><a-icon type="credit-card" /> 实名信息</span
          >
          <span slot="customDrawOutAmt"
            ><a-icon type="pay-circle" /> 可提现金额(元)</span
          >
          <span slot="drawOutAmt" slot-scope="text">{{
            Number(text).toFixed(2)
          }}</span>
          <span slot="customRefreshTime"
            ><a-icon type="history" /> 上次刷新时间</span
          >
          <span slot="customDrawOutTime"
            ><a-icon type="history" /> 上次提现时间</span
          >
          <template slot="operation" slot-scope="text, record, index">
            <a-popconfirm
              :title="`确定删除吗？`"
              @confirm="() => delAccount(index)"
            >
              <a-button type="danger" shape="circle" icon="delete" />
            </a-popconfirm>
          </template>
        </a-table>
      </a-layout-content>
    </a-layout>
    <!-- 组件注册 -->
    <!-- 添加账号组件 -->
    <AddAccountModal ref="addAccountModal" @complate="complateAddAccount" />
  </div>
</template>
<script>
import AddAccountModal from "./modules/AddAccountModal";
const columns = [
  {
    dataIndex: "userName",
    key: "userName",
    slots: { title: "customUserName" },
  },
  {
    dataIndex: "cnName",
    key: "cnName",
    slots: { title: "customCnName" },
  },
  {
    dataIndex: "drawOutAmt",
    key: "drawOutAmt",
    slots: { title: "customDrawOutAmt" },
    scopedSlots: { customRender: "drawOutAmt" },
  },
  {
    key: "refreshTime",
    dataIndex: "refreshTime",
    slots: { title: "customRefreshTime" },
  },
  {
    title: "今日成功单数",
    key: "orderCount",
    dataIndex: "orderCount",
  },
  {
    key: "drawOutTime",
    dataIndex: "drawOutTime",
    slots: { title: "customDrawOutTime" },
  },
  {
    title: "操作",
    key: "operation",
    width: 100,
    scopedSlots: { customRender: "operation" },
  },
];

export default {
  components: {
    AddAccountModal,
  },
  data() {
    return {
      dataList: [],
      columns,
      timeInterval: null,
      dataListLoading: true,
      loadingHide: null,
      fetchReqCount: 0,
    };
  },
  mounted() {
    this.getDataList(true);
  },
  destroyed() {
    this.timeInterval = null;
  },
  methods: {
    // 加载列表数据
    getDataList(isLoading = false) {
      if (isLoading) {
        this.dataListLoading = true;
      }
      this.$http.post("/mf/get_account_list").then((res) => {
        this.dataListLoading = false;
        if (res.code === "0000") {
          this.dataList = res.data;
          this.dataList = this.dataList.map((item) => {
            Object.keys(item).forEach((key) => {
              if (!item[key] && item[key] !== 0) {
                item[key] = "--";
              }
            });
            return item;
          });
        } else {
          this.$message.warning(res.msg);
        }
      });
    },
    // 列表刷新
    refreshDataList() {
      if (this.canExecBatchTask()) {
        return;
      }
      this.$http.post("/mf/mf_reload_acct").then((res) => {
        if (res.code === "0000") {
        alert(res.date);
          this.showLoadingMessage("爬虫任务处理中，预计耗时1分钟...");
          this.fetchSpiderState();
        }
      });
    },
    // 显示加载消息（刷新列表/提现触发）
    showLoadingMessage(message) {
      this.loadingHide = this.$message.loading(message, 0);
    },
    // 提现至支付宝
    drawOutToAlipay() {
      if (this.canExecBatchTask()) {
        return;
      }
      this.$http.post("/mf/mf_reload_acct").then((res) => {
        if (res.code === "0000") {
          this.showLoadingMessage("提现任务处理中，预计耗时1分钟...");
          this.fetchSpiderState();
        }
      });
    },
    // 判断能否执行批次任务
    canExecBatchTask() {
      if (this.timeInterval) {
        this.$message.warning("已有批次任务在处理，请稍候发起");
        return true;
      }
      return false;
    },
    // 获取爬取状态
    fetchSpiderState() {
      if (this.timeInterval) {
        return;
      }
      this.fetchReqCount = 0;
      this.timeInterval = setInterval(() => {
        this.$http.post("/mf/get_fetch_state").then((res) => {
          this.fetchReqCount = this.fetchReqCount + 1;
          if (this.fetchReqCount > 200) {
            this.$message.warning("执行任务出了点小意外，请手动重试");
            this.stopFetchSpider();
            return;
          }
          if (res.code === "0000" && res.data === "complate") {
            this.$message.success("列表刷新或批量提现任务已完成");
            this.stopFetchSpider();
          }
        });
      }, 2500);
    },
    // 停止间隔调度
    stopFetchSpider() {
      this.getDataList(true);
      this.loadingHide();
      clearInterval(this.timeInterval);
      this.timeInterval = null;
    },
    // 触发添加蜜蜂账号弹窗
    toAddAccount() {
      this.$refs.addAccountModal.showModal();
    },
    // 提交添加蜜蜂账号
    complateAddAccount() {
      this.getDataList(true);
    },
    // 删除账号
    delAccount(index) {
      this.$http.post("/mf/delete_account", { index: index }).then((res) => {
        if (res.code === "0000") {
          this.$message.success("删除账号成功");
          this.getDataList(true);
        } else {
          this.$message.warning(res.msg);
        }
      });
    },
  },
};
</script>

<style lang="scss" scope>
.components-page-header {
  border: 1px solid rgb(235, 237, 240);
  background-color: #fff;
}
.components-page-content {
  padding: 20px;
  background-color: #fff;
}
.table-operations {
  margin-bottom: 16px;
  button {
    margin-right: 8px;
  }
}
</style>
