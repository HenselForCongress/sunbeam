CREATE OR REPLACE FUNCTION meta.update_updated_at_column()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    -- Set the updated_at column to the current timestamp
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$function$
;
