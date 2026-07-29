# LPU Learner's Hub

Student services dashboard for Lyceum of the Philippines University – Laguna.

## Live site

Works with:

- GitHub Pages project URL: `https://norielgecolea.github.io/lpu-student-hub/`
- Custom domain (recommended): root of your domain, e.g. `https://your-domain.edu.ph/`

The production build uses `base-href=/` so assets load correctly on a custom domain.

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
4. Add your **Custom domain** (if using one) and enable **Enforce HTTPS** after DNS is verified.
5. Push to `main` (or run the **Deploy to GitHub Pages** workflow manually).

### Custom domain DNS tip

Point your domain/subdomain to GitHub Pages:

- Apex domain: `A` records to GitHub Pages IPs, or `ALIAS`/`ANAME` if supported
- Subdomain: `CNAME` record to `norielgecolea.github.io`

## Service links

| Service | URL |
| --- | --- |
| LMS | https://lms.lpulaguna.edu.ph |
| MIS Helpdesk | https://helpdesk.lpulaguna.com |
| Office 365 | https://office.com |
| Student Portal | https://students.lpulaguna.edu.ph/Student/Login.php |
| Reservation | https://reservation.lpulaguna.com |
