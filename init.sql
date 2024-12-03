-- Criar sequência para tabela payment_types
CREATE SEQUENCE payment_types_id_seq;

-- Criar tabela payment_types
CREATE TABLE payment_types (
	id INTEGER PRIMARY KEY DEFAULT nextval('payment_types_id_seq'),
	"name" varchar(80) NOT NULL,
	description text NULL,
	created_at timestamp NOT NULL
);

-- Criar sequência para tabela payments
CREATE SEQUENCE payments_id_seq;

-- Criar tabela payments
CREATE TABLE payments (
	id INTEGER PRIMARY KEY DEFAULT nextval('payments_id_seq'),
	order_id int4 NOT NULL,
	amount numeric NOT NULL,
	created_at timestamp NOT NULL,
	type_id int4 NOT NULL,
	status int2 NOT NULL,
	CONSTRAINT payments_unique UNIQUE (order_id),
    CONSTRAINT payments_orders_fk FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT payments_payment_types_fk FOREIGN KEY (type_id) REFERENCES payment_types(id)
);

INSERT INTO payment_types (id, "name", description, created_at)
VALUES(nextval('payment_types_id_seq'), 'PIX', 'PIX', NOW());

INSERT INTO payment_types (id, "name", description, created_at)
VALUES(nextval('payment_types_id_seq'), 'PIX', 'PIX', NOW());
