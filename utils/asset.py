# 资源或比较长的字符串

import os
import base64
import tkinter as tk


def GetHelpConfigText():
    return f"""
【添加多国语言】

https://github.com/hiroi-sora/Umi-OCR#下载

1. 在以上网址找到 [Umi-OCR 多国语言识别扩展包] ，按提示操作，快捷导入5种语言：繁中,日文,韩文,德文,法文。

2. 英文无需添加，所有语言均支持识别英文字母。

3. 更多小语种，参考上述网页中的说明。识别引擎PaddleOCR支持80种语言。


【启动参数说明】

1. 在“设置”选项卡中编辑启动参数。

2. 若图片中的文字方向不是正朝上，启动参数添加：
--cls=1 --use_angle_cls=1

3. 若要处理的图片的分辨率极大(4K以上)，图中小字无法识别，启动参数添加：
--limit_side_len=压缩阈值
压缩阈值建议填图片的最大边长的一半，如2000。值越大，识别小字的准确率可能提高，但速度会大幅降低，请谨慎使用。

4. 若软件初始化识别引擎时频繁报错或崩溃，且电脑CPU是早期AMD型号，启动参数尝试添加：
--enable_mkldnn=0
禁用mkldnn加速可能提高对早期AMD的兼容性，但识别速度会大幅降低。Intel和AMD锐龙系列一般不存在这个问题。

5. 若电脑的CPU大于8核16线程，启动参数添加：
--cpu_threads=线程
线程建议填CPU线程数，如16。值越大，识别速度可能提高。不应超过CPU线程数。

6. 以上启动参数可以叠加，用空格隔开，如：
--cls=1 --use_angle_cls=1 --limit_side_len=2000 --cpu_threads=20
"""


def GetHelpText(website="详见GitHub项目主页"):
    return f"""
欢迎使用【Umi-OCR 批量图片转文字工具】

本软件用于批量导入图片，识别图片中的文本，输出到软件面板或本地文件。
除了能识别普通图片，本软件还有忽略指定区域的特殊功能，防止提取到图片中的水印文本。


【批量识别本地图片】

1. 点击切换到“处理列表”选项卡。将任意图片/文件夹拖入白色表格区域。

2. 点击右上角“开始任务”，等待进度条走完。

3. 在“识别内容”查看输出文字，或者前往 [第一张图片的目录] 查看识别结果txt文件。


【识别剪贴板中的图片】

1. 按 [Win+Shift+S] 截取一张系统截图，或者在网页等地方复制一张图片。

2. 切换到“识别内容”选项卡，点击“剪贴板读取”。

3. 可以在“设置”选项卡中录制并启用全局快捷键，快速唤起程序识别。


【忽略水印】

1. 切换到“设置”选项卡，点击“添加区域”，打开新窗口。

2. 将任一张有水印的图片拖入新窗口。稍等一会。

3. 窗口里显示的图片中，虚线框出来的区域是软件识别到的文字区域。若不想要它，点击“+忽略区域 A”，按住左键将它框起来。可框选多个区域。

4. 点击完成，返回主窗口。然后正常“开始任务”即可。

{GetHelpConfigText()}

【更多功能说明】

{website}
"""


