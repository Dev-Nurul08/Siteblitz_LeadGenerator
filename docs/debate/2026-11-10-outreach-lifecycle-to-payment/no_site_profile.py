"""Read-only: contact channels of businesses with NO website listed at all (the website-sale target).
Counts only; writes no_site_profile.csv next to this file."""
import duckdb, pathlib
OUT = pathlib.Path(__file__).parent
con = duckdb.connect()
con.execute("SET temp_directory = 'E:/SiteBlitz-World-Business-Data/_work/duckdb_spill'")
con.execute(f"""
COPY (
SELECT country, count(*) AS no_site,
  count(*) FILTER (WHERE coalesce(len(emails),0) > 0) AS with_email,
  count(*) FILTER (WHERE coalesce(len(emails),0) = 0 AND coalesce(len(phones),0) > 0) AS phone_no_email,
  count(*) FILTER (WHERE coalesce(len(emails),0) = 0 AND coalesce(len(phones),0) = 0 AND coalesce(len(socials),0) > 0) AS social_only,
  count(*) FILTER (WHERE coalesce(len(emails),0) = 0 AND coalesce(len(phones),0) = 0 AND coalesce(len(socials),0) = 0) AS nothing,
  count(*) FILTER (WHERE coalesce(len(phones),0) > 0 AND confidence >= 0.77) AS phone_conf_077
FROM read_parquet('E:/SiteBlitz-World-Business-Data/_work/by_country/*/*.parquet', hive_partitioning = true)
WHERE coalesce(operating_status,'') <> 'permanently_closed' AND coalesce(len(websites),0) = 0
GROUP BY country ORDER BY no_site DESC
) TO '{(OUT/'no_site_profile.csv').as_posix()}' (HEADER)
""")
print("done")
