# Student Stress Prediction Application

A full-stack machine learning web application that predicts student stress levels based on various personal and academic factors. Built with FastAPI backend, Vue.js frontend, and containerized with Docker.

## Features

✨ **Key Capabilities:**
- 🧠 **ML Model**: K-Nearest Neighbors classifier with PCA dimensionality reduction
- 📊 **20 Input Features**: Anxiety, depression, sleep quality, academic performance, and more
- 🎯 **Real-time Predictions**: Get instant stress level predictions
- 🔄 **Auto-training**: Model trains automatically on first startup
- 🐳 **Fully Containerized**: Run anywhere with Docker
- 🌐 **REST API**: FastAPI with interactive Swagger documentation
- ⚡ **Modern Frontend**: Vue.js 3 with responsive UI
- 📱 **Stress Categories**: Low, Moderate, or High stress classification

## Project Structure

```
student-stress-prediction/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── train.py                     # Model training script
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend container config
│   ├── nginx.conf                   # Nginx configuration
│   ├── .env                         # Environment variables
│   ├── models/
│   │   ├── model.py                 # StressPredictor class
│   │   └── stress_predictor.joblib  # Trained model (auto-generated)
│   └── dataset/
│       └── StressLevelDataset.csv   # Training data
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── StressPredictor.vue  # Form component
│   │   ├── App.vue                  # Root component
│   │   ├── main.js                  # Entry point
│   │   └── style.css                # Global styles
│   ├── public/
│   │   └── favicon.svg              # App icon
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.js               # Vite configuration
│   ├── nginx.conf                   # Nginx config
│   ├── Dockerfile                   # Frontend container config
│   └── .env                         # Environment variables
├── docker-compose.yml               # Multi-container orchestration
├── run.bat                          # Windows startup script
├── run.sh                           # Linux/Mac startup script
├── .dockerignore                    # Files to exclude from Docker
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Quick Start

### Prerequisites

- **Docker** and **Docker Compose** ([Install Docker](https://www.docker.com/get-started))
- Git (optional, for cloning the repository)

### Running the Application

#### Option 1: Using Startup Scripts (Recommended)

**Windows:**
```bash
.\run.bat
```

**Linux/Mac:**
```bash
bash run.sh
```

#### Option 2: Manual Docker Compose

```bash
docker-compose up -d --build
```

### Accessing the Application

Once containers are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

## Usage

### Via Web Interface

1. Open http://localhost:5173 in your browser
2. Fill in the student stress assessment form (20 fields)
3. Click "Predict Stress Level"
4. View the prediction result (stress level and category)

### Via API

**Make a prediction request:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "anxiety_level": 5,
    "depression": 3,
    "sleep_quality": 6,
    "breathing_problem": 1,
    "noise_level": 4,
    "living_conditions": 7,
    "safety": 8,
    "basic_needs": 8,
    "academic_performance": 6,
    "study_load": 5,
    "teacher_student_relationship": 7,
    "future_career_concerns": 4,
    "social_support": 7,
    "peer_pressure": 3,
    "extracurricular_activities": 5,
    "bullying": 1,
    "self_esteem": 6,
    "mental_health_history": 2,
    "headache": 2,
    "blood_pressure": 3
  }'
```

**Check model status:**

```bash
curl "http://localhost:8000/model-status"
```

## Input Features (20 Fields)

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| anxiety_level | int | 0-10 | Student's anxiety level |
| depression | int | 0-10 | Depression symptoms |
| sleep_quality | int | 0-10 | Sleep quality rating |
| breathing_problem | int | 0-10 | Breathing difficulties |
| noise_level | int | 0-10 | Environmental noise exposure |
| living_conditions | int | 0-10 | Quality of living conditions |
| safety | int | 0-10 | Sense of safety |
| basic_needs | int | 0-10 | Access to basic needs |
| academic_performance | int | 0-10 | Academic achievement |
| study_load | int | 0-10 | Amount of studying |
| teacher_student_relationship | int | 0-10 | Relationship quality |
| future_career_concerns | int | 0-10 | Career anxiety |
| social_support | int | 0-10 | Available social support |
| peer_pressure | int | 0-10 | Peer pressure level |
| extracurricular_activities | int | 0-10 | Participation in activities |
| bullying | int | 0-10 | Bullying exposure |
| self_esteem | int | 0-10 | Self-esteem level |
| mental_health_history | int | 0-10 | Mental health background |
| headache | int | 0-10 | Frequency of headaches |
| blood_pressure | int | 0-10 | Blood pressure issues |

