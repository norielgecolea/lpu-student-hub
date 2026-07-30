import { Component, OnInit, signal } from '@angular/core';

type HubLink = {
  name: string;
  url: string;
  description: string;
};

type LocalNetworkRequestInit = RequestInit & {
  targetAddressSpace?: 'local' | 'loopback' | 'private' | 'public';
};

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  /** null = still checking, true/false = result */
  protected readonly internetReachable = signal<boolean | null>(null);

  protected readonly links: HubLink[] = [
    { name: 'MIS Helpdesk', url: 'https://lpul-mis.on.spiceworks.com/portal/registrations', description: 'Support and concerns' },
    { name: 'LMS', url: 'https://lms.lpulaguna.edu.ph', description: 'Learning Management System' },
    { name: 'Office 365', url: 'https://office.com', description: 'Email and productivity tools' },
    { name: 'Student Portal', url: 'https://students.lpulaguna.edu.ph/Student/Login.php', description: 'Grades, records, and profile' },
    { name: 'Reservation System', url: 'https://reservation.lpulaguna.com', description: 'Book rooms and facilities' },
    { name: 'Internet Access', url: 'http://web.lpu-laguna.edu.ph:8090', description: 'LPU Captive Portal' }
  ];

  ngOnInit(): void {
    const internet = this.links.find((link) => link.name === 'Internet Access');
    if (!internet) {
      return;
    }

    void this.checkInternetReachability(internet.url);
  }

  protected isInternetDisabled(): boolean {
    return this.internetReachable() !== true;
  }

  protected onLinkClick(event: Event, link: HubLink): void {
    if (link.name === 'Internet Access' && this.isInternetDisabled()) {
      event.preventDefault();
    }
  }

  private async checkInternetReachability(url: string): Promise<void> {
    // GitHub Pages is HTTPS; browsers block plain HTTP probes unless we declare
    // Local Network Access. Non-Chromium browsers often cannot probe at all —
    // leave the link enabled there instead of stuck off.
    if (this.isHttpsPage() && !this.canUseLocalNetworkFetch()) {
      this.internetReachable.set(true);
      return;
    }

    const reachable = await this.isReachable(url);
    this.internetReachable.set(reachable);
  }

  private isHttpsPage(): boolean {
    return globalThis.location?.protocol === 'https:';
  }

  /** Chromium implements fetch `targetAddressSpace` for local HTTP from HTTPS pages. */
  private canUseLocalNetworkFetch(): boolean {
    const chrome = (globalThis as { chrome?: unknown }).chrome;
    return typeof chrome === 'object' && chrome !== null;
  }

  /**
   * Probes the captive portal from GitHub Pages via Local Network Access.
   * `targetAddressSpace: 'local'` skips mixed-content blocking for private hosts.
   */
  private async isReachable(url: string, timeoutMs = 4000): Promise<boolean> {
    const probe = `${url}${url.includes('?') ? '&' : '?'}_=${Date.now()}`;
    const init: LocalNetworkRequestInit = {
      mode: 'no-cors',
      cache: 'no-store',
      signal: AbortSignal.timeout(timeoutMs),
      targetAddressSpace: 'local'
    };

    try {
      await fetch(probe, init);
      return true;
    } catch {
      // Retry without the annotation for HTTP-hosted deployments / older browsers.
      try {
        const { targetAddressSpace: _ignored, ...fallback } = init;
        await fetch(probe, fallback);
        return true;
      } catch {
        return false;
      }
    }
  }
}