# 所有资源的最终目录
_dirList = [
    'asset/icon'
]
# 图标资源
_ImageDict = {
    'umiocr64': {  # 主图标 64像素
        'path': 'asset/icon/umiocr64.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAJ5WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMi0wMy0yOFQyMzozNTo0NSswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMi0wMy0yOFQyMzo1ODo0MiswODowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjItMDMtMjhUMjM6NTg6NDIrMDg6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjQzM2E3MWZhLTU2MzMtZDU0OS05MDgyLTExYWJmNzBiNzdmMyIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjlkYTQzZTIzLWZhZGUtN2E0Yi05ZjViLWNlYWFmOWI3MzJhMSIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjk3MGVhOTdjLTAyODctZDA0OC1iNGIxLWIwYWVhNTNkZTU0MyIgcGhvdG9zaG9wOkNvbG9yTW9kZT0iMyI+IDx4bXBNTTpIaXN0b3J5PiA8cmRmOlNlcT4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNyZWF0ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6OTcwZWE5N2MtMDI4Ny1kMDQ4LWI0YjEtYjBhZWE1M2RlNTQzIiBzdEV2dDp3aGVuPSIyMDIyLTAzLTI4VDIzOjM1OjQ1KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjYxYmFiZjcxLWE3ZjktNjQ0Zi1hMmMxLTBjODIxNGZlMGJlNyIgc3RFdnQ6d2hlbj0iMjAyMi0wMy0yOFQyMzo1NjozOCswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo0N2M2MTViZC1jZDFmLTY0NDMtOTE0Yi1lMWQyODVkNGM5MzYiIHN0RXZ0OndoZW49IjIwMjItMDMtMjhUMjM6NTg6NDIrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE5IChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY29udmVydGVkIiBzdEV2dDpwYXJhbWV0ZXJzPSJmcm9tIGFwcGxpY2F0aW9uL3ZuZC5hZG9iZS5waG90b3Nob3AgdG8gaW1hZ2UvcG5nIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJkZXJpdmVkIiBzdEV2dDpwYXJhbWV0ZXJzPSJjb252ZXJ0ZWQgZnJvbSBhcHBsaWNhdGlvbi92bmQuYWRvYmUucGhvdG9zaG9wIHRvIGltYWdlL3BuZyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NDMzYTcxZmEtNTYzMy1kNTQ5LTkwODItMTFhYmY3MGI3N2YzIiBzdEV2dDp3aGVuPSIyMDIyLTAzLTI4VDIzOjU4OjQyKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjQ3YzYxNWJkLWNkMWYtNjQ0My05MTRiLWUxZDI4NWQ0YzkzNiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDo5NzBlYTk3Yy0wMjg3LWQwNDgtYjRiMS1iMGFlYTUzZGU1NDMiIHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo5NzBlYTk3Yy0wMjg3LWQwNDgtYjRiMS1iMGFlYTUzZGU1NDMiLz4gPHBob3Rvc2hvcDpUZXh0TGF5ZXJzPiA8cmRmOkJhZz4gPHJkZjpsaSBwaG90b3Nob3A6TGF5ZXJOYW1lPSLmlociIHBob3Rvc2hvcDpMYXllclRleHQ9IuaWhyIvPiA8L3JkZjpCYWc+IDwvcGhvdG9zaG9wOlRleHRMYXllcnM+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Ans7MQAAGntJREFUeNrlm3mYnFW95z/nvFttvS/pJCRmDyFAghAgyD5AEpSRJaMii4jkzr0i4HPHua44Lo+jONergsMAl4gSFXS4wdFAWAQMJiwJITvZO+mku9Nbddde9a5n/qgl1ZUO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'
    },
    'screenshot24': {  # 截屏 24像素
        'path': 'asset/icon/screenshot24.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF0WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTA5LTIxVDE5OjA2OjQxKzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0wOS0yMlQwMDowOTozMSswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMi0wOS0yMlQwMDowOTozMSswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MjMzNTYzZWUtZmYwZC1hYTQ0LThjZmYtZTVkNDcwMTRiZDVkIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ZDQyODI5OTQtZjRiNS1hYTQyLTljZjktOTlmZDhmZGUxNzQzIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6YWZmYzU3MDUtZmIxNC0xYjRlLTliM2ItN2M2ODJmODg1NzI3Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDphZmZjNTcwNS1mYjE0LTFiNGUtOWIzYi03YzY4MmY4ODU3MjciIHN0RXZ0OndoZW49IjIwMjItMDktMjFUMTk6MDY6NDErMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE5IChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MjMzNTYzZWUtZmYwZC1hYTQ0LThjZmYtZTVkNDcwMTRiZDVkIiBzdEV2dDp3aGVuPSIyMDIyLTA5LTIyVDAwOjA5OjMxKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+wLygzAAAASJJREFUSA1j+P//PwMtMTIIAeJSBhqC1UD8lhYGsyJZ8ArKZgdiLjIxJxCzIFvQDMT/qYynI1tgDMSxQHwaiD9B4yIFiNNIxKlA7A81Yy+2oFoOxC+pEOQngfgsNokVSHFACThFigXJ0DCdRysLNkAtAAUdEy0s0Abiy9BIp4kPCIF1QOxLqQVCSJkRGaRBg28xJRbIQQ15DsTWSOKiQPwNKgeiBcm1YD9aDgWlcS8g3ocmnkyOBTkkFA1HSLWAG4i/klj+aBNjAXJRwURBUXEGm8R8IP4DxLpAbAultaAuw4dhakB61ID4OhDfAmJ9IFZBtqCVBsX2RGQLQElNA+oKVTIwyLXMQHwJiK9AKx8RWtSQoAg+T8u6vRyIK+E8WjdbAFjmKfslN4pFAAAAAElFTkSuQmCC'
    },
    'paste24': {  # 粘贴 24像素
        'path': 'asset/icon/paste24.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAADzElEQVR42rVVW0iTYRjWfzp3WShBdSMUiCibp3lC8ewEc9M5zek8zc0tE2XztNSddHbhTbd1U0QoRUURgWtgV0aE5mmWSBAZWCGZRF1nzzv+X37Xv7mCLh7e7/+/73uf9/S9b9TBwUGUEJxOZzS3Hh0djR0aGjoFGSe0Hw5HFDocjhhARJL+2Wy2E0ajsVgul2+kpaXtQm4ZDAbFyMhIAu3zz4ciDMk8NjYWm5mZuSmVSr9A+VeCTCbbAz4D28PDwycj8gDsDC0GBwfPVFRU3CouLvaVlZV58/PzF9PT03dAJAm+hP/vcnJyVuhcUVGRr6qq6ga8jRcksNvtsbTAwSe49Eqj0YzV1dXZFQrF9dTU1J+9vb3y/v5+aV9fnwxShm9ZSkrKt5KSkhmcc9fX17uysrLeVFZW3vZ4PCLoi6OwHRIgdgEPsrOzVxFfNZ8dFt6ly9jbAAKSvuHlI/45nU7XAgOfhwpRgC03N3exvb1dT1aMj48HqqWnpyezpaXF3NraaoISkmbIS52dnVq9Xt/a1tZmQBF0wpAHIH/f3d2t6+joaIMs5XvAEbzGZge30dzcbExOTv5BxAjdMgd8L0OZnyqLlX78W0LOXtIaZ1Zxb7+mpuZqWAK4PK9UKj2RVEowoEabkZGxFZagtLR0rra21jE1NcUgcWLKFZ1lJSP0jXCLEWIGuWxArtaOI/CqVCrXv3jQ1dXVCIL1sAQow2dUrrQuKCiYpwrCmXVgIxh5eXlrlBOU9k2WoAkE/mMJECInrVFdKlSQFlXTBGh5aMJeI9CA/Ytms7mI54H/v4WIzYE/4hChBL0IwQpKcIkt1UX0qWVYrpyYmIihdkIvGO9HMjk5KWJDtB5xiPC7GeEwQqEBCEiExGixWM4JeWAymS78UUVkHS7+dYgwIyQg1+DFt+Nx6skYvJ9pvIPNI92U3CYPqI7hNsP3AK6L2b7PIYaaJK1RYV609G2EcQVreu3+xMTEA+qwRzxAjNehX8drdE/hgZsdLCIh69Hi49Fxv1ut1vPcPxAt4O59l8sVA4ioXYtpo7q6eho9ZA8t4gWwgJa8j9ZtESLgphfGaAKs38WEO4t/YmoPhYWFPtqDcpqQ0YeXQMQgcdCpsWq12stI0lu1Wm1je7yYbQsBUIjIuoGBgdOYdDtIdhI1PCif45RzRoRMHnLg43IQCphiElj9ASP0E2bEY9Y7JuRMplBQLVNtY1JdwcWPmFR3ysvLZwUwg0q7l5SU9AvyIWs5Ezz8w5YgKuEavUiav8BaEFYJUD5LZ91udyDmwTp+A0jzrU5GLXU+AAAAAElFTkSuQmCC'
    },
    'openfile24': {  # 打开文件 24
        'path': 'asset/icon/openfile24.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF0WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTA5LTIyVDAwOjIwOjM5KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0wOS0yMlQwMDoyNjoxOCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMi0wOS0yMlQwMDoyNjoxOCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NzI3YmRjZjMtY2FlMy1jZTQ2LWIxZjUtMjAyNDgwYTg4ZjA1IiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6NTM3ZDUxMDctZWU4ZS1kZDQzLWE4ZjMtMGI5Mjg5YjA3MDA4IiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6NTMxZGI3NjMtZjYwMC1mMjRhLThhYTgtYzQ0YmE4ZWM0NzM0Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo1MzFkYjc2My1mNjAwLWYyNGEtOGFhOC1jNDRiYThlYzQ3MzQiIHN0RXZ0OndoZW49IjIwMjItMDktMjJUMDA6MjA6MzkrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE5IChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NzI3YmRjZjMtY2FlMy1jZTQ2LWIxZjUtMjAyNDgwYTg4ZjA1IiBzdEV2dDp3aGVuPSIyMDIyLTA5LTIyVDAwOjI2OjE4KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+TbqGxQAAAdZJREFUSMfVljFLw0AUxw8d+gEEwaGxGDBpkzZpEoJ+ABFBBMXZXZyEuigUUUEd/AIOCoLaCo5FFGcnQR2cdfQb2C3+3/FSYqBp2tjBwo8kl7v3u7x7d1QEQSCGiRi6oFKpCNM0N8EVaIDrGNR2ChQgDMOg/l0pl8uyT7FYlFDDGl4EKXgplUr9C9B4xwFWgA9mYnjggvpgoDqI4IYFuYSBE9znGRyAwy4cgX0I3KigwYMnk2YGPlOmUoJ05imlNLDJjfkegjGggekEVLDH8eZpXFSg9BCkZZnjeR0BchYgX6O0QHieysguxUP5z1E8WvUmchVomubj/qOfPCeBWG2wIKsIN4FlWY9kBido2wH1AdlmSNQiwSUbv3Fth7WccR1yLKjTw1nk026ptIiMgg2ONxsXrNMu7LVb4yC98kwLr2h74p0/Ehfo4aC0EkqnqqpCURRJoVCgdqqiV9d1RVTwRZ0JmkXadaCJoAI7X4D02lQseFfTdf2X4LqfmUcF1WpV+L4vPM8TjuPUOD1OeFSccxUtZakeOtj4OH9jgQgFLf6CVWCYg/8MpMmiPYXg72GxkGDrr3Yvz5wWeDGsKLKMw3rMX/KQkXukpW7btlwPWUX//l/FD82Iu83xp20BAAAAAElFTkSuQmCC'
    },
    'delete24': {
        'path': 'asset/icon/delete24.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAQ1JREFUSEvd1bEuBFEUxvHfvoQCT6BSUClYpY6EhkKhoVUqJTRCNJ5AFCodUVFJiFbnATQKL0BOMpfsZmZ2duxtdtpz7vnf+33nnOnI/HUy1zfegD1M1Ej4XRN7wn3EqyTaxCUeWno0iRdslQFmEDc4xElLwDyeMV0GeMQHNloWT8dCwm4/4ByLWMbnqAHbuMAa7kqKx43Cm6sito7rGh97XjBbuH6Ms4qbp4I7+CqKr+KmIr8HEC31jt0BsiRIpK3gdkAb/3rQBrCP06aAYSRawFQh0QGOmkgUOU1MnsNrn8ndioEcuk2XSgrFUL41fUHKyzpoAcm+KgKSddklqbKu63+uob/j4/3LHIlMP+4uRs8NPn1iAAAAAElFTkSuQmCC'
    },
    'clear24': {
        'path': 'asset/icon/clear24.png',
        'base64': r'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAQBJREFUSEvtlcsNwjAQRF/6oAYoAVIARyiCGzQANAA3ioAjBQAlQA30ARopi4yJ7SQCBSRWihQ7m5md/dgZaVsB04DbGpjFILIEfhc4A8eA3wDoAZcQTopAAAdgCSw8kHmxl0cCQAQC0XMLRCFgEfgm/7JvLs7JCBTlJyw3AgPvO7KbEFo6HzXza1Apr5GCv9QrRaDamCkqW7vv+m7rRgTuT1YrdY6vtrTjqihojUAtKhU2B29X8PsEjYqckl2li56OD7+L/gRK4felSN1yKiLzi6zh0l3hnkW1FNQ5sm2S2yUYAdvYHZuQJBVjYGd+/hx0gA0wrJMbx3cPTICr7d0BtpOY2Yca2/wAAAAASUVORK5CYII='
    },
    # 'pass': {
    #     'path': 'asset/icon/openfile24.png',
    #     'base64': r''
    # },
}


class ASSET():
    def initRelease(self):
        '''释放资源到本地'''
        for dir in _dirList:  # 创建目录
            if not os.path.isdir(dir):
                os.makedirs(dir)
        for im in _ImageDict.values():  # base64保存图片到本地
            if not os.path.isfile(im['path']):
                with open(im['path'], 'wb') as f:
                    f.write(base64.b64decode(im['base64']))

    def initTK(self):
        for im in _ImageDict.values():
            im['tk'] = tk.PhotoImage(file=im['path'])

    def getImgTK(self, name):
        '''获取名为name的tk图片'''
        return _ImageDict[name]['tk']


Asset = ASSET()
