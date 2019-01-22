DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS childgroups;
CREATE TABLE childgroups (
    id INT NOT NULL AUTO_INCREMENT,
    parentid INT NOT NULL,
    childid INT NOT NULL,
    FOREIGN KEY (parentid) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (childid) REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    UNIQUE (parentid, childid)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS groupvars;
CREATE TABLE groupvars (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    groupid INT NOT NULL,
    FOREIGN KEY (groupid) REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    UNIQUE (name, groupid)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS hosts;
CREATE TABLE hosts (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS hostgroups;
CREATE TABLE hostgroups (
    id INT NOT NULL AUTO_INCREMENT,
    hostid INT NOT NULL,
    groupid INT NOT NULL,
    FOREIGN KEY (hostid) REFERENCES hosts(id) ON DELETE CASCADE,
    FOREIGN KEY (groupid) REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    UNIQUE (hostid)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS hostvars;
CREATE TABLE hostvars (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,
    hostid INT NOT NULL,
    FOREIGN KEY (hostid) REFERENCES hosts(id) ON DELETE CASCADE,
    PRIMARY KEY (id),
    UNIQUE (name, hostid)
) ENGINE=InnoDB;
