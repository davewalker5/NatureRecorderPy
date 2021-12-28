CREATE TABLE JobStatuses (
	id          INTEGER     NOT NULL,
	name        TEXT        NOT NULL,
	parameters  TEXT        NULL,
	start       TEXT        NOT NULL,
	end         TEXT        NULL,
	error       TEXT        NULL,
	PRIMARY KEY (id)
);
