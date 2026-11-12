# Email engine v2, phase E4 - registers the two Windows Task Scheduler jobs that read the sending mailboxes
# (spec row 14: at least every 24 hours, also on non-sending days; before and during every sending session).
#
# Written for the founder to run ONCE, by hand, in the project folder (nothing runs it automatically):
#     powershell -ExecutionPolicy Bypass -File scripts\register_outreach_tasks.ps1
# Remove them again with:
#     Unregister-ScheduledTask -TaskName "SiteBlitz outreach reconcile daily" -Confirm:$false
#     Unregister-ScheduledTask -TaskName "SiteBlitz outreach reconcile windows" -Confirm:$false
#
# Times are the laptop's local time, so the Windows clock must be on India Standard Time (UTC+05:30).
# Both tasks run scripts\outreach_reconcile.py with the project's .venv Python, as the logged-in user, and only while
# that user is logged in (the .env file and the database are on this laptop). "Run as soon as possible after a
# scheduled start is missed" is on, so a laptop that was asleep at 08:30 reads the inboxes when it wakes up.
# Exit code (Task Scheduler "Last Run Result"): 0 = all mailboxes read, 1 = a mailbox failed (it stays paused),
# 2 = refused (another run is busy / no mailbox).

param(
    [string]$ProjectDir = (Split-Path -Parent $PSScriptRoot)
)

$python = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$script = Join-Path $ProjectDir "scripts\outreach_reconcile.py"
if (-not (Test-Path $python)) { Write-Error "Python not found at $python (create the .venv first)"; exit 2 }
if (-not (Test-Path $script)) { Write-Error "Script not found at $script"; exit 2 }

$action = New-ScheduledTaskAction -Execute $python -Argument "`"$script`"" -WorkingDirectory $ProjectDir
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 20) -MultipleInstances IgnoreNew

# 1. Every day at 08:30, weekends and non-sending days included (the 24-hour rule).
$daily = New-ScheduledTaskTrigger -Daily -At "08:30"
Register-ScheduledTask -TaskName "SiteBlitz outreach reconcile daily" -Action $action -Trigger $daily `
    -Settings $settings -Force `
    -Description "SiteBlitz email engine v2: read the sending mailboxes (stops, out-of-office, bounces, replies) once a day."

# 2. Tuesday-Thursday (the campaign days): 08:55, then every 30 minutes until 16:30 (end of the second window).
$window = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Tuesday, Wednesday, Thursday -At "08:55"
$repeat = New-ScheduledTaskTrigger -Once -At "08:55" -RepetitionInterval (New-TimeSpan -Minutes 30) `
    -RepetitionDuration (New-TimeSpan -Hours 7 -Minutes 35)
$window.Repetition = $repeat.Repetition
Register-ScheduledTask -TaskName "SiteBlitz outreach reconcile windows" -Action $action -Trigger $window `
    -Settings $settings -Force `
    -Description "SiteBlitz email engine v2: read the sending mailboxes before and during the Tue-Thu sending windows."

Write-Output "Registered: 'SiteBlitz outreach reconcile daily' (08:30 every day) and 'SiteBlitz outreach reconcile windows' (Tue-Thu 08:55-16:30, every 30 min)."
