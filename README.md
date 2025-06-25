# Space-Track TLE 批量下载说明

本指南介绍如何批量下载 [Space-Track.org](https://www.space-track.org/auth/login) 提供的 TLE（Two-Line Element）文件，规避单账号下载限制，并自动切换账号与下载参数。

---

## 1. 账号和下载限制

- 单个 Space-Track 账号每天最多下载 300 个 TLE 文件。
- 每次下载后需更换文件对应的 NORAD ID、保存文件夹及账号密码。
- 每下载 29 个，需等待 60 秒（防止因频率过高导致下载失败）。
- 每次批量下载 300 个，约需 10 分钟。

---

## 2. 下载前准备

1. **准备 TLE ID 列表：**
   - 将所需下载的 Payload 或 Debris 的 NORAD_CAT_ID 存入 `payload3.xlsx` 文件中。

2. **注册多个 Space-Track 账号：**
   - 用于轮换下载，避免单账号限制。

---

## 3. 下载命令说明

每个 TLE 文件的下载命令格式如下：

```bash
curl --cookie cookies.txt \
    "https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{ID}/orderby/TLE_LINE1%20ASC/EPOCH/2025-01-01--2025-03-12/format/tle" \
    > "{保存路径}/{ID}.tle"
```

- `{ID}` 替换为当前下载的 NORAD_CAT_ID。
- `{保存路径}` 替换为当前账号的下载文件夹。
- 可根据需要修改 EPOCH 时间范围参数。

---

## 4. 下载流程示例

1. **循环读取 payload3.xlsx 的 NORAD_CAT_ID 列表。**
2. **每次下载一个 ID 的 TLE 文件，保存到不同账号/文件夹下。**
3. **每下载 29 个，自动等待 60 秒。**
4. **每下载 300 个，自动切换账号和密码、文件夹，重置计数。**

---

## 5. 注意事项

- 下载频率过快，Space-Track 可能会返回空文件或限制账号。
- 建议定期更换账号密码及下载路径。
- 保证 `cookies.txt` 为当前账号已登录状态。

---

## 6. 扩展建议

- 可用 Python 脚本自动化上述流程，批量处理账号切换和下载。
- 推荐用 `requests` + `pandas` 读取 Excel，自动填充命令和管理计数。

---

**参考链接：**
- [Space-Track 官方文档](https://www.space-track.org/documentation)
- [TLE 数据简介](https://en.wikipedia.org/wiki/Two-line_element_set)
