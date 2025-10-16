<template>
  <div class="form-container">
    <div class="form-wrapper">
      <header class="form-header">
        <h1>Student Stress Assessment</h1>
        <p class="subtitle">Evaluate your stress levels across different factors</p>
      </header>

      <!-- API Key Configuration Warning -->
      <div v-if="!apiConfigured" class="api-warning">
        <h3>⚠️ API Configuration Required</h3>
        <p>The application cannot generate AI recommendations because the Groq API key is not configured.</p>
        <p><strong>To enable recommendations:</strong></p>
        <ol>
          <li>Sign up at <a href="https://console.groq.com" target="_blank">https://console.groq.com</a></li>
          <li>Get your API key</li>
          <li>Add it to <code>backend/.env</code> file</li>
          <li>Restart the application</li>
        </ol>
      </div>

      <form @submit.prevent="submitForm" class="assessment-form">
        <!-- Form Sections -->
        <div v-for="section in sections" :key="section.title" class="form-section">
          <h2 class="section-title">{{ section.title }}</h2>
          <p class="section-description">{{ section.description }}</p>

          <div v-for="field in section.fields" :key="field" class="form-field">
            <div class="field-header">
              <label :for="field" class="field-label">{{ formatFieldName(field) }}</label>
              <span class="field-value">{{ formData[field] }}/10</span>
            </div>
            <input
              type="range"
              :id="field"
              v-model.number="formData[field]"
              min="0"
              max="10"
              class="field-slider"
            >
            <div class="slider-labels">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>
        </div>

        <!-- Loading and Error States -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="!modelLoaded" class="info-message">
          ⏳ Loading model... Please wait.
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          :disabled="loading || !modelLoaded" 
          class="submit-btn"
        >
          {{ loading ? 'Analyzing...' : 'Get Stress Assessment' }}
        </button>
      </form>

      <footer class="form-footer">
        <p>Your data is processed securely and never stored.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = reactive({
  anxiety_level: 5,
  self_esteem: 5,
  mental_health_history: 5,
  depression: 5,
  headache: 5,
  blood_pressure: 5,
  sleep_quality: 5,
  breathing_problem: 5,
  noise_level: 5,
  living_conditions: 5,
  safety: 5,
  basic_needs: 5,
  academic_performance: 5,
  study_load: 5,
  teacher_student_relationship: 5,
  future_career_concerns: 5,
  social_support: 5,
  peer_pressure: 5,
  extracurricular_activities: 5,
  bullying: 5
})

const loading = ref(false)
const error = ref(null)
const modelLoaded = ref(false)
const apiConfigured = ref(false)

const sections = [
  {
    title: 'Mental Health & Emotions',
    description: 'Rate your emotional and mental health status',
    fields: ['anxiety_level', 'depression', 'self_esteem', 'mental_health_history']
  },
  {
    title: 'Physical Health',
    description: 'Assess your physical health indicators',
    fields: ['sleep_quality', 'headache', 'blood_pressure', 'breathing_problem']
  },
  {
    title: 'Academic & Studies',
    description: 'Evaluate your academic situation and workload',
    fields: ['academic_performance', 'study_load', 'future_career_concerns']
  },
  {
    title: 'Social & Environment',
    description: 'Rate your social connections and living environment',
    fields: ['social_support', 'peer_pressure', 'teacher_student_relationship', 'bullying', 'noise_level', 'living_conditions', 'safety', 'basic_needs', 'extracurricular_activities']
  }
]

const formatFieldName = (field) => {
  return field
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Check API status on mount
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

const submitForm = async () => {
  loading.value = true
  error.value = null

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

    const result = await response.json()
    
    // Store result and navigate to results page
    sessionStorage.setItem('stressResult', JSON.stringify({
      formData,
      prediction: result.stress_level,
      category: result.stress_category,
      recommendations: result.recommendations
    }))
    
    router.push('/results')
  } catch (err) {
    error.value = err.message || 'Failed to get assessment. Please try again.'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.form-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  width: 100%;
  overflow: hidden;
}

.form-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
}

.form-header h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
}

.subtitle {
  margin: 10px 0 0 0;
  font-size: 16px;
  opacity: 0.9;
}

.api-warning {
  background-color: #fff3cd;
  border: 2px solid #ffc107;
  color: #856404;
  padding: 20px;
  margin: 20px;
  border-radius: 8px;
}

.api-warning h3 {
  margin-top: 0;
  color: #ff6b6b;
}

.api-warning code {
  background-color: #f1f3f5;
  padding: 2px 6px;
  border-radius: 3px;
  color: #495057;
}

.api-warning a {
  color: #0066cc;
  text-decoration: none;
}

.assessment-form {
  padding: 40px;
}

.form-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
  border-bottom: 3px solid #667eea;
  padding-bottom: 10px;
}

.section-description {
  font-size: 14px;
  color: #666;
  margin: 0 0 25px 0;
}

.form-field {
  margin-bottom: 30px;
}

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.field-label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
}

.field-value {
  background-color: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.field-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(to right, #667eea, #764ba2);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.field-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.5);
  border: 3px solid #667eea;
  transition: all 0.2s;
}

.field-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.7);
}

.field-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.5);
  border: 3px solid #667eea;
  transition: all 0.2s;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-top: 6px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #c62828;
}

.info-message {
  background-color: #e3f2fd;
  color: #1565c0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #1565c0;
  text-align: center;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 30px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  background-color: #f5f5f5;
  padding: 20px;
  text-align: center;
  font-size: 13px;
  color: #999;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .form-container {
    padding: 10px;
  }

  .form-header {
    padding: 30px 20px;
  }

  .form-header h1 {
    font-size: 24px;
  }

  .assessment-form {
    padding: 20px;
  }

  .section-title {
    font-size: 18px;
  }
}
</style>
