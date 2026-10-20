# Restore the TANK 2's original IMEIs

This documents the procedure successfully used on the TANK2_20241010 firmware in this project. It uses the **manufacturer's preinstalled IMEI Tool**; no additional app, root access or bootloader unlock was used.

Use the two original identifiers assigned to **your own handset**, as printed on its original box or label. This guide intentionally contains no personal IMEI numbers. Flashing the ROM does not automatically restore these records.

## Procedure

1. Boot Android and obtain the complete, original **15-digit IMEI1 and IMEI2**, keeping their SIM-slot order.
2. Enable Developer options by tapping **Build number** seven times under Settings → About phone. Enable **USB debugging**, connect to a computer with ADB installed, and accept its authorization prompt.
3. Confirm the phone is authorized:

   ```sh
   adb devices
   ```

   Its status must be `device`, rather than `unauthorized`. With multiple Android devices connected, select the intended handset with `adb -s YOUR_DEVICE_SERIAL` for each command.

4. Open the built-in tool:

   ```sh
   adb shell am start -n com.agui.app.imei/.IMEIActivity
   ```

5. In **IMEI Tool**, select **15 digits**. Replace the SIM1 field with the original IMEI1 and the SIM2 field with the original IMEI2, including their check digits. Verify both entries against the label. Press the **SAVE** button for each slot. Do not change the MEID field as part of this procedure.
6. Reboot Android:

   ```sh
   adb reboot
   ```

7. After startup, unlock the phone and open IMEI Tool again using the command in step 4. The newly populated SIM1 and SIM2 fields must exactly match their original label values. A save toast or the text entered before reboot is insufficient verification.
8. Insert a working SIM and test calling. The owner confirmed working calls on the test handset after this restoration. Mobile data was not separately confirmed.

## Why the restoration persisted

The stock tool runs with the phone subsystem's privileges. Its save operation sends the OEM `AT+EGMR` write through Android's Phone/RIL interface to the modem. It does not simply change the text shown in Settings or set an Android property.

In the recorded repair:

- Both modem write requests returned **`OK`**.
- Android was fully rebooted.
- A fresh IMEI Tool activity retrieved the two values using `TelephonyManager.getImei(0)` and `TelephonyManager.getImei(1)`.
- Both values matched the handset's original label.
- On **2026-10-20**, the owner reported that **calls are working**.

This demonstrates persistence across reboot without an app or script reapplying the values. The firmware images contain no personal IMEIs. IMEI retention after a normal factory reset was not separately tested, and a flashing-tool operation that formats device identity partitions can erase the records again.

## Scope

This procedure was tested on one TANK 2 with this firmware. If the installed tool is missing, refuses the write, or does not retain the correct values after reboot, stop and keep the error details. Do not substitute random identifiers or format the phone to troubleshoot it.

The procedure does not rebuild erased RF calibration or factory TEE/Google/RKP attestation credentials. Keep device-specific backups private; do not attach identifiers, screenshots containing them or raw NVRAM/NVDATA images to public issues.

For the associated observations, see [runtime validation](https://github.com/Elias966/unihertz-tank2-red-text-removed-rom/blob/main/verification/RUNTIME-TESTING.md).
