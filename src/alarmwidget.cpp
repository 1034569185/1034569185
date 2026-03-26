#include "alarmwidget.h"
#include "ui_alarmwidget.h"
#include <QPrinter>
#include <QPainter>
#include <QFileDialog>
#include <QMessageBox>
#include <QDateTime>

AlarmWidget::AlarmWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::AlarmWidget)
    , m_db(db)
    , m_currentPage(1)
    , m_totalPages(1)
{
    ui->setupUi(this);

    QDateTime now = QDateTime::currentDateTime();
    ui->dtEndTime->setDateTime(now);
    ui->dtStartTime->setDateTime(now.addMonths(-1));

    connect(ui->btnQuery, &QPushButton::clicked, this, &AlarmWidget::onQueryClicked);
    connect(ui->btnExportPDF, &QPushButton::clicked, this, &AlarmWidget::onExportPDFClicked);
    connect(ui->btnPrevPage, &QPushButton::clicked, this, &AlarmWidget::onPrevPageClicked);
    connect(ui->btnNextPage, &QPushButton::clicked, this, &AlarmWidget::onNextPageClicked);
    connect(ui->tableAlarm, &QTableWidget::cellChanged, this, &AlarmWidget::onTableCellChanged);

    // Make last column editable (处理人/采取措施)
    ui->tableAlarm->setEditTriggers(QAbstractItemView::DoubleClicked);
}

AlarmWidget::~AlarmWidget()
{
    delete ui;
}

void AlarmWidget::onQueryClicked()
{
    m_allRecords = m_db->queryAlarmRecords(
        ui->dtStartTime->dateTime(),
        ui->dtEndTime->dateTime());
    m_currentPage = 1;
    int pageRows = ui->spinPageRows->value();
    m_totalPages = qMax(1, (m_allRecords.size() + pageRows - 1) / pageRows);
    populateTable();
}

void AlarmWidget::populateTable()
{
    int pageRows = ui->spinPageRows->value();
    int start = (m_currentPage - 1) * pageRows;
    int end = qMin(start + pageRows, m_allRecords.size());

    ui->tableAlarm->setRowCount(0);
    for (int i = start; i < end; ++i) {
        const AlarmRecord &a = m_allRecords.at(i);
        int row = ui->tableAlarm->rowCount();
        ui->tableAlarm->insertRow(row);
        ui->tableAlarm->setItem(row, 0, new QTableWidgetItem(a.alarmTime.toString("yyyy-MM-dd HH:mm:ss")));
        ui->tableAlarm->setItem(row, 1, new QTableWidgetItem(a.deviceName));
        ui->tableAlarm->setItem(row, 2, new QTableWidgetItem(a.alarmType));
        ui->tableAlarm->setItem(row, 3, new QTableWidgetItem(QString::number(a.alarmValue, 'f', 1)));
        ui->tableAlarm->setItem(row, 4, new QTableWidgetItem(QString::number(a.limitValue, 'f', 1)));
        ui->tableAlarm->setItem(row, 5, new QTableWidgetItem(
            a.recoverTime.isValid() ? a.recoverTime.toString("yyyy-MM-dd HH:mm:ss") : "-"));

        // Editable column: 处理人/采取措施
        QTableWidgetItem *remarkItem = new QTableWidgetItem(
            a.handler.isEmpty() ? a.measures : a.handler + " / " + a.measures);
        remarkItem->setData(Qt::UserRole, a.id);
        ui->tableAlarm->setItem(row, 6, remarkItem);
    }

    ui->lblTotal->setText(tr("共 %1 条记录").arg(m_allRecords.size()));
    ui->lblPageInfo->setText(tr("第 %1 页 / 共 %2 页").arg(m_currentPage).arg(m_totalPages));
    ui->btnPrevPage->setEnabled(m_currentPage > 1);
    ui->btnNextPage->setEnabled(m_currentPage < m_totalPages);
}

void AlarmWidget::onPrevPageClicked()
{
    if (m_currentPage > 1) {
        --m_currentPage;
        populateTable();
    }
}

void AlarmWidget::onNextPageClicked()
{
    if (m_currentPage < m_totalPages) {
        ++m_currentPage;
        populateTable();
    }
}

void AlarmWidget::onTableCellChanged(int row, int col)
{
    if (col != 6) return;
    QTableWidgetItem *item = ui->tableAlarm->item(row, col);
    if (!item) return;
    int alarmId = item->data(Qt::UserRole).toInt();
    QString text = item->text();
    QString handler, measures;
    int sep = text.indexOf(" / ");
    if (sep >= 0) {
        handler = text.left(sep);
        measures = text.mid(sep + 3);
    } else {
        measures = text;
    }
    m_db->updateAlarmRemark(alarmId, handler, measures);
}

void AlarmWidget::onExportPDFClicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("导出PDF"),
        QDir::homePath() + "/报警记录.pdf",
        tr("PDF文件 (*.pdf)"));
    if (fileName.isEmpty()) return;

    QPrinter printer(QPrinter::HighResolution);
    printer.setOutputFormat(QPrinter::PdfFormat);
    printer.setOutputFileName(fileName);
    printer.setPageSize(QPageSize(QPageSize::A4));
    printer.setPageOrientation(QPageLayout::Landscape);

    QPainter painter(&printer);
    QFont titleFont("SimSun", 14, QFont::Bold);
    painter.setFont(titleFont);
    painter.drawText(QRect(0, 0, printer.width(), 100), Qt::AlignCenter, tr("报警记录报表"));

    QFont dataFont("SimSun", 8);
    painter.setFont(dataFont);
    int y = 120, rowH = 50;
    int colW[] = {250, 200, 150, 80, 80, 250, 250};
    QStringList headers = {tr("报警时间"), tr("仪表名称"), tr("报警类型"),
                           tr("报警值"), tr("限值"), tr("恢复时间"), tr("处理措施")};
    int x = 0;
    QFont hFont("SimSun", 9, QFont::Bold);
    painter.setFont(hFont);
    for (int i = 0; i < headers.size(); ++i) {
        painter.drawRect(x, y, colW[i], 60);
        painter.drawText(QRect(x, y, colW[i], 60), Qt::AlignCenter, headers[i]);
        x += colW[i];
    }
    y += 60;
    painter.setFont(dataFont);
    for (const AlarmRecord &a : m_allRecords) {
        if (y + rowH > printer.height() - 100) {
            printer.newPage(); y = 50;
        }
        x = 0;
        QStringList cols = {
            a.alarmTime.toString("yyyy-MM-dd HH:mm:ss"),
            a.deviceName, a.alarmType,
            QString::number(a.alarmValue, 'f', 1),
            QString::number(a.limitValue, 'f', 1),
            a.recoverTime.isValid() ? a.recoverTime.toString("yyyy-MM-dd HH:mm:ss") : "-",
            a.handler + (a.measures.isEmpty() ? "" : " / " + a.measures)
        };
        for (int i = 0; i < cols.size(); ++i) {
            painter.drawRect(x, y, colW[i], rowH);
            painter.drawText(QRect(x+3, y, colW[i]-6, rowH), Qt::AlignVCenter, cols[i]);
            x += colW[i];
        }
        y += rowH;
    }
    painter.end();
    QMessageBox::information(this, tr("导出成功"), tr("PDF已保存到：%1").arg(fileName));
}
