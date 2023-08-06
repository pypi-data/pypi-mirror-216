# This API token should be valid for the current $PYPI_REPO and should include the "pypi-" prefix
$PYPI_API_TOKEN = "pypi-AgEIcHlwaS5vcmcCJDkyMTViZjQwLTliZDQtNGY4Mi04ODcxLWQwNzhkNzk5MjE0ZAACKlszLCJmMGM0OWE3Mi0wZWE1LTQ4MDQtYjgzNS1mM2ZhNjlhYmQzYTMiXQAABiAPpB2rrPWV1ryHHIuvSAZe9mwqkkBBvIJXIMj17s9m6w"
# Change to "testpypi" to upload to https://test.pypi.org/
# If you do this, know that PyPI and TestPyPI require different API tokens
$PYPI_REPO="pypi"

function publish_cli
{
    # Push-Location
    # Set-Location $STUBS_DIR
    & conda activate qc38
    & python setup.py --quiet sdist bdist_wheel
    [System.Environment]::SetEnvironmentVariable('TWINE_USERNAME',"__token__")
    [System.Environment]::SetEnvironmentVariable('TWINE_PASSWORD',$PYPI_API_TOKEN)
    [System.Environment]::SetEnvironmentVariable('TWINE_REPOSITORY',$PYPI_REPO)
    & twine upload "dist/*"
    # Pop-Location
}

publish_cli