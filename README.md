# 🚀 SIMDCCO - Sistema de Diagnóstico de Saúde Mental, Clima e Cultura Organizacional

## ⚡ Quick Start

### Backend (FastAPI + PostgreSQL)

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 4. Initialize database and seed
python seed.py

# 5. Run server
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000  
📚 API Documentation: http://localhost:8000/api/docs

**Default Admin Credentials:**
- Email: `admin@simdcco.com`
- Password: `admin123` (⚠️ **CHANGE IN PRODUCTION!**)

---

### Frontend (Next.js 14)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.local.example .env.local
# Update NEXT_PUBLIC_API_URL if needed

# 4. Run development server
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## 🎯 Features Implemented

### ✅ Core System
- [x] **Backend API** (FastAPI + PostgreSQL)
  - 10 database models with relationships
  - JWT authentication with refresh tokens
  - SHA-256 hashing for sensitive data (CPF, CNPJ, email)
  - LGPD compliance (consent tracking, data deletion)
  - Comprehensive security (rate limiting, CORS, input validation)
  - Immutable audit logs

- [x] **Frontend** (Next.js 14 + TypeScript + Tailwind)
  - Premium design system (deep blue + soft green palette)
  - Fully responsive and accessible
  - Micro-animations for premium UX

### ✅ Public Pages
- [x] **Landing Page**
  - Legal authority positioning
  - Problem/solution framework
  - NR-01 compliance messaging
  - Conversion-optimized CTAs

- [x] **Legal & Compliance Page**
  - NR-01 fundamentals
  - LGPD compliance details
  - IMCO/FDAC methodology
  - Legal FAQ

### ✅ Respondent Flow
- [x] **Welcome & Validation**
  - CPF/CNPJ/Email validation
  - Department assignment
  - Session management

- [x] **LGPD Consent**
  - Full consent form
  - IP and timestamp tracking
  - User agent logging

- [x] **Interactive Questionnaire**
  - 100 questions (88 IMCO + 12 FDAC)
  - Likert scale (1-5) interface
  - Progress bar and counter
  - Question navigation (prev/next)
  - Real-time answer tracking
  - Completion validation

- [x] **Completion Page**
  - Thank you message
  - LGPD information
  - Next steps explanation

### ✅ Admin Panel
- [x] **Login Page**
  - JWT authentication
  - Secure token storage
  - Error handling

### ✅ Database
- [x] **Seeded Data**
  - 88 IMCO questions (11 vectors, 4 dimensions)
  - 12 FDAC questions (4 cultural dimensions)
  - Default admin user

---

## 📁 Project Structure

```
SIMDCCO/
├── backend/
│   ├── app/
│   │   ├── models/          # 10 SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── config.py        # Settings
│   │   ├── database.py      # DB configuration
│   │   ├── security.py      # Auth & hashing
│   │   └── main.py          # FastAPI app
│   ├── seed.py              # Database seeder
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── (public)/        # Landing, legal
│   │   ├── respondent/      # Survey flow
│   │   └── admin/           # Admin panel
│   ├── lib/
│   │   └── api.ts           # API client
│   └── package.json
└── docs/
    └── DEPLOYMENT.md        # Deployment guide
```

---

## 🔐 Security Features

- ✅ SHA-256 hashing for CPF, CNPJ, email
- ✅ JWT with access + refresh tokens
- ✅ LGPD consent tracking (IP, timestamp, user agent)
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ CORS configuration
- ✅ Immutable audit logs
- ✅ Data deletion tracking

---

## 📊 Database Schema

**10 Tables:**
1. `organizations` - Companies using the system
2. `departments` - Organizational units
3. `users` - Admin/RH/Legal users
4. `questions` - IMCO (88) + FDAC (12)
5. `consents` - LGPD consent records
6. `responses` - Survey answers (JSONB)
7. `reports` - Generated PDFs with unique numbering
8. `analytics` - Pre-calculated metrics
9. `audit_logs` - Immutable action tracking
10. `lgpd_deletions` - Data deletion records

---

## 🎨 Design System

**Colors:**
- **Primary (Blue):** Authority, trust, legal (`#0A2463`)
- **Secondary (Green):** Health, balance (`#15803D`)
- **Neutral (Graphite):** Seriousness (`#1F2937`)
- **Warning (Amber):** Attention (`#F59E0B`)
- **Danger (Red):** High risk (`#B91C1C`)

**Typography:** Inter (Google Fonts) - Modern, readable, professional

**Components:** Buttons, cards, inputs, badges, progress bars, alerts

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 📦 Deployment

See `docs/DEPLOYMENT.md` for detailed deployment instructions:
- Railway (recommended)
- Vercel (frontend)
- Docker

---

## 📋 Next Steps (Future Development)

### Phase 2: Analytics & Reports
- [ ] Analytics calculation engine
- [ ] IMCO/FDAC dashboards
- [ ] PDF report generation (ReportLab)
- [ ] Excel export

### Phase 3: Admin Panel
- [ ] Dashboard with KPIs
- [ ] Organization management
- [ ] Response viewing
- [ ] Report approval system
- [ ] LGPD data management

### Phase 4: AI/ML
- [ ] K-means clustering
- [ ] Risk prediction
- [ ] Automated recommendations

---

## 🤝 Support

- **Documentation:** `/docs`
- **API Docs:** http://localhost:8000/api/docs
- **Issues:** Open an issue in the repository
- **Email:** suporte@simdcco.com.br

---

## 📄 License

Proprietary - All rights reserved © 2026 SIMDCCO

---

## 🎯 Remember

This is not just a questionnaire.  
It's a **legal and technical tool** for **organizational mental health diagnosis**,  
created to **prove NR-01 compliance**, generate **legally defensible evidence**,  
and support **strategic and legal business decisions**.

---

**Developed with ❤️ for Brazilian companies' mental health and compliance**
