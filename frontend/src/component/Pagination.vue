<script setup>
    import VuePaginationTw from 'vue-pagination-tw';
    import "vue-pagination-tw/styles";

    const props = defineProps({
    getCurrentPage: {
        type: Function,
        required: true,
    },
    totalCount: {
        type: Number,
        required: true,
    },
    perPageData: {
        type: Number,
        required: true,
    },
    currentPage: {
        type: Number,
        required: true,
    },
   
})
</script>

<template>
    <div v-if="totalCount > 0" class=" absolute bottom-0 right-0 bg-white px-6 z-40 w-auto py-1.5">
        <div>
            <VuePaginationTw :total-items="totalCount" :current-page="currentPage" :per-page="perPageData"
                @page-changed="getCurrentPage" />
        </div>
    </div>
</template>

<style>
    ul li button.w-12:disabled {
        background: #263948 !important;
        color: white;
        border: 1px solid gray;
    }
</style>