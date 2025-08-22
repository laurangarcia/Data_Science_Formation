-- Script to alter the persons2 table
ALTER TABLE persons2
ADD COLUMN address VARCHAR(255);

-- Renombrar la columna
ALTER TABLE persons2
RENAME COLUMN address TO location;

-- Actualizacion del tipo de campo
ALTER TABLE persons2
MODIFY COLUMN location VARCHAR(255);

ALTER TABLE persons2
DROP COLUMN location;