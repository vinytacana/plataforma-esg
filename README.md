# Casca ESG Enterprise Platform

## Overview
The **Casca ESG Enterprise Platform** is a high-performance SaaS-ready solution designed to solve the critical problem of **unstructured and non-validated ESG (Environmental, Social, and Governance) data collection**.

In the corporate world, sustainability reporting is often fragmented, manual, and susceptible to "greenwashing." This platform provides a centralized, multi-tenant environment where organizations can calculate, track, and audit their ESG metrics with strict data isolation and technical validation.

## Key Problems Solved
- **Data Fragmentation**: Consolidates carbon emissions (GHG), water consumption, waste management, and social/governance indicators in one place.
- **Auditability Risk**: Implements a logical architecture ready for blockchain integration, ensuring each record is traceable.
- **Enterprise Scalability**: Supports Multi-tenancy (data isolation between companies) and extensible report generation via design patterns.

## Technical Architecture
- **Backend**: FastAPI (Python 3.10+) - High-performance asynchronous-ready API.
- **Security**: JWT (JSON Web Tokens) with OAuth2 Password Bearer flow and Bcrypt password hashing.
- **Persistence**: SQLAlchemy ORM with a generic multi-tenant mapping (`tenant_id`).
- **Reporting**: Extensible PDF Engine using the **Strategy Pattern** for ESG pillar modularity.
- **Frontend**: Modular Vanilla JS (ES6) with centralized API management and Chart.js for data visualization.

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Pip (Python Package Manager)

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd plataforma-esg
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the root directory (optional, uses defaults if not present):
   ```env
   SECRET_KEY=your-super-secret-key
   DB_URL=sqlite:///./esg_app.db
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

4. **Initialize Database and Start Server**:
   ```bash
   uvicorn main:app --reload
   ```
   The platform will be available at `http://127.0.0.1:8000`.

---

## Core Modules & Workflow

### 1. Registration & Authentication
- **Endpoint**: `/usuarios/registrar`
- **Workflow**: New companies must register a `tenant_id` (Unique identifier). This ID ensures that their data is isolated from other organizations.
- **Login**: Users authenticate to receive a JWT token required for all subsequent data operations.

### 2. ESG Data Tracking
The platform manages four main data silos:
- **Carbon Emissions**: Calculates Scope 1, 2, and 3 based on GHG Protocol factors (Fuel, Electricity, Travel).
- **Water Management**: Tracks consumption in cubic meters (m³) and calculates estimated costs and environmental impact.
- **Circular Economy**: Monitors waste destination (Landfill, Recycling, Composting).
- **Generic Metrics (S/G)**: A flexible key-value store for indicators like "Leadership Diversity (%)" or "Ethics Training (Hours)".

### 3. Executive Reporting
- **Architecture**: Uses a `RelatorioStrategy` pattern.
- **Action**: Generates a consolidated PDF summary (`/relatorios/executivo`) that pulls data from all modules, restricted to the logged-in company's context.

---

## Testing
The project includes a robust testing suite using `pytest`.
To run the full suite:
```bash
pytest tests/
```
Coverage includes:
- Emission/Energy calculation logic accuracy.
- API endpoint security and access control.
- Multi-tenant data isolation (ensuring Company A cannot see Company B's data).

## API Documentation
Once the server is running, interactive Swagger documentation is available at:
`http://127.0.0.1:8000/docs`
