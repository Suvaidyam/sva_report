<template>
  <div class="w-full h-full pt-2">
    <TabButtons class="overflow-x-auto" v-model="selectedTab" :buttons="tabs" />
    <div class="pt-3 h-full" v-if="selectedTab">
      <ListViewTable :doctype="selectedTab" :filters="filters" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { TabButtons } from 'frappe-ui'
import ListViewTable from '@/component/ListViewTable.vue'
let filters = [
  {
    name: 'id',
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
const selectedTab = ref(props?.tabs?.[0]?.label);

</script>
