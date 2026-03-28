cmake_minimum_required(VERSION 3.16)
project(HongRuanTempHumidity VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOUIC_SEARCH_PATHS ${CMAKE_CURRENT_SOURCE_DIR}/ui)

# Find Qt (supports both Qt5 and Qt6)
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS
    Core Widgets Sql Network SerialPort PrintSupport Charts)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS
    Core Widgets Sql Network SerialPort PrintSupport Charts)

set(SOURCES
    src/main.cpp
    src/mainwindow.cpp
    src/logindialog.cpp
    src/dataquerywidget.cpp
    src/alarmwidget.cpp
    src/floorplanwidget.cpp
    src/devicemanagementwidget.cpp
    src/usermanagementwidget.cpp
    src/paramconfigwidget.cpp
    src/sitemanagementwidget.cpp
    src/logquerywidget.cpp
    src/sensorwidget.cpp
    src/database/dbmanager.cpp
    src/serialcomm/serialmanager.cpp
)

set(HEADERS
    src/mainwindow.h
    src/logindialog.h
    src/dataquerywidget.h
    src/alarmwidget.h
    src/floorplanwidget.h
    src/devicemanagementwidget.h
    src/usermanagementwidget.h
    src/paramconfigwidget.h
    src/sitemanagementwidget.h
    src/logquerywidget.h
    src/sensorwidget.h
    src/database/dbmanager.h
    src/serialcomm/serialmanager.h
)

set(UI_FILES
    ui/mainwindow.ui
    ui/logindialog.ui
    ui/dataquerywidget.ui
    ui/alarmwidget.ui
    ui/floorplanwidget.ui
    ui/devicemanagementwidget.ui
    ui/usermanagementwidget.ui
    ui/paramconfigwidget.ui
    ui/sitemanagementwidget.ui
    ui/logquerywidget.ui
    ui/sensorwidget.ui
)

set(RESOURCE_FILES
    resources/skin.qrc
)

add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
    ${UI_FILES}
    ${RESOURCE_FILES}
)

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src/database
    ${CMAKE_CURRENT_SOURCE_DIR}/src/serialcomm
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Widgets
    Qt${QT_VERSION_MAJOR}::Sql
    Qt${QT_VERSION_MAJOR}::Network
    Qt${QT_VERSION_MAJOR}::SerialPort
    Qt${QT_VERSION_MAJOR}::PrintSupport
    Qt${QT_VERSION_MAJOR}::Charts
)

# Install
install(TARGETS ${PROJECT_NAME}
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
