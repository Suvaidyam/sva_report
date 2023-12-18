<template>
    <div class="w-full h-screen p-12">
        <TabList 
            :tabs="tabs"
            @tabChanged="changeTab"
        />
        <ListViewTable 
        :doctype="'user'"
        :filters="filters"
        :activeTab="activeTab"
        :isloading="isloading"
        />
    </div>
</template>
  
<script setup>
import {ref} from 'vue'
 import TabList from '@/component/TabList.vue'
 import ListViewTable from '@/component/ListViewTable.vue'
 let filters = [
    {
        type:'text',
        placeholder:'ID',
        disabled:false
    }
 ]
 let tabs = [
    {
        title:'Beneficiary'
    },
    {
        title:'User'
    }
 ]
 let activeTab = ref({index:0,title:tabs[0]?.title});
 let isloading = ref(true);

const changeTab = (index,title) => {
  activeTab.value = {
    index:index,
    title:title
  };
  console.log(title)
};
const d = ref({})
</script>
  