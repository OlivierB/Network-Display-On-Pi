var base = new BaseAlert('content-table');
base.connect(App.webServerAddress, "/base/perso/base_stat_alerts.php?caller=&sort_order=last_d", 10000);
