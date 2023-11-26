param([string]$numero_version)
if($numero_version -eq '') {
    Throw "Error - The version number of the image to build is not set !!!"
}
elseif(!($numero_version -match '^(\d{1,2}\.)(\d{1,2}\.)(\d{1,2}[a-z]{0,1})$')) {
    Throw "Error - The version number $numero_version for this image is incorrect !"
}
else {
    Write-Output "A new image of the application email-scoring will be built with version code: $numero_version";
    Write-Output "APP_VERSION=${numero_version}" | Out-File .\Docker\EMAIL_SCORING_APP\.env.app.version -Encoding utf8; 
}

docker build --build-arg version_number=$numero_version -t ${Env:DOCKER_REGISTRY}/${Env:DOCKER_REPOSITORY}:ws-email-scoring-$numero_version .