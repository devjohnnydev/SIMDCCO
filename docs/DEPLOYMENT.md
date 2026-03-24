# SIMDCCO Deployment Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your configurations:
- Database URL
- Secret keys
- SMTP settings (if using email)

### 3. Initialize Database

```bash
# Create database tables
python -c "from app.database import init_db; init_db()"

# Seed with questions and admin user
python seed.py
```

This will create:
- All database tables
- 88 IMCO questions
- 12 FDAC questions
- Admin user: `admin@simdcco.com` / `admin123` (⚠️ CHANGE PASSWORD!)

### 4. Run Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/api/docs`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:

```bash
cp .env.local.example .env.local
```

Edit to match your backend URL.

### 3. Run Frontend

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Production Deployment

### Railway (Recommended)

**Backend:**
1. Create new Railway project
2. Add PostgreSQL service
3. Add Python service from `backend/` directory
4. Set environment variables from `.env.example`
5. Build command: `pip install -r requirements.txt`
6. Start command: `python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend:**
1. Add Node service from `frontend/` directory
2. Set `NEXT_PUBLIC_API_URL` to backend URL
3. Build command: `npm run build`
4. Start command: `npm start`

### Vercel (Frontend only)

```bash
cd frontend
vercel --prod
```

Set environment variable `NEXT_PUBLIC_API_URL` in Vercel dashboard.

### Docker (Alternative)

Create `Dockerfile` in backend:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend Dockerfile:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD npm start
```

## Security Checklist

- [ ] Change default admin password
- [ ] Update `SECRET_KEY` in production
- [ ] Configure CORS properly
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure MFA for admin users
- [ ] Review SMTP credentials

## Testing

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm run test
```

## Support

For issues or questions:
- Email: suporte@simdcco.com.br
- Documentation: `/docs`
