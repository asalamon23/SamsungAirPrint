# Samsung Xpress M2675F — iPhone AirPrint Bridge (Windows 11)

**Status: experimental, not hardware-tested.** This repository builds a Windows EXE *launcher*. The actual AirPrint engine is an external open-source project, installed separately by `Setup.ps1`. Building the EXE does not prove iPhone AirPrint compatibility.

## Build with GitHub Actions
1. Create a new GitHub repository (e.g. `Samsung-AirPrint-Bridge`).
2. Upload `launcher.py`, `Setup.ps1`, `README.md`, and `.github/workflows/build-windows.yml` **preserving the folder path**. The easiest way to preserve folders is to use Git on your PC (commands below).
3. Open **Actions** > **Build Windows EXE** > **Run workflow**. Alternatively, a push to `main` triggers the build.
4. Open the completed workflow run, and under **Artifacts** download `SamsungAirPrintBridge-Windows11`.
5. Extract the artifact into a **permanent writable folder** (e.g. `%USERPROFILE%\Documents\SamsungAirPrint`). Keep `SamsungAirPrintBridge.exe` and `Setup.ps1` together.

## Set up on your PC
1. Confirm your USB-connected Samsung Xpress M2675F prints a Windows test page.
2. Install Python 3.11+ with the `py` launcher from https://www.python.org/downloads/windows/.
3. Open PowerShell in the extracted folder and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1` **after reviewing the script**. It installs Python dependencies, downloads the upstream AirPrint engine, and offers a private-network TCP 631 firewall rule.
4. Start `SamsungAirPrintBridge.exe`, choose the Windows printer, and select **Start sharing**.
5. Connect iPhone and PC to the same home LAN, then try **Share > Print > Printer**.

If no printer appears, check `bridge-console.log`, firewall rules (TCP 631 and mDNS UDP 5353), Windows Private network profile, router client isolation, and whether the upstream engine is compatible with the downloaded configuration. Keep the PC awake and the app running.

## Git commands (alternative to web upload)
```powershell
git init
git add .
git commit -m "Initial AirPrint bridge launcher"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Samsung-AirPrint-Bridge.git
git push -u origin main
```
Create an empty repository on GitHub first. Replace `YOUR_USERNAME` with your account name.

## Limitations and security
- The EXE **does not include** the upstream engine or its dependencies.
- `Setup.ps1` downloads code from the upstream `main` branch; inspect and trust the upstream project before running. Consider pinning a reviewed commit for production use.
- The engine and launcher have **not been validated** on a Samsung M2675F or an iPhone. There may be engine API/config mismatches requiring changes.
- The app does not share the scanner.
- Do not expose IPP port 631 to the public internet. Anyone on the permitted LAN may be able to send print jobs.
- Windows may show a SmartScreen warning for unsigned executables.

Upstream engine: https://github.com/salmanasmat/Windows-AirPrint-Bridge (GPL-3.0). The launcher is provided as source; check upstream license obligations before distributing a combined package.
