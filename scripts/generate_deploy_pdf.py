#!/usr/bin/env python3
"""Generate Ubuntu deployment guide PDF for LPU Student Hub."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos


OUT = Path(__file__).resolve().parents[1] / "docs" / "ubuntu-deploy-guide.pdf"


class GuidePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "LPU Learners Hub - Ubuntu Deployment Guide", align="L")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def text_block(self, h, text, **kwargs):
        self.multi_cell(0, h, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, **kwargs)

    def section_title(self, number: int, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 55, 110)
        self.ln(4)
        self.text_block(8, f"{number}. {title}")
        self.set_draw_color(20, 55, 110)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(5)

    def body(self, text: str):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.text_block(6, text)
        self.ln(2)

    def code_block(self, code: str):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(245, 245, 248)
        self.set_text_color(25, 25, 25)
        x = self.l_margin
        w = self.epw
        lines = code.strip("\n").split("\n")
        line_h = 4.5
        pad = 4
        needed = len(lines) * line_h + pad * 2
        if self.get_y() + needed > self.h - self.b_margin:
            self.add_page()
        y0 = self.get_y()
        self.rect(x, y0, w, needed, style="F")
        self.set_xy(x + 2, y0 + pad)
        for line in lines:
            safe = line.replace("\t", "    ")
            while self.get_string_width(safe) > w - 6 and len(safe) > 10:
                safe = safe[:-1]
            self.cell(w - 4, line_h, safe)
            self.ln(line_h)
            self.set_x(x + 2)
        self.set_xy(self.l_margin, y0 + needed + 3)

    def note(self, text: str):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(80, 80, 80)
        self.text_block(5, text)
        self.ln(2)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    pdf = GuidePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 55, 110)
    pdf.text_block(10, "LPU Learners Hub")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(40, 40, 40)
    pdf.text_block(8, "Ubuntu Deployment Guide")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(70, 70, 70)
    pdf.text_block(
        6,
        "Step-by-step instructions to deploy the Student Hub on an Ubuntu server "
        "using Git, Docker, and systemd.",
    )
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.text_block(5, "Repository: https://github.com/norielgecolea/lpu-student-hub.git")
    pdf.text_block(5, "Domain: leanershub.lpulaguna.com")
    pdf.ln(4)

    pdf.note(
        "Note: This project is a static Angular app. Add Dockerfile, nginx.conf, "
        "and docker-compose.yml to the repo root before step 5 if they are not present yet."
    )

    # 1. Install Git
    pdf.section_title(1, "Install Git")
    pdf.body("Update packages and install Git:")
    pdf.code_block(
        """sudo apt update && sudo apt upgrade -y
sudo apt install -y git
git --version"""
    )

    # 2. Install Docker
    pdf.section_title(2, "Install Docker")
    pdf.body("Install Docker Engine and the Docker Compose plugin:")
    pdf.code_block(
        """sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \\
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) \\
  signed-by=/etc/apt/keyrings/docker.gpg] \\
  https://download.docker.com/linux/ubuntu \\
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \\
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \\
  docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker

sudo systemctl enable --now docker
docker --version
docker compose version"""
    )
    pdf.note("Log out and back in if docker commands still require sudo after newgrp.")

    # 3. Clone repo
    pdf.section_title(3, "Clone the Repository")
    pdf.body("Create an app directory and clone the project:")
    pdf.code_block(
        """sudo mkdir -p /opt/apps
sudo chown $USER:$USER /opt/apps
cd /opt/apps

git clone https://github.com/norielgecolea/lpu-student-hub.git
cd lpu-student-hub"""
    )
    pdf.note("For a private repo, use SSH or a personal access token with HTTPS.")

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 30, 30)
    pdf.text_block(6, "Required files in the project root")
    pdf.ln(1)
    pdf.body("Dockerfile:")
    pdf.code_block(
        """FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build:gh-pages

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/student-hub/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
    )
    pdf.body("nginx.conf:")
    pdf.code_block(
        """server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}"""
    )
    pdf.body("docker-compose.yml:")
    pdf.code_block(
        """services:
  student-hub:
    build: .
    container_name: student-hub
    restart: unless-stopped
    ports:
      - "${HOST_PORT:-8080}:80"
    env_file:
      - .env"""
    )

    # 4. Create .env
    pdf.section_title(4, "Create the .env File")
    pdf.body("Create environment settings used by Docker Compose:")
    pdf.code_block(
        """cd /opt/apps/lpu-student-hub
nano .env"""
    )
    pdf.body("Example contents:")
    pdf.code_block(
        """HOST_PORT=8080
APP_NAME=lpu-student-hub
APP_ENV=production
DOMAIN=leanershub.lpulaguna.com"""
    )
    pdf.code_block("chmod 600 .env")
    pdf.note("Keep .env out of git. It mainly controls the published host port for this static app.")

    # 5. Start as systemd service
    pdf.section_title(5, "Start Docker Compose as a Service")
    pdf.body("Create a systemd unit so the app starts on boot:")
    pdf.code_block("sudo nano /etc/systemd/system/student-hub.service")
    pdf.body("Service file contents:")
    pdf.code_block(
        """[Unit]
Description=LPU Student Hub (Docker Compose)
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/apps/lpu-student-hub
ExecStart=/usr/bin/docker compose up -d --build
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target"""
    )
    pdf.body("Enable and start the service:")
    pdf.code_block(
        """sudo systemctl daemon-reload
sudo systemctl enable --now student-hub.service
sudo systemctl status student-hub.service"""
    )
    pdf.body("Verify the app is running:")
    pdf.code_block(
        """docker compose ps
curl -I http://127.0.0.1:8080"""
    )
    pdf.body("After code updates:")
    pdf.code_block(
        """cd /opt/apps/lpu-student-hub
git pull
sudo systemctl restart student-hub.service"""
    )

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 55, 110)
    pdf.text_block(7, "Quick checklist")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(30, 30, 30)
    for item in [
        "1. Install Git",
        "2. Install Docker + Compose plugin",
        "3. Clone the repository",
        "4. Create .env",
        "5. Enable student-hub.service and confirm http://SERVER:8080",
    ]:
        pdf.text_block(6, item)

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
