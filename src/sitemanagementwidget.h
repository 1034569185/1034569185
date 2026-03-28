#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class SiteManagementWidget; }
QT_END_NAMESPACE

class SiteManagementWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SiteManagementWidget(DbManager *db, QWidget *parent = nullptr);
    ~SiteManagementWidget();

private slots:
    void onSiteSelected(int row, int col);
    void onAddSiteClicked();
    void onDeleteSiteClicked();
    void onConnectSiteClicked();
    void onSaveSiteClicked();

private:
    void loadSites();

    Ui::SiteManagementWidget *ui;
    DbManager *m_db;
    int m_selectedSiteId;
};
