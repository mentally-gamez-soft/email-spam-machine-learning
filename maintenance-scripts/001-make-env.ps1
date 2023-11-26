Write-Host "================= Make File =========================";
Write-Host "+++++++++++++ CREATION OF .ENV FILES ++++++++++++++++";

Write-Host "* Currently in directory:";
Get-Location;

$from_maintenance_dir=0;

if ($pwd.path.Contains('maintenance')) {
    $from_maintenance_dir=1;
    cd ..;
    Write-Host "* Changed to application home directory:";
    Get-Location;
}
else {
    Write-Host "* No need to change dir we are already in the right place.";
}

Write-Host "* Deleting the file .env.vault ...";
Remove-Item -Path .\.env.vault;

cd .\core\app_configuration;
Write-Host "* Changed to configuration directory:";
Get-Location;

Write-Host "* Creating and encrypting .env.vault and .env.keys files.";
npx dotenv-vault local build

Write-Host "* Delete .gitignore file";
Remove-Item -Path .\.gitignore;

Write-Host "* Moving .env.vault file to root project directory.";
Get-Item -Path .\.env.vault | Move-Item -Destination ..\..\.env.vault;

Write-Host "* Copying .env.keys file to local project directory.";
Get-Item -Path .\.env.keys | Copy-Item -Destination ..\..\Docker\EMAIL_SCORING_APP\.env.keys;

Write-Host "* Copying .env.keys file for local dev.";
Get-Item -Path .\.env.keys | Copy-Item -Destination ..\..\.env.keys;

# Write-Host "* Copying .env.keys file to external env project directory.";
# Get-Item -Path .\.env.keys | Copy-Item -Destination $Env:EXTERNAL_ENV\email-scoring\.env.keys;

Write-Host "* Copying configuration file to server INTEG.";
scp -v -i $HOME/.ssh/contabo_key "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\EMAIL_SCORING_APP\\.env.keys" ${Env:SERVER_ADMIN_INTEG}@${Env:SERVER_HOSTNAME_INTEG}:${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_APP/.env.keys;

Write-Host "* Copying .env.keys file to server PROD.";
scp -v -i $HOME/.ssh/contabo_key "D:\\projects\\courses\\Python\\email spam machine learning\\Docker\\EMAIL_SCORING_APP\\.env.keys" ${Env:SERVER_ADMIN_PROD}@${Env:SERVER_HOSTNAME_PROD}:${Env:EXTERNAL_ENV}/email-scoring/EMAIL_SCORING_APP/.env.keys;


cd ..\..;
Get-Location;
Write-Host "++++++++++++++++ End of .env encryption process ++++++++++++++++"