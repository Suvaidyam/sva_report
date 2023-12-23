<template>
    <Popover>
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
                    <div v-for="(filterRow, index) in filterFields" :key="index"
                        class="flex flex-col md:flex-row gap-2 items-center">
                        <Select v-if="fields?.filters?.length > 0" :options="getFields(index)" v-model="filterRow.field1"
                            class="md:flex-1 w-full md:w-auto " />
                        <Select :options="newSelectedValues[index]?.options" v-model="filterRow.field2"
                            class="md:flex-1 w-full md:w-auto " />
                        <!-- newSelectedValues[index]?.options[0]?.type?.toLowerCase() -->
                        <FormControl :type="newSelectedValues[index]?.fieldtype" size="sm" variant="subtle"
                            v-model="filterRow.field3" :options="newSelectedValues[index]?.options2"
                            class="md:flex-1 w-full md:w-auto " />
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
import { FormControl, Popover, Select, createResource, Autocomplete } from 'frappe-ui'
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
let dataType = {
    "Data": ["=", "!=", "Like"],
    "Phone": ["=", "!=", "Like"],
    "Int": ["=", "!=", "<", ">", "<=", ">="],
    "Select": ["=", "!="],
    "Link": ["=", "!="],
    "Date": ["=", "!=", "<", ">", "<=", ">="]
}
const createRes = (doctype, txt = '') => {
    return new Promise((resolve) => {
        createResource({
            url: "frappe.desk.search.search_link",
            params: {
                doctype,
                txt,
                pageLength: 1000,
            },
            auto: true,
            onSuccess(data) {
                resolve(data)
            },
        });
    })
}
let newSelectedValues = ref([])

watch(() => props.filterFields, async (newFilterFields, oldFilterFields) => {
    newSelectedValues.value = await Promise.all(newFilterFields.map(async filter => {
        if (filter.field1) {
            try {
                let _field = props.fields?.filters?.find(f => f.fieldname == filter.field1)
                if (dataType[_field?.fieldtype]) {
                    let option2 = []
                    if (_field?.fieldtype == 'Link') {
                        option2 = await createRes(_field.options);
                    } else {
                        option2 = _field.options?.split('\n')?.map(item => ({ label: item, value: item }))
                    }
                    return {
                        ...filter,
                        fieldname: _field.fieldname,
                        fieldtype: (_field.fieldtype == 'Link' ? 'Select' : _field.fieldtype).toLowerCase(),
                        options: dataType[_field.fieldtype].map(e => { return { label: e, value: e } }),
                        options2: option2
                    };
                } else {
                    return {
                        ...filter,
                        fieldname: _field?.fieldname,
                        fieldtype: (_field?.fieldtype == 'Link' ? 'Select' : _field.fieldtype).toLowerCase(),
                        options: [],
                        options2: []
                    };
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }
        return { ...filter, options: [] };
    }));
    console.log("newSelectedValues.value", newSelectedValues.value);
}, { deep: true });
const addFilterField = () => {
    const newKey = props.filterFields.length + 1;
    props.filterFields.push({ key: newKey, field1: '', field2: '', field3: '', options: [], options2: [] });
};

const removeFilterField = (index) => {
    props.filterFields.splice(index, 1);
};
const getFields = (index) => {
    return props.fields?.filters?.map(e => { return { label: e.label, value: e?.fieldname } })
    // let opts = newSelectedValues.value?.filter((e, i) => index !== i).map(e => e.fieldname)
    // return (props.fields?.filters?.filter(f => !opts.includes(f.fieldname)))?.map(tab => {
    //     return { label: tab.label, value: tab?.fieldname };
    // })
}


</script>
