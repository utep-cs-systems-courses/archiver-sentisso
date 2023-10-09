**Used out-of-band signaling:**

- **number of files** | 2B | max 65535 files
- for each file:
  - **file name length** | 1B | max 255 characters
  - **file name** | nB | n = file name length
  - **file size** | 8B | max 2^64 bytes
  - **file content** | nB | n = file size