<template>
    <div class="w-full mx-auto border h-full relative rounded-md flex flex-col">
        <div
            class="w-full sticky top-0 md:h-14 border-b flex flex-col md:flex-row py-1 justify-between items-center px-4 gap-2">
            <p></p>
            <div class="flex items-center gap-2">
                <Filter :filterCount="filterCount" :filterFields="filterFields" :applyFilters="applyFilters"
                    :clearFilters="clearFilters" :fields="resource?.data?.columns" />
                <div class="flex">
                    <Button size="md" :icon="'align-left'" class="rounded-l-md border rounded-r-none"></Button>
                    <Autocomplete :options="dropdown" class="flex-1" />
                </div>
            </div>
        </div>
        <div class="w-full h-full overflow-y-auto">
            <Loader v-if="isloading" />
            <List v-else class="h-[250px]" :columns="resource?.data?.columns" :rows="resource?.data?.data" />
        </div>
        <div class="w-full h-16 sticky bottom-0 border-t flex justify-between items-center px-4">
            <div class="flex w-44">
                <Button size="md" @click="handleButtonClick(10)"
                    :class="page_limit == 10 ? 'border rounded-r-none bg-gray-100' : 'bg-gray-50 rounded-r-none'">10</Button>
                <Button size="md" @click="handleButtonClick(50)"
                    :class="page_limit == 50 ? 'border rounded-l-none rounded-r-none bg-gray-100' : 'bg-gray-50 rounded-l-none rounded-r-none'">50</Button>
                <Button size="md" @click="handleButtonClick(500)"
                    :class="page_limit == 500 ? 'border rounded-l-none bg-gray-100' : 'bg-gray-50 rounded-l-none'">500</Button>
            </div>
            <div>
                <Pagination :getCurrentPage="getCurrentPage" :totalCount="resource?.data?.total_records"
                    :perPageData="page_limit" :currentPage="currentPage" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { List, createResource, Autocomplete } from 'frappe-ui'
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
// ref value
let page_limit = ref(10);
let isloading = ref(false);
let currentPage = ref(1);
const filterCount = ref(0);
const filterFields = ref([{ key: 1, field1: '', field2: '', field3: '', options: [] }]);
// page limit
const handleButtonClick = (e) => {
    page_limit.value = e
}
// pagination
const getCurrentPage = (page) => {
    currentPage.value = page
}
// api call
let resource = createResource({
    url: "sva_report.controllers.get_report_data.execute",
    params: {
        doc: props.doctype,
        skip: (currentPage.value - 1) * page_limit.value,
        limit: page_limit.value,
    },
    auto: true
});
watch([() => props.doctype, () => page_limit.value], async ([newDoctype, newPageLimit], [oldDoctype, oldPageLimit]) => {
    if (newDoctype !== oldDoctype || newPageLimit !== oldPageLimit) {
        resource = createResource({
            url: "sva_report.controllers.get_report_data.execute",
            params: {
                doc: newDoctype,
                skip: (currentPage.value - 1) * newPageLimit,
                limit: newPageLimit,
            },
            auto: true
        });
    }
});

// filter api call
const applyFilters = () => {
    const allFieldsFilled = filterFields.value.every((filter) => {
        return filter.field1 !== '' && filter.field2 !== '' && filter.field3 !== '';
    });
    if (allFieldsFilled) {
        let isFilter = filterFields.value.map(item => [item.field1, item.field2, item.field3]);
       resource = createResource({
            url: "sva_report.controllers.get_report_data.execute",
            params: {
                doc: props.doctype,
                filters:isFilter,
                skip: (currentPage.value - 1) * page_limit.value,
                limit: page_limit.value,
            },
            auto: true
        });
        filterCount.value = filterFields.value.length;
    } else {
        console.log('Please fill all fields in each filter before applying filters.');
    }
};
const clearFilters = () => {
    filterFields.value.forEach((filter) => {
        filter.field1 = '';
        filter.field2 = '';
        filter.field3 = '';
    });
    filterFields.value = [{ key: 1, field1: '', field2: '', field3: '', options: [] }]
    filterCount.value = 0;
};
// filter workin

let dropdown = [
    {
        label: 'Edit Title',
        value: 'Edit Title',

    },
    {
        label: 'Manage Members',
        value: 'Manage Members',

    },
    {
        label: 'Delete this project',
        value: 'Delete this project',

    },
]
</script>