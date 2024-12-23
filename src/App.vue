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

function dispatch_data(data) {
  if (data.hasOwnProperty('heartRate')) { store.heartRate = data.heartRate } 
  if (data.hasOwnProperty('respiration')) { store.respiration = data.respiration  }
  if (data.hasOwnProperty('leftEnergy')) { store.leftEnergy = data.leftEnergy }
  if (data.hasOwnProperty('ECG')) { store.ECG = data.ECG }
  if (data.hasOwnProperty('RESP')) { store.RESP = data.RESP }
  if (data.hasOwnProperty('EDA')) { store.EDA = data.EDA }
  if (data.hasOwnProperty('PULSE')) { store.PULSE = data.PULSE }
  if (data.hasOwnProperty('mean')) { store.mean = data.mean }
  if (data.hasOwnProperty('variance')) { store.variance = data.variance }
  if (data.hasOwnProperty('value')) { store.value = data.value }
  if (data.hasOwnProperty('corrdinates')) { store.corrdinates = data.corrdinates }
  if (data.hasOwnProperty('cognitiveLoad')) { store.cognitiveLoad = data.cognitiveLoad }
  if (data.hasOwnProperty('vigilance')) { store.vigilance = data.vigilance }
  if (data.hasOwnProperty('emotion')) { store.emotion = data.emotion }
  if (data.hasOwnProperty('emotionHistory')) { 
    store.emotionHistory = data.emotionHistory.reduce((acc, val, idx) => {
      const colIdx = idx % 5;
      if (!acc[colIdx]) acc[colIdx] = [];
      acc[colIdx].push(val);
      return acc;
    }, []);
  }
}

function connectWebSocket() {
  const socket = new WebSocket('ws://127.0.0.1:8080');

  socket.onopen = () => {
    console.log('WebSocket connection established');
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    dispatch_data(data)
    console.log(data)
    console.log(store)
  }

  socket.onclose = () => {
    console.log('WebSocket connection closed, retrying in 3 seconds...');
    setTimeout(connectWebSocket, 3000);
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
    socket.close();
  }
}

onMounted(() => {
  setInterval(() => {
    generateFakeDate(store)
  }, 3000)

  // connectWebSocket();
})

function generateFakeDate(store) {
  // Basic
  store.heartRate = Math.floor(Math.random() * 100 + 60)
  store.respiration = Math.floor(Math.random() * 20 + 10)
  store.leftEnergy = Math.random().toFixed(2)

  // Waves
  store.ECG = Array.from({ length: 100 }, () => Math.random())
  store.RESP = Array.from({ length: 100 }, () => Math.random())
  store.EDA = Array.from({ length: 100 }, () => Math.random())
  store.PULSE = Array.from({ length: 100 }, () => Math.random())

  // Stability
  store.mean = 70 + Math.random() * 10
  store.variance = 10 + Math.random() * 5
  store.value = 70 + Math.random() * 10
  store.corrdinates = []
  for (let i = 0; i < 60; i++) {
    store.corrdinates.push([Math.random() * 10, Math.random() * 10])
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
