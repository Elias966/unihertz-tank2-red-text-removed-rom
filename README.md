# Tank 2 firmware — provisioning watermark removed

A community firmware package for the **Unihertz / 8849 TANK 2**, based on **TANK2_20241010 (Android 14, MT6789)**. It removes the red TEE / Google / CSR provisioning-status text from the screen while retaining Android Verified Boot verification.

**[Download the firmware release](https://github.com/Elias966/unihertz-tank2-red-text-removed-rom/releases/tag/v1.0.0)** · [Verification results](verification/AVB-COMPLETE-VERIFICATION.txt) · [File manifest](https://github.com/Elias966/unihertz-tank2-red-text-removed-rom/blob/main/firmware/manifest.json)

## Tested status

| Item | Result |
| --- | --- |
| Flashing tool | **SP Flash Tool v6 on Windows** |
| Device | One TANK 2 handset |
| Android startup | Successful; subsequent reboot also completed |
| Red provisioning overlay | Removed, confirmed on the test handset |
| Verified Boot | Device reported `green` and `locked` after reboot |
| Offline AVB verification | Complete signature, hash and hash-tree chain passed |
| Original IMEI restoration | Both original handset IMEIs restored with the built-in tool and matched after reboot |
| Cellular calls | Working, confirmed by the handset owner on 2026-10-20 |
| Mobile data | Not separately confirmed |

SP Flash Tool v6 was the only tool that accepted this package in the maintainer's testing. Other flashing tools, SP Flash Tool versions, operating systems and hardware revisions have not been validated. This package is for **TANK 2**, not TANK 2 Pro or another Tank model.

## Download and extract

The full firmware is distributed under **Releases**, rather than stored in Git history.

1. Open the [v1.0.0 release](https://github.com/Elias966/unihertz-tank2-red-text-removed-rom/releases/tag/v1.0.0).
2. Download **every** file beginning `TANK2_20241010_watermark_removed_v1.0.0.7z.` and `SHA256SUMS.txt` into the same directory. Keep the numbered filenames unchanged.
3. Check the downloaded parts against `SHA256SUMS.txt`. In PowerShell, `Get-FileHash .\TANK2_20241010_watermark_removed_v1.0.0.7z.* -Algorithm SHA256` prints their hashes. On Linux, use `sha256sum -c SHA256SUMS.txt`.
4. Use 7-Zip to extract the **`.7z.001`** file. It will read the remaining parts automatically.

Extraction produces one `new-tank-firmware` folder. All stock and modified images are together with their original filenames and the scatter files. Keep this structure intact. GitHub's automatically generated **Source code** ZIP/TAR downloads contain the documentation and verification metadata, **not the firmware images**.

With Python 3.11 or newer installed, the extracted package can also be checked before flashing:

```powershell
cd new-tank-firmware
py verify_files.py
```

The script checks package file sizes, SHA-256 hashes, metadata signatures and the original root-key match. It is an offline verifier and does not flash the phone. The recorded full AVB-chain verification is in `verification/`.

## Install with SP Flash Tool v6

Back up your data and any device-specific NVRAM/NVDATA or calibration backups before flashing. Use the complete package from this release; do not mix it with images from another build.

1. Extract the complete release on the Windows computer running **SP Flash Tool v6**.
2. Load `new-tank-firmware\download_agent\flash.xml` in the tool. If its interface requests the files separately, select `MT6789_Android_scatter.xml` and `download_agent\DA_BR.bin` from this same package.
3. Choose **Download Only**. Keep the supplied partition selections:

   | Selected partition | Image |
   | --- | --- |
   | `boot_a` | `boot.img` |
   | `vendor_boot_a` | `vendor_boot.img` |
   | `dtbo_a` | `dtbo.img` |
   | `vbmeta_a` | `vbmeta.img` |
   | `vbmeta_system_a` | `vbmeta_system.img` |
   | `vbmeta_vendor_a` | `vbmeta_vendor.img` |
   | `super` | `super.img` |

4. Leave `userdata`, preloader, NVRAM/NVDATA and the other unselected partitions unchecked. The other original images are included for completeness.
5. Click **Download** in SP Flash Tool, fully power off the phone, then connect it by USB. This is the connection sequence used for the tested preloader-mode flash.
6. Wait for the tool's successful completion before disconnecting. Start the phone and allow time for the first boot.

**Do not select Format All + Download or Firmware Upgrade for these instructions.** Formatting can erase device-specific identities, calibration and provisioning that this generic firmware package cannot recreate. Do not relock or change bootloader settings as an installation step.

## Restore your original IMEIs after formatting

The test handset's two original IMEIs were restored using the preinstalled **IMEI Tool** (`com.agui.app.imei`). Both modem writes returned `OK`, and the tool read back the exact original values after a full reboot. The owner subsequently confirmed that **calls work**.

1. Obtain **your own handset's original IMEI1 and IMEI2** from its box or original label. Keep the SIM-slot order. No example or personal IMEI is supplied in this project.
2. On the booted phone, enable **Developer options → USB debugging**, connect it to a computer with ADB installed, and approve that computer's debugging prompt.
3. Open the manufacturer's installed tool:

   ```sh
   adb shell am start -n com.agui.app.imei/.IMEIActivity
   ```

4. Select **15 digits**. Enter the complete original IMEI1 under **SIM1** and the original IMEI2 under **SIM2**, including their final check digits. Check both values carefully, then press each field's **SAVE** button. Leave MEID unchanged; this procedure restores only the two original IMEIs.
5. Reboot the phone:

   ```sh
   adb reboot
   ```

6. After Android starts, open the tool again with the same command. Its newly populated fields must match both original label values. Do not treat a save notification alone as proof of success.
7. Insert a working SIM and test calling. Calling now works on the test handset, according to the owner's follow-up report; mobile data has not been separately confirmed.

The stock app writes the modem's identity records through its privileged Phone/RIL interface. **No IMEI was hardcoded into this ROM, no Android-property spoof was used, and no startup script reapplies it.** Persistence was demonstrated by fresh readback after reboot. Normal factory-reset retention of these IMEI records has not been separately tested; formatting identity partitions with a flashing tool can erase them again.

See the [detailed restoration and persistence notes](docs/IMEI-RESTORATION.md). Restoring the original identities is separate from removing the overlay and does not recreate factory attestation keys.

## What changed

Only three firmware image files differ from the original package:

| Image | Modification |
| --- | --- |
| `super.img` | Disables `ShowTeeWaterMarkController.showTeeWaterMark()` in `services.jar`, removes its obsolete precompiled service artifacts, and rebuilds the system hash tree and FEC data. |
| `vbmeta_system.img` | Contains the updated system verification descriptor and a valid signature. |
| `vbmeta.img` | Updates the delegated system signing key and carries a valid root signature. |

The original root AVB public key exactly matches the publicly shipped AOSP RSA2048 test key. This package uses that **same root key**, preserves the original boot and vendor child keys, and retains **AVB flags `0`**. Verification has not been disabled. The system child key is changed through the signed root delegation. This is a community modification, not an official manufacturer release.

Other stock images were compared with the original ZIP and match byte for byte. Both scatter files preserve the original partition geometry; their download selections are restricted to the OS images listed above. See [technical verification](verification/SIGNATURE-REPAIR-RESULT.json), [stock-file comparison](verification/STOCK-FILES-COMPARISON.json) and [source references](verification/SOURCE-REFERENCES.txt).

## Scope and limitations

- The change removes the displayed warning. It does **not** recreate missing TEE, Google keybox or RKP/CSR provisioning, and it makes no claim about attestation, Play Integrity or DRM certification.
- No personal IMEIs, device backups, dummy identities or replacement factory keys are included. If formatting erased your IMEI records, they require a separate restoration using **your own handset's original identifiers**. Flashing this package does not perform that restoration.
- A normal Android factory reset is expected to retain the firmware change because it leaves the system image intact. Reinstalling the original firmware restores its original overlay behavior. Factory-reset retention has not been separately tested.
- A successful flash does not guarantee compatibility with another hardware revision. If the device fails to boot, keep the exact error text and tool log; do not attempt to fix it with Format All.

## Provenance

Base archive: `2024110900_g88v89c2k_dfl_tee.zip`

Base SHA-256: `385e1b15dd2ea78a0a9c50f49819ad87efa080fb38c167054392ece9c3ddbc35`

The package includes the original download agent, scatter configuration, stock companion images, file checksums and verification reports. It does not bundle the SP Flash Tool program. Manufacturer binaries and other upstream components retain their respective ownership and license terms.

For reports, include the exact device model, original build, SP Flash Tool version and error text. **Do not post IMEIs, serial numbers, personal backups or account credentials in public issues.**
