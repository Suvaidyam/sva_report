<template>
   <div class="text-sm font-medium text-center pb-4 ">
      <ul class="flex flex-wrap -mb-px gap-1">
         <li class="me-2" v-for="(item, index) in tabs" :key="index">
            <a @click="activateTab(index,item?.title)" :class="active === index ? 'text-blue-600 border-b-2 cursor-pointer p-2 border-blue-600' :
               'text-gray-600 hover:border-b-2 cursor-pointer p-2 hover:border-gray-600'">
               {{ item.title }}
            </a>
         </li>
      </ul>
   </div>
</template> 
 
<script setup>
import { ref , defineEmits } from 'vue';

const props = defineProps({
   tabs: {
      type: Array,
      required: true,
   },
});
const emit = defineEmits(['tabChanged']);
const active = ref(0);

const activateTab = (index,item) => {
   active.value = index;
   emit('tabChanged', index,item);
};
</script>
 