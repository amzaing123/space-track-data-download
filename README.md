# space-track-data-download
下载  https://www.space-track.org/auth/login 网站公开的tle文件
space track tle download
一个账号只能下载300，每下载完成一次，改变读取文件的id，改变文件夹，改变账号和密码。
每下载29等待60s（更改时间可能导致下载为空），代码设置一次下载300个，一次下载约为10分钟。

下载准备
1：需下载payload或debris的id存入payload3.xlsx。
2：多注册几个账号。
3：下载命令
'curl --cookie cookies.txt '
        'https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/{}/'
        'orderby/TLE_LINE1%20ASC/EPOCH/2025-01-01--2025-03-12/format/tle '
        '> "{}"'
{}为所下载的id，还可以修改下载时间范围内的tle文件。
