<template>
  <div style="width: 80vw;max-width: 600px;">
    <var-space direction="column" justify="center">
      <h2>背诵工具</h2>
      <var-select v-model="selectArticle" placeholder="选择一篇文章或自定义" clearable @clear="clear_">
        <template #clear-icon="{ clear }" v-if="!!(presetData.filter(item => item.id === selectArticle)[0])">
          <var-icon name="delete" color="LightCoral" class="clear-icon"
            v-if="presetData.filter(item => item.id === selectArticle)[0].local" @click="clear_" />
        </template>
        <template v-for="item in selectArticleOptions" :key="item.value">
          <var-option v-if="item.local" :value="item.value" :label="item.label">
            <template #default>
              <var-space justify="space-between">
                <span>
                  {{ item.label }}
                  <span style="color: gray;">(本地)</span>
                </span>
              </var-space>
            </template>
          </var-option>
          <var-option v-else :value="item.value" :label="item.label" />
        </template>
        <var-option value="custom-text" key="997" label="自定义:文本" />
        <var-option value="custom-knockout" key="998" label="自定义:挖空" />
        <var-option value="custom-k-v" key="999" label="自定义:键值对" />
      </var-select>
      <var-input placeholder="输入文本，一行一节，常见标点符号分割" v-if="selectArticle === 'custom-text'" v-model="customText" textarea />
      <var-input placeholder="输入文本，一行一句，双引号引出挖空内容" v-if="selectArticle === 'custom-knockout'" v-model="customKnockout" textarea />
      <var-paper :elevation="2" v-if="selectArticle === 'custom-k-v'">
        <var-cell ripple v-for="(item, index) in customKv" :key="item.id">
          <var-space>
            <var-input placeholder="键" v-model="item.key" />
            <var-input placeholder="值" v-model="item.value" />
          </var-space>
          <template #extra>
            <var-space :wrap="false" align="center">
              <span style="color: lightslategray;">#{{ index }}</span>
              <var-button type="primary" @click="customKv.splice(customKv.indexOf(item), 1)" round>
                <var-icon name="delete" />
              </var-button>
              <var-button @click="customKv.push({ key: '', value: '', id: uuidv4() })" round>
                <var-icon name="plus" />
              </var-button>
            </var-space>
          </template>
        </var-cell>
      </var-paper>
      <var-button type="primary" @click="temNameVisible = true"
        v-if="selectArticle === 'custom-k-v' || selectArticle === 'custom-text' || selectArticle === 'custom-knockout'">保存</var-button>
      <var-dialog title="输入名称" v-model:show="temNameVisible" @confirm="save">
        <template #default>
          <var-input placeholder="输入名称" v-model="temName" />
        </template>
      </var-dialog>
      <var-select v-model="selectType" placeholder="选择默写类型">
        <var-option value="up-down" label="上默下" />
        <var-option value="down-up" label="下默上" />
        <var-option value="random" label="随机" />
      </var-select>
      <var-input placeholder="输入随机概率" v-if="selectType === 'random'" v-model="randomRate" :rules="[(v) => checkRate(v)]"
        type="number" />
      <template v-if="selectArticle === 'custom-text'">
        <group :context="handledCustomText" :displayType="selectType" v-if="!!(selectType)"
          v-model:displayAll="displayAll" :randomRate="randomRate" />
      </template>
      <template v-else-if="selectArticle === 'custom-k-v'">
        <group :context="handledCustomKV" :displayType="selectType" v-if="!!(selectType)"
          v-model:displayAll="displayAll" :randomRate="randomRate" />
      </template>
      <template v-else-if="selectArticle === 'custom-knockout'">
        <group :context="handledCustomKnockout" :displayType="selectType" v-if="!!(selectType)"
          v-model:displayAll="displayAll" :randomRate="randomRate" />
      </template>
      <template v-else>
        <group :context="presetData.filter(item => item.id === selectArticle)[0]" :displayType="selectType"
          v-if="!!(presetData.filter(item => item.id === selectArticle)[0]) && !!(selectType)"
          v-model:displayAll="displayAll" :randomRate="randomRate" />
      </template>
      <span style="color: lightgray;">Powered by Vue 3 & Varlet | by @zy | source code at <a href="https://github.com/iszyzyzzy/reciteTools" style="color: lightblue">github</a></span>
    </var-space>
  </div>
</template>
<script setup>
import { ref, computed } from 'vue'
import isNumber from 'is-number'
import { v4 as uuidv4 } from 'uuid';
import group from './components/group.vue'

const displayAll = ref(false)

const selectArticle = ref('')

