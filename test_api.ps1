# Create a test function
function Test-BookAPI {
    Write-Host "`nTesting GET with empty database..."
    Invoke-RestMethod -Method Get -Uri "http://localhost:8000/books/" -ErrorAction SilentlyContinue

    Write-Host "`nTesting POST with invalid data..."
    $invalidBook = @{
        title = "Test Book"
    } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "http://localhost:8000/books/" -Body $invalidBook -ContentType "application/json" -ErrorAction SilentlyContinue

    Write-Host "`nTesting GET with non-existent ID..."
    Invoke-RestMethod -Method Get -Uri "http://localhost:8000/books/999999" -ErrorAction SilentlyContinue

    Write-Host "`nTesting PUT with invalid data..."
    $invalidUpdate = @{
        published_year = "not a number"
    } | ConvertTo-Json
    Invoke-RestMethod -Method Put -Uri "http://localhost:8000/books/1" -Body $invalidUpdate -ContentType "application/json" -ErrorAction SilentlyContinue

    Write-Host "`nTesting DELETE with non-existent ID..."
    Invoke-RestMethod -Method Delete -Uri "http://localhost:8000/books/999999" -ErrorAction SilentlyContinue
}

# Run the tests
Test-BookAPI 