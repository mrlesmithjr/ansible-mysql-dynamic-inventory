INSERT IGNORE INTO groups(name) VALUES ('atlanta');
INSERT IGNORE INTO groups(name) VALUES ('db_servers');
INSERT IGNORE INTO groups(name) VALUES ('web_servers');
INSERT IGNORE INTO childgroups(parentid, childid) VALUES ((SELECT id FROM groups WHERE name='atlanta'), (SELECT id FROM groups WHERE name='db_servers'));
INSERT IGNORE INTO childgroups(parentid, childid) VALUES ((SELECT id FROM groups WHERE name='atlanta'), (SELECT id FROM groups WHERE name='web_servers'));
INSERT IGNORE INTO hosts(name) VALUES ('node0');
INSERT IGNORE INTO hosts(name) VALUES ('node1');
INSERT IGNORE INTO hostgroups(hostid, groupid) VALUES ((SELECT id FROM hosts WHERE name='node0'), (SELECT id FROM groups WHERE name='web_servers'));
INSERT IGNORE INTO hostgroups(hostid, groupid) VALUES ((SELECT id FROM hosts WHERE name='node1'), (SELECT id FROM groups WHERE name='db_servers'));
REPLACE INTO groupvars(name, value, groupid) VALUES ('db_port','3306', (SELECT id FROM groups WHERE name='db_servers'));
REPLACE INTO groupvars(name, value, groupid) VALUES ('web_port','8080', (SELECT id FROM groups WHERE name='web_servers'));
REPLACE INTO groupvars(name, value, groupid) VALUES ('web_protocol','http', (SELECT id FROM groups WHERE name='web_servers'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_host','192.168.250.10', (SELECT id FROM hosts WHERE name='node0'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_user','vagrant', (SELECT id FROM hosts WHERE name='node0'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_password','vagrant', (SELECT id FROM hosts WHERE name='node0'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_host','192.168.250.11', (SELECT id FROM hosts WHERE name='node1'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_user','vagrant', (SELECT id FROM hosts WHERE name='node1'));
REPLACE INTO hostvars(name, value, hostid) VALUES ('ansible_password','vagrant', (SELECT id FROM hosts WHERE name='node1'));

SELECT * FROM groups;
SELECT * FROM groupvars;
SELECT * FROM childgroups;
SELECT * FROM hostgroups;
SELECT * FROM hosts;
SELECT * FROM hostvars;
SELECT name FROM groups WHERE id IN (SELECT parentid FROM childgroups);

DROP TABLE IF EXISTS hostvars;
DROP TABLE IF EXISTS hostgroups;
DROP TABLE IF EXISTS groupvars;
DROP TABLE IF EXISTS childgroups;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS hosts;

