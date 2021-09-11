<template>
  <div>
    <a-modal
      title="添加蜜蜂账号"
      :maskClosable="false"
      :visible="visible"
      :confirm-loading="confirmLoading"
      @ok="formSubmit"
      @cancel="visible = false"
    >
      <a-form ref="submitForm" :form="form">
        <a-form-item label="用户名">
          <a-input
            size="large"
            type="text"
            placeholder="请输入用户名"
            v-decorator="[
              'userName',
              {
                rules: [{ required: true, message: '请输入用户名' }],
                validateTrigger: 'change',
              },
            ]"
          >
            <a-icon
              slot="prefix"
              type="user"
              :style="{ color: 'rgba(0,0,0,.25)' }"
            />
          </a-input>
        </a-form-item>
        <a-form-item label="登录密码">
          <a-input
            size="large"
            type="password"
            autocomplete="false"
            placeholder="请输入登录密码"
            v-decorator="[
              'password',
              {
                rules: [{ required: true, message: '请输入密码' }],
                validateTrigger: 'blur',
              },
            ]"
          >
            <a-icon
              slot="prefix"
              type="lock"
              :style="{ color: 'rgba(0,0,0,.25)' }"
            />
          </a-input>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: this.$form.createForm(this),
      visible: false,
      confirmLoading: false,
    };
  },
  methods: {
    // 显示
    showModal() {
      this.form.resetFields();
      this.visible = true;
    },
    // 表单提交
    formSubmit() {
      const {
        form: { validateFields },
      } = this;
      validateFields((errors, values) => {
        if (!errors) {
          this.confirmLoading = true;
          this.$http.post("/mf/add_account", values).then((res) => {
            this.confirmLoading = false;
            if (res.code === "0000") {
              this.visible = false;
              this.$message.success("添加账号成功");
              this.$emit("complate");
            } else {
              this.$message.warning(res.msg);
            }
          });
        }
      });
    },
  },
};
</script>