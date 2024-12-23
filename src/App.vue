<script setup>
import DataBasic from './components/DataBasic.vue'
import DataWaves from './components/DataWaves.vue'
import DataHR from './components/DataHR.vue'
import DataCognitive from './components/DataCognitive.vue'
import DataLog from './components/DataLog.vue'
import DataEmotionHistory from './components/DataEmotionHistory.vue'
import DataEmotion from './components/DataEmotion.vue'
import { useStore } from './stores'
import { onMounted } from 'vue'

const store = useStore()

onMounted(() => {
  setInterval(() => {
    generateFakeDate(store)
  }, 3000)

  const socket = new WebSocket('ws://127.0.0.1:8080');

  socket.onopen = () => {
    console.log('WebSocket connection established');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle incoming data
    console.log(data);
  };

  socket.onclose = () => {
    console.log('WebSocket connection closed');
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
})

function generateFakeDate(store) {
  // Basic
  store.heartRate = Math.floor(Math.random() * 100 + 60)
  store.breathingRate = Math.floor(Math.random() * 20 + 10)
  store.leftEnergy = Math.random().toFixed(2)

  // Waves
  store.ECG = Array.from({ length: 100 }, () => Math.random())
  store.RESP = Array.from({ length: 100 }, () => Math.random())
  store.EDA = Array.from({ length: 100 }, () => Math.random())
  store.P = Array.from({ length: 100 }, () => Math.random())

  // Stability
  store.stability.mean = 5
  store.stability.std = 1
  store.stability.value = 3 + Math.random() * 4
  store.outlier = []
  for (let i = 0; i < 11; i++) {
    store.outlier.push([Math.random() * 10, Math.random() * 10])
  }

  // Cognitive
  store.cognitiveLoad = Math.floor(Math.random() * 4)
  store.vigilance = Math.random()

  // Emotion History
  let emotions = Array.from({ length: 30 }, () => {
    const row = Array.from({ length: 5 }, () => Math.random())
    const sum = row.reduce((acc, val) => acc + val, 0)
    return row.map(val => val / sum)
  })
  emotions = emotions[0].map((_, colIndex) => emotions.map(row => row[colIndex]))
  store.emotionHistory = emotions

  // Emotion
  let emotion = Array.from({ length: 5 }, () => Math.random());
  const sum = emotion.reduce((acc, val) => acc + val, 0);
  store.emotion = emotion.map(val => val / sum);
}

</script>

<template>
  <div id="header">
    <div id="headerLeftLine"></div>
    <div id="headerTitle">身心状态实时评估系统</div>
    <div id="headerRightLine"></div>
  </div>
  <div id="subjectInfo">
    <span>姓名：</span>
    <span>年龄：</span>
    <span>实验编号：</span>
    <span>实验时间：</span>
  </div>
  <div id="main">
    <div id="left" class="block">
      <div id="dataBasic">
        <DataBasic></DataBasic>
      </div>
      <div id="dataWaves">
        <DataWaves></DataWaves>
      </div>
      <div id="dataHR">
        <DataHR></DataHR>
      </div>
    </div>
    <div id="middle" class="block">
      <div id="dataCamera"></div>
      <div id="dataCognitive">
        <DataCognitive></DataCognitive>
      </div>
    </div>
    <div id="right" class="block">
      <div id="dataLog">
        <DataLog></DataLog>
      </div>
      <div id="dataEmotionHistory">
        <DataEmotionHistory></DataEmotionHistory>
      </div>
      <div id="dataEmotion">
        <DataEmotion></DataEmotion>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* h50px */
#header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 10px 0;
  height: 30px;
}

#headerTitle {
  text-align: center;
  color: white;
  font-size: 24px;
  font-weight: bold;
  margin: 0 20px;
}

#headerLeftLine,
#headerRightLine {
  flex: 1;
  height: 3px;
  background-color: aquamarine;
}

/* h40px */
#subjectInfo {
  color: white;
  font-size: 18px;
  margin-left: 20px;
  max-width: 40%;
  padding: 5px;
  height: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  border: 1px solid aquamarine;
  border-bottom: none;
  box-sizing: border-box;
}

#main {
  position: relative;
  height: calc(100vh - 90px);
  margin: 0 20px;

  display: flex;
  justify-content: space-between;

  border: 1px solid aquamarine;
  box-sizing: border-box;
}

#left #right #middle {
  height: 100%;
  box-sizing: border-box;
}

#left {
  width: 30%;
  border-right: 1px solid aquamarine;
}

#middle {
  width: 40%;
  border-right: 1px solid aquamarine;
}

#right {
  width: 30%
}

#dataBasic,
#dataWaves {
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataBasic {
  height: 33%;
}

#dataWaves {
  height: 33%;
}

#dataHR {
  height: 34%;
}

#dataCamera {
  height: 66%;
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataCognitive {
  height: 34%;
}

#dataLog,
#dataEmotionHistory {
  border-bottom: 1px solid aquamarine;
  box-sizing: border-box;
}

#dataLog {
  height: 33%;
}

#dataEmotionHistory {
  height: 33%;
}

#dataEmotion {
  height: 34%;
}
</style>
