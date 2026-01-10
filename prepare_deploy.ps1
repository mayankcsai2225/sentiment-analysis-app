# PowerShell script to prepare for deployment
# This script helps prepare your repository for deployment

Write-Host "🚀 Preparing repository for deployment..." -ForegroundColor Green

# Backup current .gitignore
if (Test-Path .gitignore) {
    Copy-Item .gitignore .gitignore.backup
    Write-Host "✅ Backed up .gitignore" -ForegroundColor Green
}

# Use deployment-friendly .gitignore
if (Test-Path .gitignore.deploy) {
    Copy-Item .gitignore.deploy .gitignore
    Write-Host "✅ Updated .gitignore for deployment" -ForegroundColor Green
} else {
    Write-Host "⚠️  .gitignore.deploy not found, skipping..." -ForegroundColor Yellow
}

# Check if models exist
if (Test-Path "models\model.joblib") {
    Write-Host "✅ Found model.joblib" -ForegroundColor Green
} else {
    Write-Host "⚠️  model.joblib not found in models/ directory" -ForegroundColor Yellow
}

if (Test-Path "models\fasttext_model_cbow.bin") {
    Write-Host "✅ Found fasttext_model_cbow.bin" -ForegroundColor Green
} else {
    Write-Host "⚠️  fasttext_model_cbow.bin not found in models/ directory" -ForegroundColor Yellow
}

Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the changes: git status" -ForegroundColor White
Write-Host "2. Add all files: git add ." -ForegroundColor White
Write-Host "3. Commit: git commit -m 'Ready for deployment'" -ForegroundColor White
Write-Host "4. Push: git push origin main" -ForegroundColor White
Write-Host "5. Deploy on Streamlit Cloud: https://share.streamlit.io" -ForegroundColor White

Write-Host "`n✨ Ready to deploy!" -ForegroundColor Green

