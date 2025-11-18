🧠 MemoriAI – AI-Powered Cognitive Assistant for Alzheimer’s Care
📘 Overview

MemoriAI is an AI-powered digital companion designed to support individuals with Alzheimer’s disease and dementia.
It provides cognitive recall assistance, adaptive reminders, and a caregiver dashboard — helping patients maintain independence and enabling caregivers to monitor well-being.

The system integrates FastAPI microservices, LangChain-based AI inference, SQLite + VectorDB storage, and GitHub Actions CI/CD pipelines deployed in Azure.

🧩 Key Features

🧠 Cognitive & Identity Assist – Personalized memory recall and word-aid service

⏰ Daily Reminders & Safety Alerts – Smart reminders with adherence tracking

📊 Caregiver Dashboard – Summaries, visual insights, and adherence metrics

🔒 Security by Design – OAuth2 + JWT, RBAC, PHIPA/HIPAA compliance

⚙️ Scalable Microservices – FastAPI, Docker, and Azure App Service deployment

🏗️ System Architecture

The system follows a Service-Oriented Microservice Architecture with clear separation of concerns:

Layer	Description
Frontend	Streamlit-based caregiver dashboard (web/mobile)
Backend	FastAPI-based Cognitive, Reminder, and Dashboard microservices
Storage	SQLite (structured) + VectorDB (semantic memory)
AI Engine	LangChain + Guardrailed LLM for safe phrasing (no medical advice)
MLOps/DevOps	GitHub Actions → Docker → Azure Deployment → Monitoring (Grafana/Prometheus)

📄 See /docs/MemoriAI_Architecture_Overview_v3.docx for diagrams and design details.

🧠 Core Microservices
Service	Purpose	Key Endpoint	Auth	Latency (p95)
Cognitive Service	Memory recall, word-aid, identity questions	/api/v1/cognitive/ask	JWT	< 800 ms
Reminder Service	Scheduling and reminders	/api/v1/reminder/create	JWT	< 500 ms
Dashboard Service	Caregiver insights & summaries	/api/v1/dashboard/summary	JWT	< 600 ms
🗂️ Repository Structure
MemoriAI/
│
├── src/                # Core application code
│   ├── cognitive/      # Cognitive service (FastAPI)
│   ├── reminders/      # Reminder service
│   ├── dashboard/      # Dashboard service
│   └── auth/           # OAuth2/JWT implementation
│
├── data/               # Datasets and embeddings
├── api/                # API routes and schemas
├── tests/              # Unit tests
├── docs/               # Design & architecture documents
│   ├── MemoriAI_HLD_v2_Advanced.docx
│   ├── MemoriAI_Architecture_Overview_v3.docx
│   └── MemoriAI_Highlevel_Design.docx
│
├── .github/workflows/  # GitHub Actions CI/CD pipelines
└── README.md           # You are here

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/<your-org>/MemoriAI.git
cd MemoriAI

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate     # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

3️⃣ Run the Services
uvicorn src.cognitive.main:app --reload --port 8001
uvicorn src.reminders.main:app --reload --port 8002
uvicorn src.dashboard.main:app --reload --port 8003

4️⃣ Access the APIs

Swagger UI → http://localhost:8001/docs

Dashboard UI → http://localhost:8501

🔗 Integration Links

🧩 Azure DevOps Board: MemoriAI Project

🧠 GitHub Repository: MemoriAI Repository

📝 Approved Pull Request: PR #1 – Instructor Review

👥 Team Roles
Member	Role	Responsibilities
Tessa (Nejla Ayvazoglu)	AI Lead / Coordinator	Project coordination, Cognitive module, final documentation
Krishna Reddy Bovilla	Backend Developer	Reminder & Auth microservices
Adhitya Kondeti	DevOps Engineer	Dockerization, CI/CD, Azure setup
Bhupender Sejwal	UI/UX & GitHub Lead	Repo setup, README, documentation, PR submission
Kumari Nikitha Singh	Frontend / Dashboard Developer	Streamlit dashboard, caregiver interface
✅ Pull Request (Instructor Review)

The instructor has been granted repository access and approved one Pull Request for evaluation purposes.
This PR contains the initial repository setup, folder structure, and README documentation.

🧩 Future Enhancements

Integration with wearable sensors for activity tracking

Voice-based recall assistant (Whisper / SpeechT5)

Predictive caregiver stress analytics

Multilingual support

⚠️ Legal Notice

© 2025 Nejla (Tessa) Ayvazoglu. All Rights Reserved.
This software and all accompanying documentation are proprietary and confidential.
Unauthorized use, reproduction, or distribution is strictly prohibited.
#===>
#docker build -t tessaayv8/memoriai-assignment4:latest .
#docker run -p 8501:8501 tessaayv8/memoriai-assignment4:latest
#docker push tessaayv8/memoriai-assignment4:latest
#====>
#docker rmi tessaayv8/memoriai-assignment4:latest   # local imajı sil
#docker pull tessaayv8/memoriai-assignment4:latest  # Hub’dan tekrar çek
#docker run -p 8501:8501 tessaayv8/memoriai-assignment4:latest
#docker run -p 8501:8501 ^
#  -v D:\Doc_2025\Sebtember2025\INFO8665ML1\MemoriAI\src\logs:/app/src/logs ^
#  tessaayv8/memoriai-assignment4:latest
