<template>
    <div class="w-full mx-auto border h-full relative rounded-md flex flex-col">
        <!-- top -->
        <!-- <div>{{ resource?.data?.columns }}</div> -->

        <div
            class="w-full sticky top-0 md:h-14 border-b flex flex-col md:flex-row py-1 justify-between items-center px-4 gap-2">
            <div class="" v-for="item in resource?.data?.filters">
                <FormControl v-model="formData[item.fieldname]" :type="item.fieldtype" :name="item.fieldname" size="sm"
                    variant="subtle" :options="item?.options ?? ''" :placeholder="item.label" />
            </div>
            <div class="flex items-center gap-2">
                <Filter />
                <div class="flex">
                    <Button size="md" :icon="'align-left'" class="rounded-l-md border rounded-r-none"></Button>
                    <Dropdown placement="left" class="bg-gray-50 truncate rounded-r-sm rounded-l-none" :options="dropdown"
                        :button="{
                            label: 'Last Updated On',
                        }" />
                </div>
            </div>
        </div>
        <div class="w-full h-full overflow-y-auto">
            <Loader v-if="isloading" />
            <List v-else class="h-[250px]" :columns="resource?.data?.columns" :rows="resource?.data?.data" />
        </div>
        <div class="w-full h-16 sticky bottom-0 border-t flex justify-between items-center px-4">
            <div class="flex">
                <Button size="md" @click="handleButtonClick(10)" class="rounded-l-sm border rounded-r-none">10</Button>
                <Button size="md" @click="handleButtonClick(50)" class="bg-gray-50 rounded-none">50</Button>
                <Button size="md" @click="handleButtonClick(500)"
                    class="bg-gray-50 rounded-r-sm rounded-l-none">500</Button>
            </div>
            <Pagination />
        </div>
    </div>
</template>

<script setup>
import { FormControl, List, Dropdown, createResource, resourcesPlugin } from 'frappe-ui'
import { ref, watch } from 'vue'
import Loader from '@/component/Loader.vue'
import Filter from '@/component/Filter.vue'
import Pagination from '@/component/Pagination.vue'

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
    activeTab: {
        type: Object,
        required: false,
    },
})
const table = ref({
    columns: [],
    rows: []
})
let dropdown = [
    {
        label: 'Edit Title',
        onClick: () => {
        },
    },
    {
        label: 'Manage Members',
        onClick: () => {
        },
    },
    {
        label: 'Delete this project',
        onClick: () => {
        },
    },
]
const handleButtonClick = (e) => {
    console.log(e)
}
const formData = ref({
    id: ''
})
let isloading = ref(false);
let docParams = props.doctype
const resource = createResource({
    url: "sva_report.controllers.get_report_data.execute",
    params: {
        doc: docParams,
    },
    auto: true
});
watch(() => props.doctype, async (newValue, oldValue) => {
    if (newValue !== oldValue) {
        docParams = newValue
    }
});

</script>