let presetData = ref([])
// 开发
fetch("./preset-text.json",
  //  fetch("https://www.zyzyzzy.top/upload/preset-text.json",
  {
    mode: 'cors',
  }
)
  .then(res => res.json())
  .then(data => {
    presetData.value = data
  })
  .catch(err => {
    console.log("获取预设失败")
    console.log(err)
    presetData.value = []
  })
  .finally(() => {
    if (localStorage.getItem('reciteToolLocalData')) {
      localData.value = JSON.parse(localStorage.getItem('reciteToolLocalData'))
      for (let i = 0; i < localData.value.customText.length; i++) {
        presetData.value.push(localData.value.customText[i])
      }
      for (let i = 0; i < localData.value.customKv.length; i++) {
        presetData.value.push(localData.value.customKv[i])
      }
    }
  })
console.log(presetData.value)

const localData = ref({
  customText: [],
  customKv: [],
  customKnockout: [],
  disnableId: [],
})

const save = () => {
  if (selectArticle.value === 'custom-text') {
    localData.value.customText.push({
      name: temName.value,
      author: 'you',
      id: uuidv4(),
      text: customText.value,
      cut: customText.value.split('\n').map(item => {
        return item.split(/([,.!?;，。！？；])/)
      }),
      local: true
    })
    presetData.value.push(localData.value.customText[localData.value.customText.length - 1])
  } else if (selectArticle.value === 'custom-k-v') {
    localData.value.customKv.push({
      name: temName.value,
      author: 'you',
      id: uuidv4(),
      text: customKv.value,
      cut: customKv.value.map(item => {
        return [item.key, ":", item.value, ""]
      }),
      local: true
    })
    presetData.value.push(localData.value.customKv[localData.value.customKv.length - 1])
  } else if (selectArticle.value === 'custom-knockout') {
    localData.value.customKnockout.push({
      name: temName.value,
      author: 'you',
      id: uuidv4(),
      text: customKnockout.value,
      cut: customKnockout.value.split('\n').map(item => {
        return item.split(/(["“”])/)
      }),
      local: true
    })
    presetData.value.push(localData.value.customKnockout[localData.value.customKnockout.length - 1])
  }
  localStorage.setItem('reciteToolLocalData', JSON.stringify(localData.value))
}

const temName = ref("")
const temNameVisible = ref(false)

const delete_ = (id) => {
  console.log("delete",id)
  presetData.value = presetData.value.filter(item => item.id !== id)
  localData.value.customText = localData.value.customText.filter(item => item.id !== id)
  localData.value.customKv = localData.value.customKv.filter(item => item.id !== id)
  localData.value.customKnockout = localData.value.customKnockout.filter(item => item.id !== id)
  localStorage.setItem('reciteToolLocalData', JSON.stringify(localData.value))
}

const selectArticleOptions = computed(() => {
  return presetData.value.map(item => {
    return {
      label: item.name,
      value: item.id,
      local: item.local
    }
  })
})

const selectType = ref('')
const randomRate = ref(0.5)
const checkRate = (value) => {
  if (isNumber(value)) {
    if (value >= 0 && value <= 100) {
      return true
    } else {
      return "请输入0-100之间的数字"
    }
  } else {
    return "请输入数字"
  }
}
const customText = ref('')
const customKv = ref([{
  key: '',
  value: '',
  id: uuidv4()
}])
const handledCustomText = computed(() => {
  let data = customText.value.split('\n').map(item => {
    return item.split(/([,.!?;，。！？；])/)
  })
  console.log(data)
  return {
    name: "自定义文本",
    author: "you",
    id: -1,
    text: customText.value,
    cut: data
  }
})
const handledCustomKV = computed(() => {
  return {
    name: "自定义键值对",
    author: "you",
    id: -1,
    text: customKv.value,
    cut: customKv.value.map(item => {
      return [item.key, ":", item.value, ""]
    })
  }
})
const handledCustomKnockout = computed(() => {
  selectType.value = 'up-down'
  return {
    name: "自定义挖空",
    author: "you",
    id: -1,
    text: customKnockout.value,
    cut: customKnockout.value.split('\n').map(item => {
      return item.split(/(["“”])/)
    })
  }
})
const clear_ = () => {
  console.log("clear", selectArticle.value)
  if (!!(presetData.value.filter(item => item.id === selectArticle.value)[0])) {
    if (presetData.value.filter(item => item.id === selectArticle.value)[0].local) {
      delete_((presetData.value.filter(item => item.id === selectArticle.value)[0]).id)
    } else {
      selectArticle.value = ''
    }
  }
}
const customKnockout = ref('')
</script>