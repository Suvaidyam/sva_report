<template>
    <div class="w-full mx-auto border h-full relative rounded-md flex flex-col">

        <div class="w-full flex items-center border-b justify-between">
            <div class="pl-4 h-auto w-[50%] font-semibold text-sm text-gray-700">
                <p>Total records :- <span>{{ resource?.data?.total_records ?? 0 }}</span></p>
            </div>
            <div
                class="w-[50%] sticky top-0 md:h-14 flex flex-col md:flex-row py-1 justify-end items-center px-4 gap-2">
                <div class="flex items-center gap-2">
                    <Filter v-if="resource?.data?.filters.length" :filterCount="filterCount" :filterFields="filterFields" :applyFilters="applyFilters"
                        :clearFilters="clearFilters" :fields="resource?.data ?? {}" />
                    <div class="flex" v-if="false">
                        <Button size="md" :icon="'align-left'" class="rounded-l-md border rounded-r-none"></Button>
                        <Autocomplete size="md" :options="resource?.data?.columns" v-model="sortValue"
                            class="rounded-r-md border rounded-l-none bg-gray-100 py-[1px]" />
                    </div>
                    <div class="flex">
                        <Tooltip text="download csv">
                            <Button size="md" :icon="'download'" @click="handleDownload"></Button>
                        </Tooltip>
                    </div>
                </div>
            </div>
        </div>
        <div class="w-full h-full overflow-y-auto">
            <Loader v-if="isloading" />
            <!-- LIST TABLE -->
            <div v-else>
                <table class="w-full text-sm text-left rtl:text-right text-gray-500">
                    <thead class="text-xs text-gray-800 bg-gray-50">
                        <tr>
                            <th scope="col" class="px-4 py-2 truncate" v-for="(column, index) in resource?.data?.columns"
                                :key="index">{{ column.label }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="bg-white border-b hover:bg-gray-100"
                            v-for="(item, itemIndex) in resource?.data?.data" :key="itemIndex">
                            <td scope="row" class="px-4 py-2 font-medium text-gray-900 whitespace-nowrap"
                                v-for="(column, columnIndex) in resource?.data?.columns" :key="columnIndex">
                                {{ item[column.key] }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!-- LIST TABLE -->
        </div>
        <div class="w-full h-16 sticky bottom-0 border-t flex justify-between items-center px-4">
            <div class="flex w-44">
                <Button size="md" @click="handleButtonClick(10)" :class="page_limit == 10 ? 'border rounded-r-none bg-gray-100'
                    : 'bg-gray-50 rounded-r-none'">10</Button>
                <Button size="md" @click="handleButtonClick(50)" :class="page_limit == 50 ? 'border rounded-l-none rounded-r-none bg-gray-100'
                    : 'bg-gray-50 rounded-l-none rounded-r-none'">50</Button>
                <Button size="md" @click="handleButtonClick(500)" :class="page_limit == 500 ? 'border rounded-l-none bg-gray-100'
                    : 'bg-gray-50 rounded-l-none'">500</Button>
            </div>
            <div>
                <Pagination :getCurrentPage="getCurrentPage" :totalCount="resource?.data?.total_records"
                    :perPageData="page_limit" :currentPage="currentPage" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { createResource, Autocomplete, Tooltip } from 'frappe-ui'
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
let sortValue = ref('Name');
let isloading = ref(false);
let currentPage = ref(1);
const filterCount = ref(0);
const filterFields = ref([{ key: 1, field1: '', field2: '', field3: '', options: [{ label: '=', value: '=' }], options2: [] }]);
// page limit
const handleButtonClick = (e) => {
    page_limit.value = e
}
const handleDownload = (e) => {
    window.open(`/api/method/sva_report.controllers.get_report_data.execute?doc=${props.doctype}&csv_export=1`, '_blank');
}
// pagination
const getCurrentPage = (page) => {
    currentPage.value = page
    console.log(page)
}
// api call
isloading.value = true
let resource = createResource({
    url: "sva_report.controllers.get_report_data.execute",
    params: {
        doc: props.doctype,
        sort: sortValue.value,
        skip: (currentPage.value - 1) * page_limit.value,
        limit: page_limit.value,
    },
    auto: true,
    onSuccess() {
        setTimeout(() => {
            isloading.value = false
        }, 1000)
    },
});
let filters = ref([])
watch([() => props.doctype, () => page_limit.value, () => currentPage.value, () => sortValue.value, () => filters.value],
    async ([
        newDoctype, newPageLimit, newCurrentPage, newSort, newFilters
    ], [
        oldDoctype, oldPageLimit, oldCurrentPage, oldSort, oldFilters
    ]) => {
        if (newDoctype !== oldDoctype || newPageLimit !== oldPageLimit || newCurrentPage !== oldCurrentPage || newSort !== oldSort || newFilters != oldFilters) {
            isloading.value = true
            resource = createResource({
                url: "sva_report.controllers.get_report_data.execute",
                params: {
                    doc: newDoctype,
                    filters: filters.value,
                    sort: newSort.name,
                    skip: (newCurrentPage - 1) * newPageLimit,
                    limit: newPageLimit,
                },
                auto: true,
                onSuccess() {
                    setTimeout(() => {
                        isloading.value = false
                    }, 1000)
                },
            });
        }
    });

// filter api call
const applyFilters = () => {
    const allFieldsFilled = filterFields.value.every((filter) => {
        return filter.field1 !== '' && filter.field2 !== '' && filter.field3 !== '';
    });
    if (allFieldsFilled) {
        isloading.value = true
        filters.value = filterFields.value.map(item => [item.field1, item.field2, (item.field3?.value || item.field3)]);
        console.log(filterFields.value)
    } else {
        console.log('Please fill all fields in each filter before applying filters.');
    }
};
const clearFilters = () => {
    filterFields.value = [{ key: 1, field1: '', field2: '', field3: '', options: [{ label: '=', value: '=' }], options2: [] }]
    let isValue = filterFields.value.forEach((filter) => {
        filter.field1 = '';
        filter.field2 = '';
        filter.field3 = '';
    });
    if (isValue) {
        isloading.value = true
        resource = createResource({
            url: "sva_report.controllers.get_report_data.execute",
            params: {
                doc: props.doctype,
                filters: [],
                skip: (currentPage.value - 1) * page_limit.value,
                limit: page_limit.value,
            },
            auto: true,
            onSuccess() {
                setTimeout(() => {
                    isloading.value = false
                }, 1000)
            },
        });
    }

    filterCount.value = 0;
};
// filter workin

</script>