SAMSUNG XPRESS M2675F — iPHONE AIRPRINT BRIDGE (Windows 11)
==========================================================
This package is a custom launcher and setup script that uses the GPL-3.0
Windows-AirPrint-Bridge engine by Salman Asmat:
https://github.com/salmanasmat/Windows-AirPrint-Bridge
The engine is downloaded during setup; this ZIP does not bundle it.

REQUIREMENTS
- Samsung Xpress M2675F connected by USB and printing from Windows 11
- PC and iPhone on the same private home LAN (Wi-Fi or Ethernet)
- Python 3.11+ installed from https://www.python.org/downloads/windows/
- Internet access for first-time setup

INSTALL
1. Extract the ZIP to a permanent folder, e.g. Documents\SamsungAirPrint.
2. In Windows, print a test page using the Samsung printer.
3. Right-click Setup.ps1 and choose Run with PowerShell. If blocked,
   open PowerShell in the extracted folder and run:
     powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup.ps1
   Only do this if you trust and have reviewed the script.
4. If firewall rule installation is declined, add an inbound Windows Defender
   Firewall rule for TCP port 631 on PRIVATE networks only.
5. Double-click Start Bridge.bat. Select your exact Samsung printer and
   click Start sharing.
6. On iPhone, connect to same home Wi-Fi. Open a photo or PDF, tap
   Share > Print > Printer, select the shared Samsung printer, and Print.

TROUBLESHOOTING
- Keep Windows awake, the app running, and the printer powered on.
- Windows network profile should be Private, not Public.
- Guest Wi-Fi / client isolation can block discovery.
- Bonjour/mDNS uses UDP 5353; allow the Python process on Private networks
  if Windows prompts. Don't open this to the internet.
- Another program using TCP 631 will prevent the engine from starting.
- Check airprint_bridge.log and bridge-console.log in this folder.
- Check the Samsung Windows driver and USB cable with a Windows test page.
- If the iPhone doesn't discover the printer, temporarily disable VPNs on
  the iPhone and PC and retry.
- The launcher stops the engine when you close its window.

SECURITY / LIMITATIONS
- Local LAN only. No user authentication; anyone on the same accessible LAN
  may be able to print. Do not use on untrusted/public networks.
- Does not provide scanning from the iPhone.
- Not tested on your actual printer or a Windows 11/iPhone combination here.
- The engine is downloaded from upstream 'main' and may change. Review it.
- Open-source upstream is GPL-3.0; see its repository for full license.
