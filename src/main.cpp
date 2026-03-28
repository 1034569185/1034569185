#include "mainwindow.h"
#include <QApplication>
#include <QLocale>
#include <QTranslator>
#include <QFont>
#include <QDir>
#include <QStandardPaths>
#include <QFile>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    app.setApplicationName("HongRuanTempHumidity");
    app.setApplicationVersion("2022.0516.3.1");
    app.setOrganizationName("Guangzhou HongRuan Information Technology Co.,Ltd");
    app.setOrganizationDomain("hongruan.com");

    // Set Chinese font for Kylin Linux
    QFont font;
    font.setFamily("Noto Sans CJK SC");
    font.setPointSize(10);
    app.setFont(font);

    // Load translation (if available)
    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "HongRuanTempHumidity_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }

    // Load QSS skin from QSS-Skin-Builder package
    QFile skinFile(":/skin/blue.css");
    if (skinFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        app.setStyleSheet(QString::fromUtf8(skinFile.readAll()));
        skinFile.close();
    }

    MainWindow w;
    w.show();

    return app.exec();
}
