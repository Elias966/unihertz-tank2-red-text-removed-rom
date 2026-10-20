TANK 2 / TANK2_20241010 — WATERMARK REMOVAL v1.0.0

Read README.md for the full installation and verification guide.

Tested: SP Flash Tool v6 on Windows, one TANK 2 handset.
Android boot, overlay removal and a subsequent reboot were verified.
The handset reported AVB green / locked. Calls and mobile data were not tested.

All images are together with their original filenames. Load download_agent/flash.xml,
or the XML scatter and download_agent/DA_BR.bin if requested separately.
Use DOWNLOAD ONLY and keep the supplied seven OS partition selections.
Click Download, fully power off the phone, then connect USB.
Do not use Format All + Download or Firmware Upgrade.

Modified images: super.img, vbmeta_system.img, vbmeta.img.
The complete AVB chain was verified with the same original root public key,
flags 0, regenerated system hash tree/FEC and preserved boot/vendor keys.

This change removes the warning; missing factory attestation credentials are
not recreated. No personal IMEIs, handset backups or dummy keys are included.
Device-specific identity restoration is separate from flashing this package.

Optional offline check: Python 3.11+; run python verify_files.py in this folder.
The script does not flash a phone.
