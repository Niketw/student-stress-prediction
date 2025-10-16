<template>
  <div class="results-container">
    <div class="results-wrapper">
      <!-- Header -->
      <header class="results-header">
        <h1>Your Stress Assessment Results</h1>
      </header>

      <!-- Main Result Card -->
      <div v-if="result" :class="['result-card', resultClass]">
        <div class="result-icon">
          <svg v-if="stressLevel === 0" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <!-- Green smiley face -->
            <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="3"/>
            <circle cx="35" cy="40" r="4" fill="currentColor"/>
            <circle cx="65" cy="40" r="4" fill="currentColor"/>
            <path d="M 30 60 Q 50 70 70 60" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round"/>
          </svg>
          <svg v-else-if="stressLevel === 1" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <!-- Yellow neutral face -->
            <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="3"/>
            <circle cx="35" cy="40" r="4" fill="currentColor"/>
            <circle cx="65" cy="40" r="4" fill="currentColor"/>
            <line x1="30" y1="60" x2="70" y2="60" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
          </svg>
          <svg v-else viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <!-- Red worried face -->
            <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="3"/>
            <circle cx="35" cy="40" r="4" fill="currentColor"/>
            <circle cx="65" cy="40" r="4" fill="currentColor"/>
            <path d="M 30 65 Q 50 55 70 65" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round"/>
          </svg>
        </div>

        <div class="result-content">
          <h2 class="result-title">{{ result.category }}</h2>
          <p class="result-description">{{ stressDescription }}</p>
          <div class="result-score">Stress Score: {{ stressLevel }}/2</div>
        </div>
      </div>

      <!-- Recommendations Section -->
      <div v-if="result && result.recommendations" class="recommendations-section">
        <h3 class="recommendations-title">📋 Personalized Recommendations</h3>
        <div class="recommendations-content">
          <div v-html="formattedRecommendations" class="markdown-content"></div>
        </div>
      </div>

      <!-- Form Data Summary -->
      <div class="form-summary">
        <h3 class="summary-title">Your Assessment Summary</h3>
        <div class="summary-grid">
          <div v-for="(value, field) in result.formData" :key="field" class="summary-item">
            <span class="summary-label">{{ formatFieldName(field) }}</span>
            <div class="summary-bar">
              <div class="summary-fill" :style="{ width: (value / 10 * 100) + '%' }"></div>
            </div>
            <span class="summary-value">{{ value }}/10</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button @click="retakeAssessment" class="btn btn-primary">📝 Retake Assessment</button>
        <button @click="downloadReport" class="btn btn-secondary">📥 Download Report</button>
      </div>

      <footer class="results-footer">
        <p>For immediate support, please contact a mental health professional.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Import marked for markdown parsing
const marked = window.marked || ((text) => `<pre>${text}</pre>`)

const router = useRouter()

const result = ref(null)
const stressLevel = ref(0)

const stressDescriptions = {
  0: 'You have a low stress level. Keep up your healthy habits and maintain the positive factors in your life!',
  1: 'You have moderate stress. Consider implementing some stress management techniques to improve your well-being.',
  2: 'You have high stress levels. Please consider reaching out to a mental health professional for support.'
}

const resultClass = computed(() => {
  const classes = ['low-stress', 'medium-stress', 'high-stress']
  return classes[stressLevel.value] || 'low-stress'
})

const stressDescription = computed(() => {
  return stressDescriptions[stressLevel.value] || 'Unable to determine stress level'
})

const formattedRecommendations = computed(() => {
  if (!result.value?.recommendations) return ''
  try {
    return marked(result.value.recommendations)
  } catch (err) {
    console.error('Error parsing markdown:', err)
    return `<pre>${result.value.recommendations}</pre>`
  }
})

const formatFieldName = (field) => {
  return field
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

onMounted(() => {
  const storedResult = sessionStorage.getItem('stressResult')
  if (storedResult) {
    result.value = JSON.parse(storedResult)
    stressLevel.value = result.value.prediction
  } else {
    router.push('/')
  }
})

const retakeAssessment = () => {
  sessionStorage.removeItem('stressResult')
  router.push('/')
}

const downloadReport = () => {
  if (!result.value) return

  const reportContent = `
STRESS ASSESSMENT REPORT
Generated: ${new Date().toLocaleString()}

OVERALL STRESS LEVEL: ${result.value.category}
Score: ${stressLevel.value}/2

ASSESSMENT DETAILS:
${Object.entries(result.value.formData)
  .map(([field, value]) => `${formatFieldName(field)}: ${value}/10`)
  .join('\n')}

RECOMMENDATIONS:
${result.value.recommendations}

---
This report was generated by the Student Stress Prediction Application.
For professional help, please consult a mental health specialist.
  `.trim()

  const blob = new Blob([reportContent], { type: 'text/plain' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `stress-report-${new Date().toISOString().slice(0, 10)}.txt`
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}
</script>

<style scoped>
.results-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.results-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  width: 100%;
  overflow: hidden;
}

.results-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
}

.results-header h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
}

.result-card {
  padding: 40px;
  display: flex;
  gap: 30px;
  align-items: center;
  border-left: 6px solid;
  margin: 20px;
  border-radius: 8px;
  background: #f9f9f9;
}

.result-card.low-stress {
  border-left-color: #4caf50;
  background: rgba(76, 175, 80, 0.05);
}

.result-card.medium-stress {
  border-left-color: #ff9800;
  background: rgba(255, 152, 0, 0.05);
}

.result-card.high-stress {
  border-left-color: #f44336;
  background: rgba(244, 67, 54, 0.05);
}

.result-icon {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
  color: #667eea;
}

.result-icon svg {
  width: 100%;
  height: 100%;
}

.result-card.low-stress .result-icon {
  color: #4caf50;
}

.result-card.medium-stress .result-icon {
  color: #ff9800;
}

.result-card.high-stress .result-icon {
  color: #f44336;
}

.result-content {
  flex: 1;
}

.result-title {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
}

.result-description {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}

.result-score {
  font-size: 18px;
  font-weight: 600;
  color: #667eea;
}

.recommendations-section {
  padding: 40px;
  border-top: 1px solid #eee;
}

.recommendations-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.recommendations-content {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.markdown-content {
  line-height: 1.8;
  color: #333;
}

.markdown-content p {
  margin: 12px 0;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
  color: #2c3e50;
  margin-top: 20px;
  margin-bottom: 10px;
}

.markdown-content ul,
.markdown-content ol {
  margin: 12px 0;
  padding-left: 30px;
}

.markdown-content li {
  margin: 8px 0;
}

.markdown-content strong {
  color: #667eea;
  font-weight: 600;
}

.markdown-content code {
  background: #f1f1f1;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
}

.form-summary {
  padding: 40px;
  border-top: 1px solid #eee;
}

.summary-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-label {
  font-size: 13px;
  font-weight: 600;
  color: #2c3e50;
}

.summary-bar {
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.summary-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s;
}

.summary-value {
  font-size: 12px;
  color: #999;
}

.action-buttons {
  display: flex;
  gap: 15px;
  padding: 40px;
  border-top: 1px solid #eee;
}

.btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
}

.btn-secondary {
  background: #f5f5f5;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.results-footer {
  background-color: #f5f5f5;
  padding: 20px;
  text-align: center;
  font-size: 13px;
  color: #999;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .results-container {
    padding: 10px;
  }

  .result-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .result-icon {
    width: 80px;
    height: 80px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
