<template>
    <div class="w-full h-screen px-2 pt-12 md:p-12">
        <div class="w-full h-12 bg-gray-50 fixed top-0 left-0 flex justify-between items-center px-6">
            <p>Dashboard</p>
            <Dropdown :options="[
            {
                label: 'Logout',
                onClick: () =>  auth.logout.submit(),
            }
            ]">
            <Tooltip
            :text="session.user"
            :hover-delay="1"
            :placement="'bottom'"
            >
            <Button>
                    {{ session.user?.split('')[0] }}
                </Button class="w-10 h-10" :shape="'circle'" :image="null" :label="session.user" size="md">
            </Tooltip>
            </Dropdown>
        </div>
        <TabList v-if="doc?.data" :tabs="doc?.data?.map(tab => ({ label: tab.name }))" />

    </div>
</template>

<script setup>
import TabList from '@/component/TabList.vue'
import { createResource, Dropdown, Button,Tooltip } from 'frappe-ui';
import { session } from '../data/session'
import { ref } from 'vue'

const auth = ref(session)
const doc = createResource({
    url: "sva_report.controllers.get_report_list.get_report_list",
    fields: ['*'],
    auto: true
})
</script>
