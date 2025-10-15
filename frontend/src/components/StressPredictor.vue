<template>
  <div class="stress-predictor">
    <h1>Student Stress Level Predictor</h1>
    
    <form @submit.prevent="predictStress" class="predictor-form">
      <div v-for="(value, field) in formData" :key="field" class="form-group">
        <label :for="field">{{ formatFieldName(field) }}</label>
        <input
          type="number"
          :id="field"
          v-model.number="formData[field]"
          min="0"
          max="10"
          required
          class="form-control"
        >
      </div>

      <button type="submit" :disabled="loading" class="submit-button">
        {{ loading ? 'Predicting...' : 'Predict Stress Level' }}
      </button>
    </form>

    <div v-if="prediction" class="prediction-result">
      <h2>Prediction Result</h2>
      <p>Stress Level: <strong>{{ prediction.stress_category }}</strong></p>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const formData = reactive({
  anxiety_level: 0,
  self_esteem: 0,
  mental_health_history: 0,
  depression: 0,
  headache: 0,
  blood_pressure: 0,
  sleep_quality: 0,
  breathing_problem: 0,
  noise_level: 0,
  living_conditions: 0,
  safety: 0,
  basic_needs: 0,
  academic_performance: 0,
  study_load: 0,
  teacher_student_relationship: 0,
  future_career_concerns: 0,
  social_support: 0,
  peer_pressure: 0,
  extracurricular_activities: 0,
  bullying: 0
})

const prediction = ref(null)
const loading = ref(false)
const error = ref(null)

const formatFieldName = (field) => {
  return field
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const predictStress = async () => {
  loading.value = true
  error.value = null
  prediction.value = null

  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Prediction failed')
    }

    prediction.value = await response.json()
  } catch (err) {
    error.value = err.message || 'Failed to get prediction. Please try again.'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.stress-predictor {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.predictor-form {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-size: 14px;
  color: #333;
}

.form-control {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.submit-button {
  grid-column: 1 / -1;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.submit-button:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.prediction-result {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.error-message {
  margin-top: 20px;
  padding: 10px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

h2 {
  margin-bottom: 10px;
  color: #2c3e50;
}

@media (max-width: 600px) {
  .predictor-form {
    grid-template-columns: 1fr;
  }
  
  .stress-predictor {
    padding: 10px;
  }
}
</style>