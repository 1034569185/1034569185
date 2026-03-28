#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class UserManagementWidget; }
QT_END_NAMESPACE

class UserManagementWidget : public QWidget
{
    Q_OBJECT
public:
    explicit UserManagementWidget(DbManager *db, QWidget *parent = nullptr);
    ~UserManagementWidget();

private slots:
    void onUserSelected(const QString &username);
    void onAddUserClicked();
    void onDeleteUserClicked();
    void onSaveClicked();
    void onAddPhoneClicked();
    void onRemovePhoneClicked();

private:
    void loadUsers();
    void showUserDetail(const UserInfo &user);

    Ui::UserManagementWidget *ui;
    DbManager *m_db;
    int m_selectedUserId;
};
