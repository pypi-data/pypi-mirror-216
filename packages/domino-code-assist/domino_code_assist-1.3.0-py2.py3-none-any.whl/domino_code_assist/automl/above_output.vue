<template>
  <div class="above-output-sticky mt-4">
    <div style="display: flex">
      <div class="prompt"></div>
      <div>
        <jupyter-widget :widget="widget" v-for="widget in children"></jupyter-widget>
      </div>
    </div>
  </div>
</template>
<script>
model.exports = {
  mounted() {
    let output = this.$el
    while (!(output.classList.contains("output_wrapper") || output.classList.contains("jp-Cell-outputWrapper")) || output == null) {
      output = output.parentElement;
    }
    let top = this.$el
    while (!top.classList.contains("vuetify-styles")) {
      top = top.parentElement;
    }
    if (output) {
      window.bla = top
      this.__content = top
      output.parentElement.insertBefore(this.__content, output)
    }
  },
  beforeDestroy() {
    if (this.__content) {
      this.__content.parentElement.removeChild(this.__content);
    }
  },
}
</script>
<style id="above-output-sticky">
.jp-Notebook-cell .above-output-sticky .prompt {
  min-width: 72px;
}
</style>
