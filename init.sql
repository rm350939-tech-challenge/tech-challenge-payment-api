CREATE SCHEMA IF NOT EXISTS service_payment;

-- Criar sequência para tabela payment_types
CREATE SEQUENCE service_payment.payment_types_id_seq;

-- Criar tabela payment_types
CREATE TABLE service_payment.payment_types (
	id INTEGER NOT NULL DEFAULT nextval('service_payment.payment_types_id_seq'),
	"name" varchar(80) NOT NULL,
	description text NULL,
	created_at timestamp NOT NULL,
	CONSTRAINT payment_types_pkey PRIMARY KEY (id)
);

-- Criar sequência para tabela payments
CREATE SEQUENCE service_payment.payments_id_seq;

-- Criar tabela payments
CREATE TABLE service_payment.payments (
	id INTEGER NOT NULL DEFAULT nextval('service_payment.payments_id_seq'),
	order_id int4 NOT NULL,
	amount numeric NOT NULL,
	created_at timestamp NOT NULL,
	type_id int4 NOT NULL,
	status int2 NOT NULL,
	CONSTRAINT payments_pkey PRIMARY KEY (id),
	CONSTRAINT payments_unique UNIQUE (order_id),
    CONSTRAINT payments_payment_types_fk FOREIGN KEY (type_id) REFERENCES service_payment.payment_types(id)
);

INSERT INTO service_payment.payment_types (id, "name", description, created_at)
VALUES(nextval('service_payment.payment_types_id_seq'), 'PIX', 'PIX', NOW());

INSERT INTO service_payment.payment_types (id, "name", description, created_at)
VALUES(nextval('service_payment.payment_types_id_seq'), 'PIX', 'PIX', NOW());
