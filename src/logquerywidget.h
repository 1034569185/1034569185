#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class LogQueryWidget; }
QT_END_NAMESPACE

class LogQueryWidget : public QWidget
{
    Q_OBJECT
public:
    explicit LogQueryWidget(DbManager *db, QWidget *parent = nullptr);
    ~LogQueryWidget();

private slots:
    void onQueryClicked();
    void onPresetChanged(int index);
    void onPrevPageClicked();
    void onNextPageClicked();

private:
    void populateTable();

    Ui::LogQueryWidget *ui;
    DbManager *m_db;
    QList<SystemLog> m_allLogs;
    int m_currentPage;
    int m_totalPages;
    static const int PAGE_SIZE = 50;
};
