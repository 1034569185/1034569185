#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class ParamConfigWidget; }
QT_END_NAMESPACE

class ParamConfigWidget : public QWidget
{
    Q_OBJECT
public:
    explicit ParamConfigWidget(DbManager *db, QWidget *parent = nullptr);
    ~ParamConfigWidget();

signals:
    void configSaved();

private slots:
    void onSaveClicked();
    void onBrowseBackupDirClicked();

private:
    void loadConfig();

    Ui::ParamConfigWidget *ui;
    DbManager *m_db;
};
