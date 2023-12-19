<template>
    <div class="w-full h-screen px-2 pt-12 md:p-12">
        <div class="w-full h-12 bg-gray-50 fixed top-0 left-0"></div>
        <TabList :tabs="doc.data.map(tab => {
            return { label: tab.name };
        })" />
    </div>
</template>
  
<script setup>
import TabList from '@/component/TabList.vue'
import { createResource } from 'frappe-ui';

const doc = createResource({
    url: "sva_report.controllers.get_report_list.get_report_list",
    fields: ['*'],
    auto: true
})

</script>
  