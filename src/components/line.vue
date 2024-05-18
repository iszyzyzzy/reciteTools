<template>
    <var-cell v-if="props.context[0].text[0]">
        <template #default>
            <template v-for="item in props.context">
                <template v-if="item.text[0]">
                    <span v-if="item.display || modelDisplay">{{item.text[0]}}</span>
                    <span v-else>{{generateUnderlines(item.text[0])}}</span>
                    <span v-if="item.text[1]">{{item.text[1]}}</span>
                </template>
            </template>
        </template>
        <template #extra>
            <var-icon transition="100" :name="modelDisplay ? 'view-outline' : 'view'" @click="() => modelDisplay = !modelDisplay"/>
        </template>
    </var-cell>
    <var-divider v-else />
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
    context: Array,
})
const modelDisplay = ref(false)

const generateUnderlines = (text) => {
    return "__".repeat(text.length)
}
/*
context:[
{
    text:["",""],
    display:Ture/False
}
]
 */
</script>