# 📊 Housing Data Chart Generator — Visualizer

As part of a full-stack project, this is the repo for my **Python-based chart renderer**, which uses data from the **2013 American Housing Survey (AHS)** to create visual representations of housing-burden statistics.

Deployed via **GitHub Actions** and **GitHub Pages**, this automation generates **150 static pie charts** (for all 50 U.S. states × 3 metro types) and publishes an `index.html` page with links to each chart.

---
**Live site:** [https://housingdata.netlify.app](https://housingdata.netlify.app)  

**Live index page (GitHub Pages):**  
🔗 [https://jasmingg.github.io/housingdata-visualizer/](https://jasmingg.github.io/housingdata-visualizer/)

Each link routes to a chart like this:  
`/charts/virginia-suburban.svg`

---

## 🚀 Highlights

- 🐍 Python-based static chart generator
- 📈 150 charts: 50 U.S. states × 3 metro categories
- 🎨 Pie charts for housing burden distribution
- 🤖 GitHub Actions automation:
  - Generates all charts
  - Builds `index.html` with links
  - Deploys via GitHub Pages
- 📁 Output stored in `docs/` for automatic publishing

---

## 📦 Project Overview – Housing Data Platform

This project consists of three repos working together, with the other two being:

- ☕ [`housingdata-backend`](https://github.com/jasmingg/housingdata-backend)  
  Java Spring Boot API hosted on AWS Elastic Beanstalk.  
  Exposes housing burden data via `/api?state=...&metro=...`.

- 🎨 [`housingdata-frontend`](https://github.com/jasmingg/housingdata-frontend)  
  React + Vite frontend deployed on Netlify.  
  Uses a serverless function to fetch data and renders charts + stats cards.

Together, these form a lightweight full-stack visualization platform for U.S. housing burden data.
