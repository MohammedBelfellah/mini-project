# 🏛️ Urban Heritage Management System

<p align="center">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square" alt="License">
</p>

A comprehensive web application for managing **urban heritage buildings**, inspections, restoration interventions, documents, and related entities. Built as part of a university project at **Université Abdelmalek Essaâdi** for the **Operating Systems & Network Administration** course.

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Routes](#-api-routes)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Authors](#-authors)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 📊 Dashboard

- Real-time statistics overview
- Interactive map with building locations (Leaflet.js)
- Urgent buildings requiring immediate attention
- Restoration costs analysis by year
- Multiple map styles (satellite, dark, light, streets)

### 🏢 Buildings Management

- Full CRUD operations (Create, Read, Update, Delete)
- Advanced filtering by zone, type, protection level, and condition
- Search functionality across all building attributes
- GPS coordinates with map visualization
- Historical notes and construction dates

### 🔍 Inspections

- Track building conditions over time
- Condition states: Bon, Moyen, Dégradé, En ruine
- Detailed inspection reports
- Date-based filtering and history

### 🔧 Interventions

- Manage restoration works and projects
- Cost estimation tracking
- Status management (Planifié, En cours, Terminé, Annulé)
- Municipal validation workflow
- Link interventions to service providers

### 📁 Documents & Media

- Attach photos, plans, PDFs, videos to buildings
- Document categorization by type
- URL-based file linking (Google Drive, Dropbox, etc.)
- Gallery view for all documents

### 👥 Reference Data Management

- **Zones Urbaines**: Organize buildings by urban zones
- **Types de Bâtiment**: Categorize buildings (Religious, Civil, Military, etc.)
- **Niveaux de Protection**: Heritage protection status tracking
- **Propriétaires**: Building owners management
- **Prestataires**: Service providers (architects, contractors, etc.)

### 🎨 User Interface

- Modern Bootstrap 5 responsive design
- Sidebar navigation with active state indicators
- Flash messages for user feedback
- Confirmation modals for destructive actions
- Mobile-friendly layout

---

## 📸 Screenshots

### Dashboard with Statistics

![Dashboard](screenshots/dashboard.png)

### Interactive Map View

![Map View](screenshots/map.png)

### Buildings List with Filters

![Buildings](screenshots/buildings.png)

### Inspection Details

![Inspections](screenshots/inspections.png)



---

## 🛠️ Tech Stack

| Category        | Technology                     |
| --------------- | ------------------------------ |
| **Backend**     | Python 3.10+, Flask 2.3.3      |
| **Database**    | PostgreSQL (Neon.tech cloud)   |
| **ORM/Driver**  | psycopg 3.2.3                  |
| **Frontend**    | Bootstrap 5.3, Bootstrap Icons |
| **Maps**        | Leaflet.js 1.9.4               |
| **Templating**  | Jinja2                         |
| **Server**      | Gunicorn (production)          |
| **Environment** | python-dotenv                  |

---

## 📁 Project Structure

```
ui-app/
│
├── app/
│   ├── __init__.py          # Application factory
│   ├── db.py                 # Database connection handling
│   ├── models/               # Data models (if needed)
│   ├── routes/               # Blueprint routes
│   │   ├── __init__.py
│   │   ├── buildings.py      # Buildings CRUD
│   │   ├── inspections.py    # Inspections CRUD
│   │   ├── interventions.py  # Interventions & validation
│   │   ├── dashboard.py      # Dashboard & statistics
│   │   ├── prestataires.py   # Service providers
│   │   ├── proprietaires.py  # Building owners
│   │   ├── protections.py    # Protection levels
│   │   ├── types.py          # Building types
│   │   ├── zones.py          # Urban zones
│   │   └── documents.py      # Documents & media
│   ├── static/               # CSS, JS, images
│   └── templates/            # Jinja2 templates
│       ├── base.html         # Base layout
│       ├── dashboard/
│       ├── buildings/
│       ├── inspections/
│       ├── interventions/
│       ├── documents/
│       ├── prestataires/
│       ├── proprietaires/
│       ├── protections/
│       ├── types/
│       └── zones/
│
├── config.py                 # Configuration class
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment
├── .env                      # Environment variables (not in git)
├── .gitignore
└── README.md
```

---

## 🗄️ Database Schema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ZONE_URBAINE   │     │    BATIMENT     │     │  TYPE_BATIMENT  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id_zone (PK)    │◄────│ id_zone (FK)    │────►│ id_type (PK)    │
│ nom_zone        │     │ code_batiment   │     │ libelle_type    │
│ type_zone       │     │ nom_batiment    │     └─────────────────┘
└─────────────────┘     │ adresse_rue     │
                        │ latitude        │     ┌─────────────────┐
┌─────────────────┐     │ longitude       │     │ NIV_PROTECTION  │
│  PROPRIETAIRE   │     │ date_constr     │     ├─────────────────┤
├─────────────────┤     │ note_historique │────►│ id_protection   │
│ id_proprio (PK) │◄────│ id_proprio (FK) │     │ niveau          │
│ nom_complet     │     │ id_type (FK)    │     └─────────────────┘
│ type_proprio    │     │ id_protection   │
│ contact         │     └────────┬────────┘
└─────────────────┘              │
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   INSPECTION    │     │  INTERVENTION   │     │ DOCUMENT_MEDIA  │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id_inspect (PK) │     │ id_interv (PK)  │     │ id_doc (PK)     │
│ date_visite     │     │ date_debut      │     │ titre_doc       │
│ etat_constate   │     │ date_fin        │     │ type_doc        │
│ rapport         │     │ type_travaux    │     │ url_fichier     │
│ code_batiment   │     │ cout_estime     │     │ code_batiment   │
└─────────────────┘     │ est_validee     │     └─────────────────┘
                        │ statut_travaux  │
                        │ id_prestataire  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  PRESTATAIRE    │
                        ├─────────────────┤
                        │ id_prestataire  │
                        │ nom_entreprise  │
                        │ role_prest      │
                        └─────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database (local or cloud like Neon.tech)
- Git

### Step-by-Step Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/urban-heritage-management.git
   cd urban-heritage-management/ui-app
   ```

2. **Create virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   # Create .env file
   copy .env.example .env   # Windows
   cp .env.example .env     # Linux/macOS
   ```

5. **Configure your `.env` file**

   ```env
   DATABASE_URL="postgresql://user:password@host:5432/dbname?sslmode=require"
   SECRET_KEY="your-secure-random-secret-key"
   PORT=5000
   ```

6. **Run the application**

   ```bash
   python run.py
   ```

7. **Access the application**

   Open your browser and navigate to: `http://localhost:5000`

---

## ⚙️ Configuration

### Environment Variables

| Variable       | Description                   | Example                               |
| -------------- | ----------------------------- | ------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string  | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY`   | Flask secret key for sessions | `your-random-secret-key`              |
| `PORT`         | Application port              | `5000`                                |

### Database Setup

Create the required tables in your PostgreSQL database:

```sql
-- Run your SQL schema here or use migrations
-- Tables: BATIMENT, INSPECTION, INTERVENTION, DOCUMENT_MEDIA,
--         PRESTATAIRE, PROPRIETAIRE, ZONE_URBAINE, NIV_PROTECTION, TYPE_BATIMENT
```

---

## 📖 Usage

### Dashboard

- View overall statistics and KPIs
- Toggle between **Statistics** and **Map** views
- Identify urgent buildings requiring attention
- Analyze restoration costs by year

### Managing Buildings

1. Navigate to **Bâtiments** in the sidebar
2. Use filters to search by zone, type, protection level, or condition
3. Click **+ Ajouter** to create a new building
4. Click on a building to view details, inspections, and interventions

### Recording Inspections

1. Go to **Inspections** or access from a building's detail page
2. Select the building and date
3. Choose the condition state (Bon, Moyen, Dégradé, En ruine)
4. Add detailed notes in the rapport field

### Managing Interventions

1. Navigate to **Interventions**
2. Create new intervention linked to a building
3. Assign a service provider (Prestataire)
4. Track costs, status, and validation

---

## 🛣️ API Routes

| Blueprint     | Route                          | Methods   | Description            |
| ------------- | ------------------------------ | --------- | ---------------------- |
| Dashboard     | `/`                            | GET       | Main dashboard         |
| Buildings     | `/buildings`                   | GET       | List all buildings     |
| Buildings     | `/buildings/add`               | GET, POST | Add new building       |
| Buildings     | `/buildings/view/<id>`         | GET       | View building details  |
| Buildings     | `/buildings/edit/<id>`         | GET, POST | Edit building          |
| Buildings     | `/buildings/delete/<id>`       | POST      | Delete building        |
| Inspections   | `/inspections`                 | GET       | List inspections       |
| Interventions | `/interventions`               | GET       | List interventions     |
| Interventions | `/interventions/validate/<id>` | POST      | Validate intervention  |
| Documents     | `/documents`                   | GET       | List all documents     |
| Zones         | `/zones`                       | GET       | List urban zones       |
| Types         | `/types`                       | GET       | List building types    |
| Protections   | `/protections`                 | GET       | List protection levels |
| Propriétaires | `/proprietaires`               | GET       | List owners            |
| Prestataires  | `/prestataires`                | GET       | List service providers |

---

## 🌐 Deployment

### Heroku Deployment

1. **Install Heroku CLI** and login

   ```bash
   heroku login
   ```

2. **Create Heroku app**

   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**

   ```bash
   heroku config:set DATABASE_URL="your-database-url"
   heroku config:set SECRET_KEY="your-secret-key"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Using Gunicorn (Production)

```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

The `Procfile` is already configured for this.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👥 Authors

<table>
  <tr>
    <td align="center">
      <strong>Mohammed Belfellah</strong><br>
      <a href="mailto:mohammedbelfellah2@gmail.com">📧 Email</a>
    </td>
    <td align="center">
      <strong>Hamza Boulahrouf</strong><br>
    </td>
  </tr>
</table>

**Institution:** Université Abdelmalek Essaâdi - Faculty of Sciences and Technology, Tangier

**Course:** Operating Systems & Network Administration

**Academic Year:** 2024-2025

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Mohammed Belfellah, Hamza Boulahrouf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - UI framework
- [Leaflet.js](https://leafletjs.com/) - Interactive maps
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Neon.tech](https://neon.tech/) - Serverless PostgreSQL hosting
- [psycopg](https://www.psycopg.org/) - PostgreSQL adapter
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library

---

## 📬 Contact

For questions, suggestions, or support:

- **Email:** [mohammedbelfellah2@gmail.com](mailto:mohammedbelfellah2@gmail.com)


---

<p align="center">
  Made with ❤️ for preserving urban heritage
</p>
