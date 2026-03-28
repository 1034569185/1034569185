#pragma once

#include <QDialog>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class LoginDialog; }
QT_END_NAMESPACE

class LoginDialog : public QDialog
{
    Q_OBJECT
public:
    explicit LoginDialog(DbManager *db, QWidget *parent = nullptr);
    ~LoginDialog();

    QString username() const;
    int permissions() const;

private slots:
    void onLoginClicked();

private:
    Ui::LoginDialog *ui;
    DbManager *m_db;
    QString m_username;
    int m_permissions;
};
