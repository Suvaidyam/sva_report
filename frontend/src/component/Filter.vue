<template>
    <Popover >
        <template #target="{ togglePopover }">
            <button @click="togglePopover()"
                class="bg-gray-100 border rounded-r-none rounded-l-md text-gray-600 flex items-center gap-1 px-3 py-0.5 ">
                Filter
                <p v-if="filterCount > 0" class="text-sm">{{ filterCount }}</p>
            </button>
            <Button @click="clearFilters" :icon="'x'" class=" rounded-l-none py-4"></Button>
        </template>
        <template #body-main>
            <div class="p-2 max-w-lg w-auto md:w-[500px]">
                <div class="flex flex-col gap-2">
                    <div v-for="(filter, index) in filterFields" :key="index"
                        class="flex flex-col md:flex-row gap-2 items-center">
                        <Select v-if="fields?.columns?.length > 0" :options="fields?.columns?.map(tab => {
                            return { label: tab.label, value: JSON?.stringify({ type: tab?.fieldtype, value: tab?.fieldname }) };
                        })" v-model="filter.field1" class="md:flex-1 w-full md:w-auto " />
                        <Select :options="newSelectedValues[index]?.options" v-model="filter.field2" class="md:flex-1 w-full md:w-auto " />
                        <!-- newSelectedValues[index]?.options[0]?.type?.toLowerCase() -->
                        <FormControl :type="'select'" size="sm" variant="subtle" v-model="filter.field3"
                            :options="newSelectedValues[index]?.options2" class="md:flex-1 w-full md:w-auto " /> 
                        <Button @click="removeFilterField(index)" :icon="'x'"
                            class="bg-transparent hover:bg-transparent"></Button>
                    </div>
                    <div class="flex py-2 border-t items-center justify-between">
                        <div>
                            <Button @click="addFilterField" class="bg-white hover:bg-transparent">Add a Filter</Button>
                        </div>
                        <div class="flex gap-2">
                            <Button @click="clearFilters">Clear Filters</Button>
                            <Button @click="applyFilters" variant="solid">Apply Filters</Button>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Popover>
</template>
<script setup>
import { FormControl, Popover, Select } from 'frappe-ui'
import { ref, watch } from 'vue';

const props = defineProps({
    filterFields: {
        type: Array,
        required: true,
    },
    filterCount: {
        type: Number,
        required: true,
    },
    applyFilters: {
        type: Function,
        required: true,
    },
    clearFilters: {
        type: Function,
        required: true,
    },
    fields: {
        type: Object,
        required: true,
    },
})
let dataType = ref([
    {
        id: 1,
        label: 'Equals',
        type: 'Data',
    },
    {
        id: 2,
        label: 'Not Equals',
        type: 'Data',
    },
    {
        id: 3,
        label: 'Like',
        type: 'Data',
    },
    {
        id: 4,
        label: '=',
        type: 'Phone',
    },
    {
        id: 5,
        label: '!=',
        type: 'Phone',
    },
    {
        id: 6,
        label: '>=',
        type: 'Phone',
    },
    {
        id: 7,
        label: '>=',
        type: 'Select',
    },
])
let newSelectedValues = ref([])
watch(() => props.filterFields, (newFilterFields, oldFilterFields) => {
    newSelectedValues.value = newFilterFields.map(filter => {
        if (filter.field1) {
            try {
                return {
                    ...filter,
                    options: dataType.value.filter(item => item.type === JSON.parse(filter.field1).type),
                    options2:props.fields.data.map(item => ({ label: item[JSON.parse(filter.field1 ?? "{}")?.value], value: item[JSON.parse(filter.field1 ?? "{}")?.value] }))
                };
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }
        return { ...filter, options: [] };
    });
}, { deep: true });
const addFilterField = () => {
    const newKey = props.filterFields.length + 1;
    props.filterFields.push({ key: newKey, field1: '', field2: '', field3: '', options: [],options2: [] });
};

const removeFilterField = (index) => {
    props.filterFields.splice(index, 1);
};



</script>
