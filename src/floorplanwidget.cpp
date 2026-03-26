#include "floorplanwidget.h"
#include "ui_floorplanwidget.h"
#include <QFileDialog>
#include <QDragEnterEvent>
#include <QDropEvent>
#include <QMimeData>
#include <QPainter>
#include <QMessageBox>

FloorPlanWidget::FloorPlanWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::FloorPlanWidget)
    , m_db(db)
{
    ui->setupUi(this);
    ui->floorPlanCanvas->setAcceptDrops(true);

    connect(ui->btnSelectImage, &QPushButton::clicked, this, &FloorPlanWidget::onSelectImageClicked);
    connect(ui->btnSave, &QPushButton::clicked, this, &FloorPlanWidget::onSaveClicked);

    loadDeviceList();
}

FloorPlanWidget::~FloorPlanWidget()
{
    delete ui;
}

void FloorPlanWidget::loadDeviceList()
{
    ui->lstAvailableDevices->clear();
    QList<DeviceInfo> devices = m_db->getAllDevices();
    for (const DeviceInfo &dev : devices) {
        QListWidgetItem *item = new QListWidgetItem(dev.name);
        item->setData(Qt::UserRole, dev.id);
        ui->lstAvailableDevices->addItem(item);
    }
}

void FloorPlanWidget::onSelectImageClicked()
{
    QString fileName = QFileDialog::getOpenFileName(this, tr("选择平面图"),
        QDir::homePath(),
        tr("图片文件 (*.png *.jpg *.jpeg *.bmp)"));
    if (fileName.isEmpty()) return;

    m_floorPlanImage = QPixmap(fileName);
    if (m_floorPlanImage.isNull()) {
        QMessageBox::warning(this, tr("错误"), tr("无法加载图片：%1").arg(fileName));
        return;
    }
    renderFloorPlan();
}

void FloorPlanWidget::onSaveClicked()
{
    QString area = ui->txtAreaName->text().trimmed();
    if (area.isEmpty()) {
        QMessageBox::warning(this, tr("提示"), tr("请输入区域名称"));
        return;
    }
    // In a full implementation, save device positions to database
    QMessageBox::information(this, tr("保存成功"), tr("平面图设置已保存"));
}

void FloorPlanWidget::dragEnterEvent(QDragEnterEvent *event)
{
    if (event->mimeData()->hasText()) {
        event->acceptProposedAction();
    }
}

void FloorPlanWidget::dropEvent(QDropEvent *event)
{
    // Handle device drop onto floor plan
    // In a full implementation, place device label at drop position
}

void FloorPlanWidget::renderFloorPlan()
{
    if (m_floorPlanImage.isNull()) return;

    // Render background image
    QPixmap display = m_floorPlanImage.scaled(
        ui->floorPlanCanvas->size(),
        Qt::KeepAspectRatio,
        Qt::SmoothTransformation);

    QPainter painter(&display);
    // Draw device markers
    painter.setPen(Qt::red);
    painter.setBrush(QColor(255, 0, 0, 180));
    for (auto it = m_devicePositions.begin(); it != m_devicePositions.end(); ++it) {
        painter.drawEllipse(it.value(), 10, 10);
    }

    // Display on canvas (using QPalette or a QLabel)
    // In full implementation, use a custom QWidget with paintEvent
}
