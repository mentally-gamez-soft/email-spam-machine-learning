param ($mode)
if(!$mode){
    $mode = 'undefined';
}

if ($mode.toLower() -like '*test*') {
    write-host "The tests suit execution is set at launch.";
}
elseif ($mode.toLower() -like '*env*') {
    write-host "The mode creation of encrypted env files is set at launch.";
}
elseif ($mode.toLower() -like '*build*') {
    write-host "The mode creation of docker image is set at launch.";
}
elseif ($mode.toLower() -like '*deploy*') {
    write-host "The mode configuration of remote servers is set at launch.";
}

function Execute-deploy-config-remote-server {
    param([String]$Mode)

     if ($Mode -eq 'fixed') {
        $message = "The configuration of the remote servers is deploying ...";
        Write-Output $message;
        & ".\maintenance-scripts\010-deploy-configuration-files-to-servers.ps1";
     }
     else {
        $yes = New-Object System.Management.Automation.Host.ChoiceDescription '&Yes', 'Deploy config files onto remote servers.'
        $no = New-Object System.Management.Automation.Host.ChoiceDescription '&No', 'Do not deploy config files onto remote servers.'
        $options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)
        $result = $host.ui.PromptForChoice('Deploy the configuration files onto remote servers?', 'Do you want to deploy config files onto remote servers?', $options, 0)
    
        switch ($result)
            {
                0 {
                    $message = "The configuration of the remote servers is deploying ...";
                    Write-Output $message;
                    & ".\maintenance-scripts\010-deploy-configuration-files-to-servers.ps1";
                }
                1 {
                    $message = "The configuration for the remote servers will not be deployed.";
                    Write-Output $message;
                }
            }
     }
 }

function Execute-test-suite {
    param([String]$Mode)

     if ($Mode -eq 'fixed') {
        $message = "The tests suit is executing ...";
        Write-Output $message;
        & ".\maintenance-scripts\003-launch-tests-suite.ps1";
     }
     else {
        $yes = New-Object System.Management.Automation.Host.ChoiceDescription '&Yes', 'Launch the tests suit.'
        $no = New-Object System.Management.Automation.Host.ChoiceDescription '&No', 'Do not execute the tests suit.'
        $options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)
        $result = $host.ui.PromptForChoice('Execute the tests suit?', 'Do you want to execute the tests suit?', $options, 0)
    
        switch ($result)
            {
                0 {
                    $message = "The tests suit is executing ...";
                    Write-Output $message;
                    & ".\maintenance-scripts\003-launch-tests-suite.ps1";
                }
                1 {
                    $message = "The tests suit will not launch.";
                    Write-Output $message;
                }
            }
     }
 }

function Encrypt-env {
    param([String]$Mode)

     if ($Mode -eq 'fixed') {
        $message = "The encryption of the .env file is processing ...";
        Write-Output $message;
        & ".\maintenance-scripts\001-make-env.ps1";
     }
     else {
        $yes = New-Object System.Management.Automation.Host.ChoiceDescription '&Yes', 'Launch the encryption of .env files'
        $no = New-Object System.Management.Automation.Host.ChoiceDescription '&No', 'Do not execute the .env encryption'
        $options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)
        $result = $host.ui.PromptForChoice('Encrypt the .env files?', 'Do you want to encrypt the .env files?', $options, 0)
    
        switch ($result)
            {
                0 {
                    $message = "The encryption of the .env file is processing ...";
                    Write-Output $message;
                    & ".\maintenance-scripts\001-make-env.ps1";
                }
                1 {
                    $message = "The encryption of the .env file will not launch.";
                    Write-Output $message;
                }
            }
     }
 }

function Build-app-image {
     param([String]$Mode)

     if ($Mode -eq 'fixed') {
        $version_number = Read-Host -Prompt 'Please indicate the new code version for the app';
        $message = "The following new image for email-scoring app will be built => email-scoring-$version_number";
        Write-Output $message;
        & ".\maintenance-scripts\004-build-docker-image.ps1" $version_number;
     }
     else {
        $yes = New-Object System.Management.Automation.Host.ChoiceDescription '&Yes', 'Create a new image version of email-scoring app.'
        $no = New-Object System.Management.Automation.Host.ChoiceDescription '&No', 'Do not create a new image of email-scoring app.'
        $options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)
        $result = $host.ui.PromptForChoice('Create a new image of the application ?', 'Would you like to create a new version of the app ?', $options, 0)
    
        switch ($result)
            {
                0 {
                    $version_number = Read-Host -Prompt 'Please indicate the new code version for the app';
                    $message = "The following new image for email-scoring app will be built => email-scoring-$version_number";
                    Write-Output $message;
                    & ".\maintenance-scripts\004-build-docker-image.ps1" $version_number;
                }
                1 {
                    $message = "No new image version of email-scoring will be built.";
                    Write-Output $message;
                }
            } 
     }

 }

if ($mode.toLower() -like '*test*') {
    Execute-test-suite "fixed";
}
elseif ($mode.toLower() -like '*env*') {
    Encrypt-env "fixed";
}
elseif ($mode.toLower() -like '*build*') {
    Build-app-image "fixed";
}
elseif ($mode.toLower() -like '*deploy*') {
    Execute-deploy-config-remote-server "fixed";
}
else {
    Encrypt-env;
    Execute-test-suite;
    Build-app-image;
    Execute-deploy-config-remote-server;
}