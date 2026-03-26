#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class FloorPlanWidget; }
QT_END_NAMESPACE

class FloorPlanWidget : public QWidget
{
    Q_OBJECT
public:
    explicit FloorPlanWidget(DbManager *db, QWidget *parent = nullptr);
    ~FloorPlanWidget();

private slots:
    void onSelectImageClicked();
    void onSaveClicked();

protected:
    void dragEnterEvent(QDragEnterEvent *event) override;
    void dropEvent(QDropEvent *event) override;

private:
    void loadDeviceList();
    void renderFloorPlan();

    Ui::FloorPlanWidget *ui;
    DbManager *m_db;
    QPixmap m_floorPlanImage;
    QMap<int, QPoint> m_devicePositions; // deviceId -> position on floor plan
};
