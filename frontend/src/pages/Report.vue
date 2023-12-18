<template>
    <div class="w-full h-screen p-12">
        <div class="w-full h-12 bg-gray-50 fixed top-0 left-0"></div>
        <TabList :tabs="tabs"  />
    </div>
</template>
  
<script setup>
import TabList from '@/component/TabList.vue'

let tabs = [
    {
        label: 'Beneficiary',
        value:'beneficiary'
    },
    {
        label: 'User',
        value:'user'
    }
]

</script>
  