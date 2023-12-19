<template>
  <div class="w-full h-full pt-2">
    <TabButtons v-model="selectedTab" :buttons="tabs" :onTabChanged="active" />
    <div class="pt-3 h-full">
      <ListViewTable :doctype="selectedTab" :filters="filters" :isloading="isloading" />
    </div>
  </div>
</template> 
 
<script setup>
import { ref } from 'vue';
import { TabButtons } from 'frappe-ui'
import ListViewTable from '@/component/ListViewTable.vue'
let filters = [
  {
    name:'id',
    type: 'text',
    placeholder: 'ID',
    disabled: false
  }
]
const props = defineProps({
  tabs: {
    type: Array,
    required: true,
  },
});
const selectedTab = ref(props.tabs[0]?.value);
let isloading = ref(false);
const active = () => {
  isloading.value = true
}
</script>
 