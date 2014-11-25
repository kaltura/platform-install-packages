DROP VIEW IF EXISTS kalturadw.dwh_view_partners_monthly_billing;
CREATE VIEW `kalturadw`.`dwh_view_partners_monthly_billing` 
    AS
(
	SELECT max_blling_updated.month_id, billing.* 
	FROM kalturadw.dwh_view_partners_monthly_billing_last_updated_at max_blling_updated, 
		kalturadw.dwh_dim_partners_billing billing
	WHERE max_blling_updated.partner_id = billing.partner_id
	AND max_blling_updated.updated_at = billing.updated_at
);

