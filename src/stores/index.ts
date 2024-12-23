import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => ({
    // Basic
    heartRate: 70,
    breathingRate: 20,
    leftEnergy: 20,

    // Waves
    ECG: [],
    RESP: [],
    EDA: [],
    P: [],

    // Stability
    stability: {
      mean: 0,
      std: 1,
      value: 0.5
    },
    outlier: [],

    // Cognitive
    cognitiveLoad: 0,
    vigilance: 0,

    // Emotion History
    emotionHistory: [],

    // Emotion
    emotion: [1, 1, 1, 1, 1]
  })
})