#include "sitemanagementwidget.h"
#include "ui_sitemanagementwidget.h"
#include <QMessageBox>

SiteManagementWidget::SiteManagementWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::SiteManagementWidget)
    , m_db(db)
    , m_selectedSiteId(-1)
{
    ui->setupUi(this);
    connect(ui->tableSites, &QTableWidget::cellClicked, this, &SiteManagementWidget::onSiteSelected);
    connect(ui->btnAddSite, &QPushButton::clicked, this, &SiteManagementWidget::onAddSiteClicked);
    connect(ui->btnDeleteSite, &QPushButton::clicked, this, &SiteManagementWidget::onDeleteSiteClicked);
    connect(ui->btnConnectSite, &QPushButton::clicked, this, &SiteManagementWidget::onConnectSiteClicked);
    connect(ui->btnSaveSite, &QPushButton::clicked, this, &SiteManagementWidget::onSaveSiteClicked);
    loadSites();
}

SiteManagementWidget::~SiteManagementWidget()
{
    delete ui;
}

void SiteManagementWidget::loadSites()
{
    ui->tableSites->setRowCount(0);
    QList<SiteInfo> sites = m_db->getAllSites();
    for (const SiteInfo &s : sites) {
        int row = ui->tableSites->rowCount();
        ui->tableSites->insertRow(row);
        QTableWidgetItem *nameItem = new QTableWidgetItem(s.name);
        nameItem->setData(Qt::UserRole, s.id);
        ui->tableSites->setItem(row, 0, nameItem);
        ui->tableSites->setItem(row, 1, new QTableWidgetItem(s.hostname));
        ui->tableSites->setItem(row, 2, new QTableWidgetItem(s.connectId));
        ui->tableSites->setItem(row, 3, new QTableWidgetItem(tr("未连接")));
    }
}

void SiteManagementWidget::onSiteSelected(int row, int /*col*/)
{
    QTableWidgetItem *item = ui->tableSites->item(row, 0);
    if (!item) return;
    m_selectedSiteId = item->data(Qt::UserRole).toInt();

    QList<SiteInfo> sites = m_db->getAllSites();
    for (const SiteInfo &s : sites) {
        if (s.id == m_selectedSiteId) {
            ui->txtSiteName->setText(s.name);
            ui->txtHostname->setText(s.hostname);
            ui->txtConnectID->setText(s.connectId);
            ui->txtConnectPwd->clear();
            break;
        }
    }
}

void SiteManagementWidget::onAddSiteClicked()
{
    m_selectedSiteId = -1;
    ui->txtSiteName->clear();
    ui->txtHostname->clear();
    ui->txtConnectID->clear();
    ui->txtConnectPwd->clear();
}

void SiteManagementWidget::onDeleteSiteClicked()
{
    if (m_selectedSiteId < 0) {
        QMessageBox::warning(this, tr("提示"), tr("请先选择一个站点"));
        return;
    }
    if (QMessageBox::question(this, tr("确认删除"), tr("确认删除该站点？"),
            QMessageBox::Yes | QMessageBox::No) == QMessageBox::Yes) {
        m_db->deleteSite(m_selectedSiteId);
        loadSites();
        m_selectedSiteId = -1;
    }
}

void SiteManagementWidget::onConnectSiteClicked()
{
    if (m_selectedSiteId < 0) {
        QMessageBox::warning(this, tr("提示"), tr("请先选择一个站点"));
        return;
    }
    QMessageBox::information(this, tr("连接站点"),
        tr("连接到站点功能需要网络支持。\n此功能在后续版本中实现。"));
}

void SiteManagementWidget::onSaveSiteClicked()
{
    QString name = ui->txtSiteName->text().trimmed();
    QString host = ui->txtHostname->text().trimmed();
    if (name.isEmpty() || host.isEmpty()) {
        QMessageBox::warning(this, tr("提示"), tr("请填写站点名称和主机名/IP"));
        return;
    }

    SiteInfo site;
    site.id = m_selectedSiteId;
    site.name = name;
    site.hostname = host;
    site.connectId = ui->txtConnectID->text().trimmed();
    site.connectPwd = ui->txtConnectPwd->text();

    bool ok;
    if (m_selectedSiteId < 0) {
        ok = m_db->addSite(site);
    } else {
        ok = m_db->updateSite(site);
    }

    if (ok) {
        QMessageBox::information(this, tr("成功"), tr("站点已保存"));
        loadSites();
    } else {
        QMessageBox::critical(this, tr("错误"), tr("保存失败：%1").arg(m_db->lastError()));
    }
}
