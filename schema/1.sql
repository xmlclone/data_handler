CREATE TABLE excution_record (
        id INTEGER NOT NULL,
        bus_id INTEGER NOT NULL,
        project VARCHAR NOT NULL,
        scene VARCHAR NOT NULL,
        area VARCHAR,
        steps JSON NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        result VARCHAR(11),
        error_message VARCHAR,
        ai_reason_code INTEGER,
        ai_reason VARCHAR,
        act_reason_code INTEGER,
        act_reason VARCHAR,
        day DATE NOT NULL,
        PRIMARY KEY (id)
);