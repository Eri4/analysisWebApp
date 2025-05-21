# Marketing Analytics Dashboard

A proof-of-concept web application that performs automated analysis on marketing campaign data, detects anomalies, provides AI-generated recommendations, and sends notifications for significant findings.

## Architecture

### Backend

- **Framework**: Python with FastAPI
- **Architecture**: Simple layered architecture with clear separation of concerns:
  - API Routes Layer: Handles HTTP requests and responses
  - Service Layer: Contains business logic and analysis algorithms
  - Data Access Layer: Interacts with the database
  - Schema Layer: Defines data validation models
- **Database**: PostgreSQL for storing campaign data, analysis results, and recommendations
- **AI Integration**: Mistral API for generating actionable recommendations
- **Notification**: Email service for alerts on significant findings

### Frontend

- **Framework**: React with TypeScript
- **UI Components**: shadcn/ui with Tailwind CSS
- **Data Display**: Tables with filtering capabilities
- **API Integration**: Axios for data fetching

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Docker (for running PostgreSQL)

### Database Setup

1. Start the PostgreSQL database using Docker, go to the server directory and run this:
   ```bash
   docker-compose up -d
   ```

2. Verify that the database is running:
   ```bash
   docker-compose ps
   ```

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the server directory with the following:
   ```
   MISTRAL_API_KEY=your_api_key_here
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=marketing_analytics
   SMTP_SERVER=localhost
   SMTP_PORT=1025
   EMAILS_FROM_EMAIL=alerts@marketinganalytics.com
   EMAILS_TO_EMAIL=your-email@company.com
   ```
   Note: Replace `your_api_key_here` with your Mistral API key and `your-email@company.com` with the email where notifications should be sent.

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

6. The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. The application will be available at http://localhost:5173

## Testing Email Notifications

For dev purposes, you can use this to catch and view emails instead of sending them:

   ```bash
   python -m smtpd -n -c DebuggingServer localhost:1025
   ```

## Usage

1. View marketing campaign data in the dashboard
2. Use filters to narrow down the data
3. Click "Run Analysis" to analyze the data for anomalies
4. View analysis results and recommendations
5. Email notifications are automatically sent for high-severity findings