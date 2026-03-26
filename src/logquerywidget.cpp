#include "logquerywidget.h"
#include "ui_logquerywidget.h"

LogQueryWidget::LogQueryWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::LogQueryWidget)
    , m_db(db)
    , m_currentPage(1)
    , m_totalPages(1)
{
    ui->setupUi(this);

    QDateTime now = QDateTime::currentDateTime();
    ui->dtEndTime->setDateTime(now);
    ui->dtStartTime->setDateTime(now.addMonths(-1));

    connect(ui->btnQuery, &QPushButton::clicked, this, &LogQueryWidget::onQueryClicked);
    connect(ui->cmbPreset, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &LogQueryWidget::onPresetChanged);
    connect(ui->btnPrevPage, &QPushButton::clicked, this, &LogQueryWidget::onPrevPageClicked);
    connect(ui->btnNextPage, &QPushButton::clicked, this, &LogQueryWidget::onNextPageClicked);
}

LogQueryWidget::~LogQueryWidget()
{
    delete ui;
}

void LogQueryWidget::onPresetChanged(int index)
{
    QDateTime now = QDateTime::currentDateTime();
    switch (index) {
    case 1: // 最近一月
        ui->dtStartTime->setDateTime(now.addMonths(-1));
        ui->dtEndTime->setDateTime(now);
        break;
    case 2: // 最近三月
        ui->dtStartTime->setDateTime(now.addMonths(-3));
        ui->dtEndTime->setDateTime(now);
        break;
    case 3: // 最近半年
        ui->dtStartTime->setDateTime(now.addMonths(-6));
        ui->dtEndTime->setDateTime(now);
        break;
    default:
        break;
    }
}

void LogQueryWidget::onQueryClicked()
{
    m_allLogs = m_db->queryLogs(
        ui->dtStartTime->dateTime(),
        ui->dtEndTime->dateTime(),
        ui->chkServiceLog->isChecked(),
        ui->chkUILog->isChecked());
    m_currentPage = 1;
    m_totalPages = qMax(1, (m_allLogs.size() + PAGE_SIZE - 1) / PAGE_SIZE);
    populateTable();
}

void LogQueryWidget::populateTable()
{
    int start = (m_currentPage - 1) * PAGE_SIZE;
    int end = qMin(start + PAGE_SIZE, m_allLogs.size());

    ui->tableLog->setRowCount(0);
    for (int i = start; i < end; ++i) {
        const SystemLog &l = m_allLogs.at(i);
        int row = ui->tableLog->rowCount();
        ui->tableLog->insertRow(row);
        ui->tableLog->setItem(row, 0, new QTableWidgetItem(l.logTime.toString("yyyy-MM-dd HH:mm:ss")));
        ui->tableLog->setItem(row, 1, new QTableWidgetItem(
            l.logType == "service" ? tr("服务端") : tr("界面端")));
        ui->tableLog->setItem(row, 2, new QTableWidgetItem(l.username));
        ui->tableLog->setItem(row, 3, new QTableWidgetItem(l.operation));
        ui->tableLog->setItem(row, 4, new QTableWidgetItem(l.detail));
    }

    ui->lblTotal->setText(tr("共 %1 条记录").arg(m_allLogs.size()));
    ui->lblPageInfo->setText(tr("第 %1 页 / 共 %2 页").arg(m_currentPage).arg(m_totalPages));
    ui->btnPrevPage->setEnabled(m_currentPage > 1);
    ui->btnNextPage->setEnabled(m_currentPage < m_totalPages);
}

void LogQueryWidget::onPrevPageClicked()
{
    if (m_currentPage > 1) {
        --m_currentPage;
        populateTable();
    }
}

void LogQueryWidget::onNextPageClicked()
{
    if (m_currentPage < m_totalPages) {
        ++m_currentPage;
        populateTable();
    }
}
