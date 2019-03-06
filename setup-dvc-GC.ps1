param(
    [string]$key = "starry-battery-103809-d129914e1f44.json" # by default check if key is present in current dir
)

if (-Not (Test-Path -Path $key)) {
    $key = $(Read-Host "Input path to the key file")
    if (-Not (Test-Path -Path $key)) {
        throw "Wrong key path!"
    }
}

$key = [System.IO.Path]::GetFullPath($key)

# [System.Environment]::SetEnvironmentVariable('GOOGLE_APPLICATION_CREDENTIALS', $key, [System.EnvironmentVariableTarget]::User)
setx GOOGLE_APPLICATION_CREDENTIALS $key

# should be done only once - saves in .dvc/config file
# dvc remote add gc gs://spacy-pl
# dvc config core.remote gc

Write-Host 'Done! Open a new command line window for changes to take effect.';
Write-Host -NoNewLine 'Press any key to continue...';
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
