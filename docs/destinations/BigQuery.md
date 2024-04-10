# BigQuery

To use bq, you need to create a gcloud service account with these perms:

BigQuery Data Editor (roles/bigquery.dataEditor): This role includes permissions to create, update, and delete data within BigQuery tables. It's suitable for scenarios where the service account needs to manage table data, but it doesn't grant permissions to manage the tables or datasets themselves (e.g., creating or deleting tables).
BigQuery User (roles/bigquery.user): This role grants permissions to run jobs, including query jobs, within the project. It can be combined with data-specific roles (like BigQuery Data Editor) to provide broader access that includes both managing data and executing queries.
