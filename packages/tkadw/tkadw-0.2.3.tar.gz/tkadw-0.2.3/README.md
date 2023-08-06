# tkadw

![PyPI](https://img.shields.io/pypi/v/tkadw?logo=python&logoColor=white&label=Version&labelColor=black&color=blue&link=https%3A%2F%2Ftest.pypi.org%2Fproject%2Ftkadw%2F)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tkadw?logo=python&logoColor=white&label=Support%20interpreter&labelColor=black)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tkadw?logo=python&logoColor=white&label=Support%20wheel&labelColor=black&color=blue)
![PyPI - License](https://img.shields.io/pypi/l/tkadw?logo=python&logoColor=white&label=License&labelColor=black&color=blue)
---

使用tkinter.Canvas、tcltk扩展自绘技术实现的扩展界面

> - `轻量`
>> 仅用`python`代码实现，不掺杂大型数据文件
> - `支持圆角`
>> 运用`DrawEngine`引擎快速画出圆角矩形
> - `跨平台`
>> `tkinter.Canvas`的跨平台性


## 安装
安装使用的途径仅在`pypi.org`平台上，所以可以直接使用`pip`
```bash
python -m pip install -U tkadw
```
`Requirement already satisfied: tkadw in $pythonpath\lib\site-packages (0.1.4)`

对于`windows`平台，安装时需勾选`tcl/tk`选项安装`tkinter`

对于`linux`平台，需自行查询`python3-tk`的安装步骤

## 包树视图
```
TKADW 源目录
├─advanced 高级包：用平台的接口实现更多扩展功能
├─canvas Canvas包：集合基本的绘画组件及额外组件库
│  ├─adwite 使用Canvas包设计的UI组件库
│  ├─atomize 使用Canvas包设计的UI组件库
│  └─fluent 使用Canvas包设计的UI组件库
└─tkite 其他根据gtk设计的UI组件库
   └─gtk 使用Canvas包设计的UI组件库

```

## Canvas组件库
`Canvas组件库`是用`tkinter.Canvas`自绘技术进行绘制实现的基础组件库

### 主题配置
我提供了一个配置主题的方法`palette`，主题设置为字典类型。

如`AdwDrawButton`的样式
```python
{
    "button": {  # 类
        "back": "#353535",  # 背景颜色
        "border": "#454545",  # 边框颜色
        "text_back": "#ffffff",  # 文字颜色
        "border_width": 1,  # 边框宽带

        "active": {  # 状态：被鼠标碰到
            "back": "#3a3a3a",  # 背景颜色
            "border": "#454545",  # 边框颜色
            "text_back": "#cecece",  # 文字颜色
            "border_width": 1,  # 边框宽带
        },

        "pressed": {  # 状态：被鼠标按下
            "back": "#2f2f2f",  # 背景颜色
            "border": "#454545",  # 边框颜色
            "text_back": "#9a9a9a",  # 文字颜色
            "border_width": 1,  # 边框宽带
        },
    }
}
```

如果想要制作基于`Canvas组件`的扩展组件，可以继承`default_palette`方法，在此会将设置为默认样式，以`GTkButton`为例

```python
from tkadw import AdwDrawRoundButton3


class GTkButton(AdwDrawRoundButton3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "button": {
                    "radius": 11,
                    "back": "#f6f5f4",
                    "border": "#ccc6c1",
                    "text_back": "#2e3436",
                    "border_width": 1.3,

                    "active": {
                        "back": "#f8f8f7",
                        "border": "#dad6d2",
                        "text_back": "#2e3436",
                        "border_width": 1.3,
                    },

                    "pressed": {
                        "back": "#dad6d2",
                        "border": "#dad6d2",
                        "text_back": "#2e3436",
                        "border_width": 1.3,
                    },
                }
            }
```


## GTk组件库
`GTk组件库`使用`tkadw.canvas`设计的UI组件库。我为每个组件都额外设计了`Dark暗黑`组件。

[![1.png](https://i.postimg.cc/nLtB97YG/QQ-20230623160308.png)](https://postimg.cc/LJNnrJWJ)

> 暂无macOS下的演示图，因为作者是个学生党，买不起苹果电脑

### GTkButton 按钮组件

#### 示例
```python
from tkinter import Tk
from tkadw import GTkButton, GTkDarkButton, GTkFrame, GTkDarkFrame

root = Tk()
root.configure(background="#1e1e1e")

frame = GTkFrame(root)

button1 = GTkButton(frame.frame, text="GTkButton")
button1.pack(fill="x", ipadx=5, padx=5, pady=5)

frame.pack(fill="both", expand="yes", side="right")

frame2 = GTkDarkFrame(root)

button2 = GTkDarkButton(frame2.frame, text="GTkDarkButton")
button2.pack(fill="x", ipadx=5, padx=5, pady=5)

frame2.pack(fill="both", expand="yes", side="left")

root.mainloop()
```

[![2.gif](https://i.postimg.cc/J05HJ4mY/2.gif)](https://postimg.cc/1V4z1S8D)

### GTkEntry 输入框组件

#### 示例
```python
from tkinter import Tk
from tkadw import GTkEntry, GTkDarkEntry, GTkFrame, GTkDarkFrame

root = Tk()
root.configure(background="#1e1e1e")

frame = GTkFrame(root)

entry1 = GTkEntry(frame.frame)
entry1.pack(fill="x", ipadx=5, padx=5, pady=5)

frame.pack(fill="both", expand="yes", side="right")

frame2 = GTkDarkFrame(root)

entry2 = GTkDarkEntry(frame2.frame)
entry2.pack(fill="x", ipadx=5, padx=5, pady=5)

frame2.pack(fill="both", expand="yes", side="left")

root.mainloop()
```

[![3.gif](https://i.postimg.cc/fbyPrJrX/3.gif)](https://postimg.cc/t10D1CyC)


### GTkTextBox 文本输入框组件

#### 示例
```python
from tkinter import Tk
from tkadw import GTkFrame, GTkDarkFrame, GTkTextBox, GTkDarkTextBox

root = Tk()
root.configure(background="#1f1f1f")

frame = GTkFrame(root)

textbox1 = GTkTextBox(frame.frame)
textbox1.pack(fill="x", ipadx=5, padx=5, pady=5)

frame.pack(fill="both", expand="yes", side="right")

frame2 = GTkDarkFrame(root)

textbox2 = GTkDarkTextBox(frame2.frame)
textbox2.pack(fill="x", ipadx=5, padx=5, pady=5)

frame2.pack(fill="both", expand="yes", side="left")

root.mainloop()
```

[![4.gif](https://i.postimg.cc/hjJdZsQN/4.gif)](https://postimg.cc/8JScjhHb)


## 更新记录
> `<=0.2.0`:
>> 作者都没记下来

> `0.2.0`:
>> `201`主题配置
> 
>> `202`改变修复`AdwDrawEntry`的`Entry`组件在`Linux`平台下出现边框
> 
>> `203`修复各别解释器类似注释的错误

> `0.2.1`
>> `211`扩充README文档
>
>> `212`新增组件`Adw`
> 
>> `213`删除多余文件

> `0.2.2` 
>> `221`扩展额外界面库`BiliBili`，根据`BiliBili桌面版`设计
> 
>> `222`修复`palette`修改完后没完全修改配色的问题
> 
>> `223`扩展额外界面库`Win11`，根据`Sunvalley`设计
> 
>> `224`修复`AdwDrawButton`类边框遮挡的问题

> `0.2.3`
>> `231` `AdwDrawEngine`添加绘画渐变图形的方法
> 
>> `232`扩展额外界面库`Fluent`，作者制作设计