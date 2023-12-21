<template>
    <Popover>
        <template #target="{ togglePopover }">
            <button @click="togglePopover()" class="bg-gray-100 border rounded-r-none rounded-l-md text-gray-600 flex items-center gap-1 px-3 py-0.5 ">
                Filter
                <p v-if="filterCount > 0" class="text-sm">{{ filterCount }}</p>
            </button>
            <Button @click="clearFilters" :icon="'x'" class=" rounded-l-none py-4"></Button>
        </template>
        <template #body-main>
            <div class="p-2 max-w-lg w-auto md:w-[500px]">
                <div class="flex flex-col gap-2">
                    <div v-for="(filter, index) in filterFields" :key="index" class="flex flex-col md:flex-row gap-2 items-center">
                        <Input v-model="filter.field1" class="flex-1" />
                        <Input v-model="filter.field2" class="flex-1" />
                        <Input v-model="filter.field3" class="flex-1" />
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
import { Popover } from 'frappe-ui'
</script>
<script>
export default {
    data() {
        return {
            isOpenFilter: false,
            filterCount: 0,
            filterFields: [{ key: 1, field1: '', field2: '', field3: '' }]
        };
    },
    methods: {
        addFilterField() {
            const newKey = this.filterFields.length + 1;
            this.filterFields.push({ key: newKey, field1: '', field2: '', field3: '' });
        },
        removeFilterField(index) {
            this.filterFields.splice(index, 1);
        },
        clearFilters() {
            this.filterFields.forEach((filter) => {
                filter.field1 = '';
                filter.field2 = '';
                filter.field3 = '';
            });
            this.filterCount = 0
        },
        applyFilters() {
            const allFieldsFilled = this.filterFields.every(filter => {
                return filter.field1 !== '' && filter.field2 !== '' && filter.field3 !== '';
            });
            if (allFieldsFilled) {
                console.log('Filters applied:', this.filterFields);
                this.filterCount = this.filterFields.length;
            } else {
                console.log('Please fill all fields in each filter before applying filters.');
            }
        },
    },

};
</script>
  