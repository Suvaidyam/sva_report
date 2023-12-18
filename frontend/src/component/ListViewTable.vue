<template>
      <div class="w-full mx-auto border h-full relative rounded-md flex flex-col">
            <!-- top -->
            <div class="w-full sticky top-0 h-14 border-b flex justify-between items-center px-4 gap-2">
                <div class="" v-for="item in filters">
                    <FormControl
                        :type="item.type"
                        size="sm"
                        variant="subtle"
                        :options="item?.option ?? []"
                        :placeholder="item.placeholder"
                        :disabled="item.disabled"
                    />
                </div>  
                <div class="flex items-center gap-2">
                    <button class="bg-gray-100 rounded-md px-2 py-0.5 text-gray-500">Fiter</button>
                    <button class="bg-gray-100 rounded-md px-2 py-0.5 text-gray-500">Last Updateed On</button>
                </div>
            </div>
            <div class="w-full h-full overflow-y-scroll">
                <Loader v-if="activeTab.index === 1"/>
                {{ activeTab }}
                <!-- <ListView
                    class="h-[250px]"
                    :columns="[
                        {
                        label: 'Name',
                        key: 'name',
                        width: 3,
                        }
                    ]"
                    :rows="[
                        {
                        id: 1,
                        name: 'John Doe',
                        },
                    ]"
                    :options="{name: 'User', params: { userId: 1 } }"
                    row-key="id"
                    /> -->
            </div>
            <div class="w-full h-16 sticky bottom-0 border-t"></div>
        </div>
</template>

<script setup>
import {FormControl} from 'frappe-ui'
import Loader from '@/component/Loader.vue'
 const props = defineProps({
	doctype: {
		type: String,
		required: true,
	},
	filters: {
		type: Array,
		required: true,
	},
	groupBy: {
		type: String,
		required: false,
	},
    activeTab:{
        type: Object,
		required: true, 
    },
    isloading:{
        type:Boolean,
        required:true
    }
	// filterConfig: {
	// 	type: Array,
	// 	required: true,
	// },
	// tabButtons: {
	// 	type: Array,
	// 	required: true,
	// },
})
</script>