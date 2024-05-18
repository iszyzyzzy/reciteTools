<template>
    <var-card :title="props.context.name" v-model:floating="floating">
        <template #description>
            <template v-for="item in usedContextArray">
                <Line :context="item" />
            </template>
        </template>
        <template #extra>
            <var-space>
                <var-button type="primary" @click="() => displayAll = !displayAll">
                    显示全部
                </var-button>
                <var-button type="primary" @click="floating = true" v-if="!floating">开启全屏</var-button>
            </var-space>
        </template>
    </var-card>
</template>
<script setup>
import { ref, computed } from 'vue'
import Line from './line.vue'

const props = defineProps({
    context: Object,
    displayType: String,
    randomRate: {
        type: Number,
        default: 0.5
    }
})
const displayAll = defineModel('displayAll')

const floating = ref(false)

const generateDisplay = () => {
    if (props.displayType === 'up-down') {
        return [true, false]
    } else if (props.displayType === 'down-up') {
        return [false, true]
    } else if (props.displayType === 'random') {
        return [Math.random() < props.randomRate, Math.random() < props.randomRate]
    } else {
        return [true, true]
    }
}

const internalContextArray = computed(() => {
    let result = [[]]
    result[0].push({
        text: ["作者："],
        display: true
    })
    result[0].push({
        text: [props.context.author],
        display: false
    })
    for (let i = 0; i < props.context.cut.length; i++) {
        for (let j = 0; j < props.context.cut[i].length; j = j + 4) {
            result.push([])
            let d = generateDisplay()
            result[result.length - 1].push({
                text: [props.context.cut[i][j], props.context.cut[i][j + 1]],
                display: d[0]
            })
            result[result.length - 1].push({
                text: [props.context.cut[i][j + 2], props.context.cut[i][j + 3]],
                display: d[1]
            })
        }
    }
    return result
})
const usedContextArray = computed(() => {
    return internalContextArray.value.map(
        (item) => {
            return item.map(
                (item_) => {
                    return {
                        text: item_.text,
                        display: item_.display || displayAll.value
                    }
                }
            )
        }
    )
})
</script>