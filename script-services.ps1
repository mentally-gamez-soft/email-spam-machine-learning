param ($mode)
if (!$mode){
    throw 'The execution mode must be set: [startdb|stopdb|startmb|stopmb|startapp|stopapp]';
}

function Start-database {
    $message = "The database service is starting ...";
    Write-Output $message;
    & ".\maintenance-scripts\002.a.1-launch-server-database.ps1";
 }

 function Stop-database {
    $message = "The database service is stopping ...";
    Write-Output $message;
    & ".\maintenance-scripts\002.b.1-stop-server-database.ps1";
 }

 function Start-metabase {
    $message = "The metabase service is starting ...";
    Write-Output $message;
    & ".\maintenance-scripts\002.a.2-launch-server-metabase.ps1";
 }
 function Stop-metabase {
    $message = "The metabase service is stopping ...";
    Write-Output $message;
    & ".\maintenance-scripts\002.b.2-stop-server-metabase.ps1";
 }

 function Start-app {
    $message = "The ws-email-scoring app service is starting ...";
    Write-Output $message;
    & ".\maintenance-scripts\005.a-start-service-app.ps1";
 }
 function Stop-app {
    $message = "The ws-email-scoring app service is stopping ...";
    Write-Output $message;
    & ".\maintenance-scripts\005.b-stop-service-app.ps1";
 }

if ($mode.toLower() -like '*startdb*') {
    Start-database;
}
elseif ($mode.toLower() -like '*stopdb*') {
    Stop-database;
}
elseif ($mode.toLower() -like '*stopdb*') {
    Stop-database;
}
elseif ($mode.toLower() -like '*startmb*') {
    Start-metabase;
}
elseif ($mode.toLower() -like '*stopmb*') {
    Stop-metabase;
}
elseif ($mode.toLower() -like '*startapp*') {
    Start-app;
}
elseif ($mode.toLower() -like '*stopapp*') {
    Stop-app;
}