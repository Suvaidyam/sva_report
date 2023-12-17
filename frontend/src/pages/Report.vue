<template>
    <div class="w-full h-screen p-12">
        <TabList />
        <ListViewTable 
        :doctype="'user'"
        :filters="filters"
        />
        
    </div>
</template>
  
<script setup>

 import TabList from '@/component/TabList.vue'
 import ListViewTable from '@/component/ListViewTable.vue'
 let filters = [
    {
        type:'text',
        placeholder:'ID',
        disabled:false
    }
 ]
</script>
  