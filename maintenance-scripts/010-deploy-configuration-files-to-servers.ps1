# $CONNECTION_URI_INTEG = "$Env:SERVER_ADMIN_INTEG@$Env:SERVER_HOSTNAME_INTEG";
# $CONNECTION_URI_PROD = "$Env:SERVER_ADMIN_INTEG@$Env:SERVER_HOSTNAME_INTEG";
$APP_NAME = "email-scoring"

Write-Host "* Copying configuration files to server INTEG docker compose directory.";
Write-Output "APP_ENV=integ" | Out-File .\Docker\EMAIL_SCORING_APP\.env -Encoding utf8; 
Get-Content .\Docker\EMAIL_SCORING_APP\.env.app.version | Add-Content .\Docker\EMAIL_SCORING_APP\.env;
scp -v -i $HOME/.ssh/contabo_key -rp "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\EMAIL_SCORING_APP" ${Env:SERVER_ADMIN_INTEG}@${Env:SERVER_HOSTNAME_INTEG}:${Env:EXTERNAL_ENV}/$APP_NAME/

Write-Host "* Copying database environment config on INTEG server";
scp -v -i $HOME/.ssh/contabo_key -rp "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\DATABASES\\EMAIL_SCORING_DB" ${Env:SERVER_ADMIN_INTEG}@${Env:SERVER_HOSTNAME_INTEG}:${Env:EXTERNAL_ENV}/$APP_NAME/


Write-Host "* Copying .env.keys file to server PROD docker compose directory.";
Write-Output "APP_ENV=prod" | Out-File .\Docker\EMAIL_SCORING_APP\.env -Encoding utf8; 
Get-Content .\Docker\EMAIL_SCORING_APP\.env.app.version | Add-Content .\Docker\EMAIL_SCORING_APP\.env;
scp -v -i $HOME/.ssh/contabo_key -rp "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\EMAIL_SCORING_APP" ${Env:SERVER_ADMIN_PROD}@${Env:SERVER_HOSTNAME_PROD}:${Env:EXTERNAL_ENV}/$APP_NAME/

Write-Host "* Copying database environment config on PROD server";
scp -v -i $HOME/.ssh/contabo_key -rp "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\DATABASES\\EMAIL_SCORING_DB" ${Env:SERVER_ADMIN_PROD}@${Env:SERVER_HOSTNAME_PROD}:${Env:EXTERNAL_ENV}/$APP_NAME/


Write-Output "APP_ENV=dev" | Out-File .\Docker\EMAIL_SCORING_APP\.env -Encoding utf8;
Get-Content .\Docker\EMAIL_SCORING_APP\.env.app.version | Add-Content .\Docker\EMAIL_SCORING_APP\.env;

Start-Sleep -Seconds 1.5;
ssh -i $HOME/.ssh/contabo_key ${Env:SERVER_ADMIN_INTEG}@${Env:SERVER_HOSTNAME_INTEG} chmod +x ${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_DB/start-container.sh ${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_DB/stop-container.sh;
ssh -i $HOME/.ssh/contabo_key ${Env:SERVER_ADMIN_PROD}@${Env:SERVER_HOSTNAME_PROD} chmod +x ${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_DB/start-container.sh ${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_DB/stop-container.sh;