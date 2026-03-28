#pragma once

#include <QWidget>
#include <QTreeWidgetItem>
#include <QtCharts/QChartView>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class DataQueryWidget; }
QT_END_NAMESPACE

class DataQueryWidget : public QWidget
{
    Q_OBJECT
public:
    explicit DataQueryWidget(DbManager *db, QWidget *parent = nullptr);
    ~DataQueryWidget();

private slots:
    void onQueryClicked();
    void onExportPDFClicked();
    void onDeviceSelectionChanged();
    void onTreeItemChanged(QTreeWidgetItem *item, int column);

private:
    void populateDeviceList();
    QList<int> checkedDeviceIds() const;
    void appendCheckedDeviceIds(QTreeWidgetItem *parent, QList<int> &ids) const;
    void updateAncestorCheckState(QTreeWidgetItem *item);
    void populateTable(const QList<SensorData> &data);
    void updateCharts(const QList<SensorData> &data);

    Ui::DataQueryWidget *ui;
    DbManager *m_db;
    QChartView *m_tempChartView;
    QChartView *m_humidChartView;
};
