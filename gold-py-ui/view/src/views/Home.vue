<template>
  <a-layout id="components-layout-demo-side" style="min-height: 100vh">
    <a-layout-sider v-model="collapsed" collapsible icon="arrow-left">
      <div class="home-logo">
        <span class="logo" />
        <span class="logo-text">{{ title }} </span>
      </div>
     
      <a-menu theme="dark" :default-selected-keys="['1001']" mode="inline">
        <a-menu-item key="1001" @click="$router.push('/mf/accountList')">
          <a-icon type="money-collect" />
          <span>蜜蜂帐号</span>
        </a-menu-item>
        <a-menu-item key="1002" @click="$message.info('功能开发中ヾ(◍°∇°◍)ﾉﾞ')">
          <a-icon type="bar-chart" />
          <span>利润报表</span>
        </a-menu-item>
        <a-menu-item key="1003" @click="$message.info('功能开发中ヾ(◍°∇°◍)ﾉﾞ')">
          <a-icon type="tags" />
          <span>帮助中心</span>
        </a-menu-item>
        <a-menu-item key="1004" @click="$message.info('功能开发中ヾ(◍°∇°◍)ﾉﾞ')">
          <a-icon type="heart" />
          <span>关于作者</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-content>
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
    <!-- 组件注册 -->
    <!-- 应用运行日志输出组件 -->
    <AppRuntimeLogDrawer ref="appRuntimeLogDrawer" />
  </a-layout>
</template>
<script>
import AppRuntimeLogDrawer from "@/components/AppRuntimeLogDrawer";
export default {
  components: {
    AppRuntimeLogDrawer,
  },
  data() {
    return {
      subject: "湘西-小金子",
      user: {
        clientName: "湘西-小金子",
       // userName: "云芝，是你吗",
      },
      collapsed: false,
      categorys: [],
      selectedCategoryId: "",
      level: 1,
    };
  },
  created() {},
  mounted() {},
  computed: {
    title: function () {
      if (!this.collapsed) {
        return this.subject;
      } else {
        return "";
      }
    },
    userTextClass: function () {
      if (!this.collapsed) {
        return "user-text";
      } else {
        return "user-text-hide";
      }
    },
  },
  methods: {
    // 查看日志
    showLogDrawer() {
      this.$refs.appRuntimeLogDrawer.showDrawer();
    }
  }
};
</script>

<style lang="scss" scope>
.home-logo {
  height: 48px;
  margin: 15px 16px 0px 16px;
  color: #ffe161;
  font: 200;
  font-size: 22px;
  overflow: hidden;

  .logo {
    display: inline-block;
    width: 48px;
    height: 48px;
    background: url(~@/assets/logo.png) no-repeat;
    background-size: 100%;
  }
  .logo-text {
    position: relative;
    top: -17px;
  }
}

.user-info {
  margin: 20px 0px 12px 18px;
  color: rgb(183, 197, 214);

  .user-logo {
    width: 54px;
    height: 54px;
    border-radius: 10px;
   // background: url(~@/assets/default_face.png) no-repeat;
    background-size: 100%;
    z-index: 1;
    margin-left: -5px;
  }
}

.user-text {
  display: inline;
  color: #add8f7;
  a {
    position: relative;
    top: -20px;
  }
}

.user-text-hide {
  display: none;
}
</style>
