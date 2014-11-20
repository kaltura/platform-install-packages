USE kalturadw;
INSERT INTO dwh_dim_partners 
	(partner_id, admin_email,admin_name,adult_content,anonymous_kuser_id,commercial_use,content_categories,
	created_at,created_date_id,created_hour_id,description,moderate_content,notify,partner_name,partner_package,
	partner_status_id,partner_status_name,partner_type_id,partner_type_name,updated_at,updated_date_id,updated_hour_id ,ri_ind) 
SELECT DISTINCT a.partner_id, "Missing Value","Missing Value","-1","-1","-1", "Missing Value",
	"2099-01-01 00:00:00","-1","-1","Missing Value","-1","-1","Missing Value","-1",
	"-1","Missing Value","-1","Missing Value","2099-01-01 00:00:00","-1","-1" ,1 
	FROM kalturadw.dwh_hourly_errors a LEFT OUTER JOIN kalturadw.dwh_dim_partners b  
	ON a.partner_id = b.partner_id
	WHERE b.partner_id IS NULL AND a.partner_id IS NOT NULL;
