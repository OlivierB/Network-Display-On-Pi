
var serverStat = new ServerStat('server-stat');
serverStat.add('proc', 'proc_load', 100);
serverStat.add('memory', 'mem_load', 100);
serverStat.add('swap', 'swap_load', 100);
serverStat.add('loss', 'pkt_lost', 100);

serverStat.connect(dispatcher, App.serverStatProtocol);