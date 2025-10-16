<template>
  <div class="stress-predictor">
    <h1>Student Stress Level Predictor</h1>
    
    <!-- API Key Configuration Warning -->
    <div v-if="!apiConfigured" class="api-warning">
      <h2>⚠️ API Configuration Required</h2>
      <p>The application cannot generate AI recommendations because the Groq API key is not configured.</p>
      <p><strong>To enable recommendations:</strong></p>
      <ol>
        <li>Sign up at <a href="https://console.groq.com" target="_blank">https://console.groq.com</a></li>
        <li>Get your API key</li>
        <li>Add it to <code>backend/.env</code> file:
          <pre>GROQ_API_KEY=your_key_here</pre>
        </li>
        <li>Restart the application: <code>docker-compose restart backend</code></li>
      </ol>
      <p>Without this, the app can still predict stress levels but won't provide personalized recommendations.</p>
    </div>
    
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

      <button type="submit" :disabled="loading || !modelLoaded" class="submit-button">
        {{ loading ? 'Predicting...' : 'Predict Stress Level' }}
      </button>
      
      <p v-if="!modelLoaded" class="info-text">⏳ Loading model... Please wait.</p>
    </form>

    <div v-if="prediction" class="prediction-result">
      <h2>Prediction Result</h2>
      <p>Stress Level: <strong>{{ prediction.stress_category }}</strong></p>
      
      <div v-if="prediction.recommendations" class="recommendations">
        <h3>Personalized Recommendations</h3>
        <div class="recommendations-content">
          {{ prediction.recommendations }}
        </div>
      </div>
      
      <div v-else-if="!apiConfigured" class="info-message">
        <p>Recommendations are not available because the Groq API is not configured. Only stress level prediction is available.</p>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

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
const apiConfigured = ref(false)
const modelLoaded = ref(false)

// Check API status on component mount
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/model-status')
    const data = await response.json()
    modelLoaded.value = data.model_loaded || false
    apiConfigured.value = data.groq_api_configured || false
  } catch (err) {
    console.error('Failed to check model status:', err)
    modelLoaded.value = false
    apiConfigured.value = false
  }
})

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

.api-warning {
  background-color: #fff3cd;
  border: 2px solid #ffc107;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  color: #856404;
}

.api-warning h2 {
  color: #ff6b6b;
  margin-top: 0;
  margin-bottom: 10px;
}

.api-warning ol {
  margin: 10px 0;
  padding-left: 20px;
}

.api-warning li {
  margin: 8px 0;
}

.api-warning code {
  background-color: #f1f3f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  color: #495057;
}

.api-warning pre {
  background-color: #f1f3f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 8px 0;
}

.api-warning a {
  color: #0066cc;
  text-decoration: none;
}

.api-warning a:hover {
  text-decoration: underline;
}

.info-text {
  text-align: center;
  color: #6c757d;
  font-size: 14px;
  margin-top: 10px;
}

.info-message {
  background-color: #e7f3ff;
  border-left: 4px solid #2196F3;
  padding: 15px;
  border-radius: 4px;
  margin-top: 15px;
  color: #1565c0;
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

.recommendations {
  margin-top: 20px;
  text-align: left;
}

.recommendations h3 {
  color: #2c3e50;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.recommendations-content {
  background-color: #ffffff;
  padding: 15px;
  border-left: 4px solid #4CAF50;
  border-radius: 4px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
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