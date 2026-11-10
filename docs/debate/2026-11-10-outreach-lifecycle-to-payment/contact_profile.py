"""Read-only profile of the world business data: which contact channel each business can be reached on,
and how trustworthy the emails look. Writes contact_profile.csv + email_quality.csv next to this file.
No names, emails or phone numbers are written out - only counts."""
import sys, duckdb, pathlib
SRC = "E:/SiteBlitz-World-Business-Data/_work/by_country/*/*.parquet"
OUT = pathlib.Path(__file__).parent
con = duckdb.connect()
con.execute("SET temp_directory = 'E:/SiteBlitz-World-Business-Data/_work/duckdb_spill'")
con.execute(f"""
CREATE TEMP VIEW p AS
SELECT country,
       coalesce(len(emails),0)  > 0 AS has_email,
       coalesce(len(phones),0)  > 0 AS has_phone,
       coalesce(len(socials),0) > 0 AS has_social,
       coalesce(len(websites),0) > 0 AS has_any_site,
       emails, websites
FROM read_parquet('{SRC}', hive_partitioning = true)
WHERE coalesce(operating_status,'') <> 'permanently_closed'
""")
# 1. reachability buckets per country
con.execute(f"""
COPY (
SELECT country,
  count(*) AS businesses,
  count(*) FILTER (WHERE has_email AND has_phone)            AS email_and_phone,
  count(*) FILTER (WHERE has_email AND NOT has_phone)        AS email_only,
  count(*) FILTER (WHERE NOT has_email AND has_phone)        AS phone_only,
  count(*) FILTER (WHERE NOT has_email AND NOT has_phone AND has_social)  AS social_only_no_contact,
  count(*) FILTER (WHERE NOT has_email AND NOT has_phone AND NOT has_social AND has_any_site) AS site_only,
  count(*) FILTER (WHERE NOT has_email AND NOT has_phone AND NOT has_social AND NOT has_any_site) AS nothing
FROM p GROUP BY country ORDER BY businesses DESC
) TO '{(OUT/'contact_profile.csv').as_posix()}' (HEADER)
""")
# 2. email quality signals (first email of each business)
con.execute(f"""
CREATE TEMP TABLE e AS
SELECT country, lower(trim(emails[1])) AS em,
       lower(regexp_extract(coalesce(websites[1],''), '^(?:https?://)?(?:www\.)?([^/:?#]+)', 1)) AS site_dom
FROM p WHERE has_email
""")
con.execute("""
CREATE TEMP TABLE e2 AS
SELECT *, split_part(em,'@',2) AS dom, split_part(em,'@',1) AS local_part,
       count(*) OVER (PARTITION BY em) AS used_by
FROM e
""")
con.execute(f"""
COPY (
SELECT country, count(*) AS with_email,
  count(*) FILTER (WHERE NOT regexp_matches(em, '^[a-z0-9._%+''-]+@[a-z0-9.-]+\.[a-z]{{2,}}$')) AS bad_syntax,
  count(*) FILTER (WHERE dom IN ('gmail.com','yahoo.com','hotmail.com','outlook.com','live.com','yahoo.co.in',
        'rediffmail.com','icloud.com','aol.com','gmx.de','web.de','mail.ru','yandex.ru','hotmail.co.uk','yahoo.co.uk',
        'libero.it','orange.fr','free.fr','wanadoo.fr','qq.com','163.com','naver.com','bol.com.br','uol.com.br','terra.com.br','yahoo.com.br','hotmail.fr','hotmail.it','t-online.de','proton.me','protonmail.com','ymail.com','msn.com')) AS free_mail,
  count(*) FILTER (WHERE site_dom <> '' AND (dom = site_dom OR site_dom LIKE '%.' || dom OR dom LIKE '%.' || site_dom)) AS matches_own_site,
  count(*) FILTER (WHERE local_part IN ('info','contact','hello','office','admin','sales','enquiry','enquiries','mail','support','booking','reservations','kontakt','contacto','contato','bonjour')) AS role_address,
  count(*) FILTER (WHERE used_by >= 5) AS shared_by_5plus_places,
  count(*) FILTER (WHERE used_by >= 50) AS shared_by_50plus_places
FROM e2 GROUP BY country ORDER BY with_email DESC
) TO '{(OUT/'email_quality.csv').as_posix()}' (HEADER)
""")
print("done")
