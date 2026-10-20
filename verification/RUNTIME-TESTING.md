# Runtime validation

Test date: **2026-10-19**. Scope: **one TANK 2 handset**.

The owner flashed the combined signed package using **SP Flash Tool v6 on Windows** and confirmed that Android started and the red provisioning overlay was absent. A subsequent full reboot completed successfully, with these values read over an authorized ADB connection:

| Property | Observed value |
| --- | --- |
| Model | `TANK2` |
| Build fingerprint | `8849/TANK2/TANK2:14/UP1A.231005.007/root.20241010.155741:user/release-keys` |
| `sys.boot_completed` | `1` |
| `ro.boot.verifiedbootstate` | `green` |
| `ro.boot.vbmeta.device_state` | `locked` |
| SIM presence | No SIM inserted |

## Original IMEI restoration and follow-up

On 2026-10-19, both original box-label IMEIs were restored using the preinstalled manufacturer IMEI Tool (`com.agui.app.imei/.IMEIActivity`). The modem returned `OK` for both writes. After a full reboot, a newly launched tool activity read the exact original values through `TelephonyManager.getImei(0)` and `getImei(1)`. The identifiers themselves remain private.

On **2026-10-20**, the handset owner additionally reported that **calls are working**. This is an owner-reported functional test; no call was placed or observed over ADB. The earlier boot/IMEI verification was performed without a SIM inserted, as shown in the table above. Mobile data has not been separately confirmed.

Persistence across reboot was verified. IMEI retention after a factory reset was not separately tested. The procedure uses modem records rather than a system-property change or a startup script. See [IMEI restoration](../docs/IMEI-RESTORATION.md).

These tests do not establish compatibility with other hardware revisions or restoration of factory attestation credentials.

The other files in this directory retain the earlier **offline build verification** results. Their `on_device_boot_verified: false` fields record that no handset boot test had been completed when those build reports were generated. The subsequent runtime observations are recorded here and summarized in the repository README.

Personal handset identifiers, device screenshots and raw device backups are excluded from the public repository.
