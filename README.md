# LPU Learner's Hub

Student services dashboard for Lyceum of the Philippines University – Laguna.

## Live site

After GitHub Pages is enabled, the app is available at:

https://norielgecolea.github.io/lpu-student-hub/

## Development

```bash
npm install
npm start
```

Open http://localhost:4200/

## Build for GitHub Pages

```bash
npm run build:gh-pages
```

Output is written to `dist/student-hub/browser`.

## GitHub Pages setup

1. Push this repository to GitHub (`main` branch).
2. Open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to `main` (or run the **Deploy to GitHub Pages** workflow manually).

The workflow builds the Angular app with base href `/lpu-student-hub/` and deploys it automatically.

## Service links

| Service | URL |
| --- | --- |
| LMS | https://lms.lpulaguna.edu.ph |
| MIS Helpdesk | https://helpdesk.lpulaguna.com |
| Office 365 | https://office.com |
| Student Portal | https://students.lpulaguna.edu.ph/Student/Login.php |
| Reservation | https://reservation.lpulaguna.com |
