# 鸿软温湿度监测系统 (Qt版)

广州鸿软信息科技有限公司  
Guangzhou HongRuan Information Technology Co.,Ltd

## 项目说明

本项目是将原 Windows .NET WinForms 版本的**鸿软温湿度监测系统**移植为基于 **Qt** 的跨平台桌面应用，支持在**银河麒麟系统**（Kylin Linux）上运行。

## 技术选型

| 项目 | 说明 |
|------|------|
| UI框架 | Qt 5/6 Widgets（免费 LGPL 授权） |
| 数据库 | SQLite（通过 Qt SQL 模块） |
| 串口通信 | Qt SerialPort（RS485/RS232 Modbus RTU） |
| 图表 | Qt Charts |
| PDF导出 | Qt PrintSupport |
| 网络 | Qt Network |
| 构建系统 | CMake 3.16+ |

> **注意**：使用 Qt 开源版（LGPL 授权），无需付费。

## 系统功能

### 主界面
- 按区域分组显示所有温湿度记录仪的实时数据
- 实时温度/湿度数值显示（超限自动变红/蓝色）
- 顶部菜单栏（数据查询、系统报警、设置平面图、系统设定、切换站点、日志查询）
- 底部状态栏（公司信息、最新报警、当前时间）
- 10分钟无操作自动退出锁定

### 数据查询 (dataquerywidget.ui)
- 按时间段、仪表名称查询历史温湿度数据
- 支持全部/正常/异常数据筛选
- 数据列表、温度曲线图、湿度曲线图、统计报表四个视图
- 导出 PDF 报表

### 系统报警 (alarmwidget.ui)
- 查询报警历史记录
- 支持填写处理人和采取措施备注
- 分页显示
- 导出 PDF 报告

### 设置平面图 (floorplanwidget.ui)
- 上传区域平面图（PNG/JPG）
- 拖拽放置仪表到平面图指定位置

### 系统设定
#### 设备管理 (devicemanagementwidget.ui)
- 添加/修改/删除温湿度记录仪
- 设置仪表名称、通讯地址（1-253）、是否启用、所属区域
- 设置报警上下限（温度/湿度）
- 支持写配置到仪表 / 从仪表读配置（Modbus RTU）

#### 用户管理 (usermanagementwidget.ui)
- 新增/删除/修改用户
- 设置用户权限（数据查询、报警查询、设备管理等）
- 配置报警短信接收手机号

#### 参数配置 (paramconfigwidget.ui)
- 库名、记录间隔、报警音量等17项系统参数
- 邮件报警配置
- 数据库备份目录配置

### 切换站点 (sitemanagementwidget.ui)
- 配置多个监测站点（主机名/IP、连接ID/密码）
- 连接切换不同站点

### 日志查询 (logquerywidget.ui)
- 按时间段查询用户操作日志
- 支持服务端/界面端日志筛选
- 快速选择（最近一月/三月/半年）

## 目录结构

```
├── CMakeLists.txt              # 构建配置文件
├── src/                        # C++ 源代码
│   ├── main.cpp
│   ├── mainwindow.h/.cpp       # 主窗口
│   ├── logindialog.h/.cpp      # 登录对话框
│   ├── sensorwidget.h/.cpp     # 传感器显示小部件
│   ├── dataquerywidget.h/.cpp  # 数据查询
│   ├── alarmwidget.h/.cpp      # 系统报警
│   ├── floorplanwidget.h/.cpp  # 平面图设置
│   ├── devicemanagementwidget.h/.cpp  # 设备管理
│   ├── usermanagementwidget.h/.cpp    # 用户管理
│   ├── paramconfigwidget.h/.cpp       # 参数配置
│   ├── sitemanagementwidget.h/.cpp    # 站点管理
│   ├── logquerywidget.h/.cpp          # 日志查询
│   ├── database/
│   │   ├── dbmanager.h/.cpp    # SQLite 数据库管理
│   └── serialcomm/
│       ├── serialmanager.h/.cpp # 串口通信（Modbus RTU）
└── ui/                         # Qt Designer UI 文件（可图形化编辑）
    ├── mainwindow.ui
    ├── logindialog.ui
    ├── sensorwidget.ui
    ├── dataquerywidget.ui
    ├── alarmwidget.ui
    ├── floorplanwidget.ui
    ├── devicemanagementwidget.ui
    ├── usermanagementwidget.ui
    ├── paramconfigwidget.ui
    ├── sitemanagementwidget.ui
    └── logquerywidget.ui
```

## 编译安装

### 银河麒麟系统依赖安装

```bash
# 安装 Qt 5 开发环境（银河麒麟/Ubuntu 系）
sudo apt-get install -y \
    qt5-default \
    qtbase5-dev \
    qtbase5-dev-tools \
    libqt5sql5-sqlite \
    libqt5serialport5-dev \
    libqt5charts5-dev \
    libqt5printsupport5 \
    cmake \
    build-essential

# 或使用 Qt 6
sudo apt-get install -y \
    qt6-base-dev \
    qt6-base-dev-tools \
    libqt6sql6-sqlite \
    libqt6serialport6-dev \
    libqt6charts6-dev \
    cmake \
    build-essential
```

### 编译

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### 运行

```bash
./HongRuanTempHumidity
```

## PyQt 版本（UI 优化演示）

为便于对比 Qt C++ 版本界面，仓库新增了一个并行的 PyQt UI 演示版本（不影响原工程构建）：

```bash
cd pyqt_app
python3 -m pip install -r requirements.txt
python3 main.py
```

说明：
- 默认演示登录：任意非空用户名/密码均可进入（仅用于本地 UI 演示）
- 如需固定登录账号，可在运行前配置环境变量 `PYQT_DEMO_USERNAME`、`PYQT_DEMO_PASSWORD`
- 该版本主要用于界面风格与布局优化演示，后续可逐步接入现有数据库与串口逻辑

## UI 文件编辑

所有 `.ui` 文件位于 `ui/` 目录，可使用 **Qt Designer** 进行图形化编辑：

```bash
# 打开 Qt Designer
designer ui/mainwindow.ui
```

## 硬件接口说明

- 串口通信：支持 RS485/RS232，波特率 9600，数据位 8，无校验，停止位 1
- 通信协议：Modbus RTU
  - 读取温湿度：功能码 0x03，寄存器 0x0000-0x0001
  - 读写报警配置：功能码 0x03/0x10，寄存器 0x0010-0x0013
- 设备地址：1-253（可在设备管理中设置）

## 默认登录

| 用户名 | 密码 |
|--------|------|
| admin | admin123 |

> 首次登录后请立即修改密码。
