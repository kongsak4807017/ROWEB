# ROWeb Player Experience Workbench

ตำแหน่งมาตรฐานของ Workbench คือ:

```text
C:\RO-WEB-V1\ROWEB\apps\workbench
```

เหตุผลที่วางที่นี่:

- แยกจาก `roBrowserLegacy` ซึ่งเป็น runtime ที่ pin ไว้
- แยกจาก `private-assets` ซึ่งห้ามเข้า Git
- อยู่ใน ROWEB ซึ่งเป็น production/control repository
- สามารถพัฒนาและ deploy เป็น static admin application ได้

## เปิดใช้งานทันที

จาก PowerShell:

```powershell
Set-Location C:\RO-WEB-V1\ROWEB\apps\workbench
py -m http.server 4173
```

เปิด:

```text
http://127.0.0.1:4173
```

Workbench รุ่นนี้เป็น interactive static MVP และยังไม่เขียนกลับไฟล์จริงใน `roBrowserLegacy` หรือ `private-assets` เพื่อป้องกันความเสียหายระหว่างออกแบบ UI profile

## หน้าที่ปัจจุบัน

- Preview หน้าจอผู้เล่น
- สลับ Desktop / Mobile Landscape / Mobile Portrait
- เลือก EP01–EP17
- เลือก Component และแก้ตำแหน่ง ขนาด scale opacity anchor
- Preview joystick และ mobile action buttons
- ตรวจ validation checklist
- จำลอง Save Draft / Validate / Publish

## จุดเชื่อม Production ที่ต้องทำต่อ

1. Persist profile เป็น JSON ใน `config/player-ui-profiles.json`
2. เพิ่ม adapter อ่านรายการ Component จาก roBrowserLegacy
3. เพิ่ม preview asset URL จาก Asset Server
4. เพิ่ม exporter สำหรับ runtime profile
5. ให้ roBrowserLegacy โหลด profile โดยไม่ hard-code layout
6. เพิ่ม authentication ก่อน deploy Workbench นอกเครื่อง local

## Boundary

Workbench จัดการ configuration และ preview เท่านั้น ไม่ควร:

- เก็บ licensed assets ใน Git
- เขียน rAthena database โดยตรง
- restart server โดยไม่มี approval
- แก้ source roBrowserLegacy อัตโนมัติจาก browser
