# 🚗 Car Price Prediction API (Production-Ready)

## 📌 Overview
This project is a **production-grade Machine Learning API** built with **FastAPI** to predict used car prices. It follows **clean architecture principles**, includes **authentication, caching, monitoring, and containerization**, and is ready for real-world deployment.

---

## 🧠 ML Model

- Model Used: **LightGBM (LGBMRegressor)**
- Applied **Hyperparameter Tuning** (Random Search)
- Optimized for:
  - Low latency predictions
  - High accuracy
  - Handling tabular data efficiently

- Performance:
  - RMSE: 122,471.755
  - R² Score: 0.89

---

## 📦 Features

- 🔐 JWT Authentication + API Key validation  
- 🧠 ML Prediction using tuned LightGBM model  
- ⚡ Redis caching for performance optimization  
- 📈 Prometheus + Grafana monitoring  
- 🐳 Dockerized setup  
- ☁️ Deployment-ready (Render)  

---

## 🧱 Project Structure

```
app/
├── api/            
├── cache/          
├── core/           
├── middlewares/    
├── models/         
├── services/       
├── utils/          
├── main.py         

data/               
logs/               
notebooks/          
train/              

.env                
dockerfile          
docker-compose.yml  
prometheus.yml      
render.yml          
requirements.txt    
setup.py            
templates.py        
```

---

## ⚙️ Tech Stack

- FastAPI
- LightGBM
- Redis
- Docker
- Prometheus + Grafana

---

## 🔐 Authentication

- JWT-based authentication
- API key validation layer

---

## ⚡ Redis Caching

- Hash input → check cache  
- Cache hit → return result  
- Cache miss → compute → store → return  

---

## 📊 Input Features

| Feature | Description |
|--------|------------|
| company | Car brand |
| year | Manufacturing year |
| owner | Ownership history |
| fuel | Fuel type |
| seller_type | Seller type |
| transmission | Transmission |
| km_driven | Distance driven |
| mileage_mpg | Mileage |
| engine_cc | Engine capacity |
| max_power_bhp | Power |
| torque_nm | Torque |
| seats | Seating capacity |

---

## 🚀 Setup

### Clone
```bash
git clone https://github.com/Sumit-Prasad01/Car-Price-Prediction-API.git
```

### Environment
```
REDIS_URL=redis://redis:6379
SECRET_KEY=your_secret_key
API_KEY=your_api_key
```

### Run
```bash
docker-compose up --build
```

---

## 📡 API

### POST /predict

Headers:
```
Authorization: Bearer <token>
x-api-key: <api_key>
```

Body:
```json
{
  "company": "Maruti",
  "year": 2015,
  "owner": "Second",
  "fuel": "Petrol",
  "seller_type": "Individual",
  "transmission": "Automatic",
  "km_driven": 200000,
  "mileage_mpg": 55,
  "engine_cc": 1250,
  "max_power_bhp": 80,
  "torque_nm": 200,
  "seats": 5
}
```

---

## 📈 Monitoring

- Prometheus metrics collection  
- Grafana dashboards visualization  

---

## ☁️ Deployment

- Ready for Render deployment using `render.yml`

---
