
CREATE TABLE finance.loans (
  id int4 NOT NULL,
  committee_name varchar NOT NULL,
  amount money NOT NULL,
  loan_source_entity varchar NOT NULL,
  incurred_at timestamptz NULL,
  due_at timestamptz NULL,
  interest_rate numeric NOT NULL,
  secured bool DEFAULT true NOT NULL,
  personal_funds bool DEFAULT true NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL,
  CONSTRAINT loans_pk PRIMARY KEY (id)
);

-- Table Triggers

CREATE TRIGGER trigger_fl_updated_at BEFORE
UPDATE
    ON
    finance.loans FOR EACH ROW EXECUTE FUNCTION meta.update_updated_at_column();

CREATE TABLE finance.donations (
    id serial4 NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    transaction_id varchar NOT NULL,
    address_1 varchar NOT NULL,
    address_2 varchar NULL,
    donation_fee_platform money NULL,
    donation_amount money NOT NULL,
    donation_net money NOT NULL,
    donation_at timestamptz NOT NULL,
    address_city varchar NOT NULL,
    address_state varchar NOT NULL,
    address_zip varchar NOT NULL,
    address_country varchar NOT NULL,
    email varchar NULL,
    phone varchar NULL,
    middle_name varchar NULL,
    occupation varchar NOT NULL,
    employer varchar NOT NULL,
    name_title varchar NULL,
    name_suffix varchar NULL,
    page_id varchar NULL,
    "event" varchar NOT NULL,
    created_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz DEFAULT now() NOT NULL,
    loan_id int4 NULL,
    CONSTRAINT donations_pk PRIMARY KEY (id),
    CONSTRAINT donations_loans_fk FOREIGN KEY (loan_id) REFERENCES finance.loans(id)
  );

-- Table Triggers

CREATE TRIGGER trigger_fd_updated_at BEFORE
UPDATE
    ON
    finance.donations FOR EACH ROW EXECUTE FUNCTION meta.update_updated_at_column();



CREATE VIEW public.donations AS
    SELECT
        first_name,
        last_name,
        transaction_id,
        address_1,
        address_2,
        donation_fee_platform,
        donation_amount,
        donation_net,
        donation_at,
        address_city,
        address_state,
        address_zip,
        address_country,
        middle_name,
        occupation,
        employer,
        name_title,
        name_suffix,
        page_id,
        event,
        created_at,
        updated_at,
        loan_id
    FROM finance.donations;


CREATE OR REPLACE VIEW public.donation_metrics AS
    SELECT SUM(donation_amount) AS total_donated
    SELECT count(id) AS donation_count
    SELECT sum(donation_amount) where first_name = "Bentley" and last_name = "Hensel" AS candidate_loan_amount
    FROM finance.donations;


