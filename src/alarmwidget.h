#pragma once

#include <QWidget>
#include <QList>
#include <QTreeWidgetItem>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class AlarmWidget; }
QT_END_NAMESPACE

class AlarmWidget : public QWidget
{
    Q_OBJECT
public:
    explicit AlarmWidget(DbManager *db, QWidget *parent = nullptr);
    ~AlarmWidget();

private slots:
    void onQueryClicked();
    void onExportPDFClicked();
    void onPrevPageClicked();
    void onNextPageClicked();
    void onTableCellChanged(int row, int col);
    void onTreeItemChanged(QTreeWidgetItem *item, int column);

private:
    void populateDeviceTree();
    QList<int> checkedDeviceIds() const;
    void populateTable();

    Ui::AlarmWidget *ui;
    DbManager *m_db;
    QList<AlarmRecord> m_allRecords;
    int m_currentPage;
    int m_totalPages;
};
