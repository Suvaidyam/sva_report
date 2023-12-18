<template>
    <div class="relative" ref="filterContainer">
        <Button :icon="'filter'" @click="openFilter" label="Filter"
            class="bg-gray-100 rounded-md px-2 py-0.5 text-gray-500"></Button>
        <div v-if="isOpenFilter"
            class="max-w-lg w-[500px] px-3 pt-3 right-0 absolute top-9 rounded-md bg-white border-2 shadow-sm">
            <div class="flex flex-col gap-2">
                <div  v-for="(filter, index) in filterFields" :key="index" class="flex gap-2 items-center">
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
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            isOpenFilter: false,
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
        },
        applyFilters() {
            console.log('Filters applied:', this.filterFields);
        },
        openFilter() {
            this.isOpenFilter = !this.isOpenFilter;

        },
        closeDropdown(event) {
            if (!this.$refs?.filterContainer?.contains(event?.target)) {
                this.isOpenFilter = false;
            }
        },
    },
    beforeDestroy() {
        window.removeEventListener('click', this.closeDropdown);
    },
    mounted(){
        window.addEventListener('click', this.closeDropdown);
    }

};
</script>
  