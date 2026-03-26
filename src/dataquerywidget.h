#pragma once

#include <QWidget>
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

private:
    void populateDeviceList();
    void populateTable(const QList<SensorData> &data);
    void updateCharts(const QList<SensorData> &data);

    Ui::DataQueryWidget *ui;
    DbManager *m_db;
};