## Stress Level Categories

- **Low (0)**: Minimal stress, healthy stress levels
- **Moderate (1)**: Manageable stress, some concerns
- **High (2)**: Significant stress, intervention may be needed

## Machine Learning Model

### Algorithm
- **Classifier**: K-Nearest Neighbors (KNN) with k=5
- **Dimensionality Reduction**: Principal Component Analysis (PCA)
- **Variance Explained**: 95%
- **Preprocessing**: StandardScaler normalization

### Data Preprocessing Pipeline

1. **Missing Values**: Filled with median imputation
2. **Outliers**: Detected and capped using IQR method
   - Lower bound: Q1 - 1.5 × IQR
   - Upper bound: Q3 + 1.5 × IQR
3. **Feature Scaling**: StandardScaler normalization
4. **Dimensionality**: PCA reduction to 95% variance

### Model Training

The model automatically trains on first startup if `stress_predictor.joblib` doesn't exist:

```bash
# Manual retraining
docker-compose exec backend python train.py
```

## Docker Containers

### Backend Container
- **Image**: Python 3.9-slim
- **Port**: 8000
- **Services**:
  - FastAPI application
  - Model training/prediction
  - REST API endpoints

### Frontend Container
- **Image**: Nginx (Alpine)
- **Port**: 5173 (mapped to 80 internally)
- **Services**:
  - Vue.js application
  - Static file serving
  - SPA routing

## Environment Variables

### Backend (.env)
```
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```

## Stopping the Application

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Troubleshooting

### Port Already in Use

If ports 5173 or 8000 are already in use:

```bash
# Find process using port
netstat -ano | findstr :5173  # Windows
lsof -i :5173                  # Mac/Linux

# Change port in docker-compose.yml
```

### Model Not Training

```bash
# Check logs
docker-compose logs backend

# Manual training
docker-compose exec backend python train.py

# Verify dataset exists
ls backend/dataset/StressLevelDataset.csv
```

### Frontend Not Loading

```bash
# Hard refresh browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Check frontend logs
docker-compose logs frontend

# Rebuild containers
docker-compose up -d --build
```

### CORS Errors

Backend is configured to accept requests from `http://localhost:5173`. If accessing from different origin, update `main.py`:

```python
origins = [
    "http://localhost:5173",
    "http://your-domain.com",  # Add your domain
]
```

## API Endpoints

### POST /predict

**Request:**
```json
{
  "anxiety_level": 5,
  "depression": 3,
  ...
  "blood_pressure": 3
}
```

**Response:**
```json
{
  "stress_level": 1,
  "stress_category": "Moderate"
}
```

### GET /model-status

**Response:**
```json
{
  "model_loaded": true
}
```

## Development

### Local Development (Without Docker)

1. **Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
```

2. **Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

### Building for Production

```bash
# Build optimized frontend
npm run build

# Build Docker images for production
docker-compose build

# Run with production settings
docker-compose up -d
```

## Performance Metrics

- **Model Training Time**: ~1-2 seconds
- **Prediction Latency**: <100ms
- **API Response Time**: <500ms
- **Frontend Load Time**: <1 second

## Technologies Used

**Backend:**
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Scikit-learn 1.3.0
- Pandas 2.0.3
- NumPy 1.24.3
- Joblib 1.3.1
- Pydantic 2.3.0

**Frontend:**
- Vue.js 3
- Vite
- CSS3

**DevOps:**
- Docker
- Docker Compose
- Nginx

**Python Version:** 3.9

## File Sizes

- Trained Model: ~50KB
- Dataset: ~1MB
- Frontend Build: ~100KB

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review FastAPI docs: https://fastapi.tiangolo.com/
3. Check Vue.js docs: https://vuejs.org/

## Acknowledgments

- Dataset: StressLevelDataset.csv
- Machine Learning: Scikit-learn community
- Web Framework: FastAPI and Vue.js communities

---

**Last Updated**: October 16, 2025
**Version**: 1.0.0
