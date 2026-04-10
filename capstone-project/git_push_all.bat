@echo off
echo ================================================================
echo  BBO Capstone -- Git Add, Commit and Push
echo  Run from: capstone-project\capstone-project\
echo ================================================================
echo.

:: Step 1 -- delete the accidental REN file in week-11
echo [1/5] Deleting accidental REN file...
if exist week-11\REN (
    del week-11\REN
    echo       Deleted: week-11\REN
) else (
    echo       Not found -- skipping
)
echo.

:: Step 2 -- stage everything (untracked + modified + deleted)
echo [2/5] Staging all changes (git add -A)...
git add -A
echo       Done.
echo.

:: Step 3 -- show summary of what is staged
echo [3/5] Status summary:
git status --short
echo.

:: Step 4 -- commit
echo [4/5] Committing...
git commit -m "Add W1-W12 all notebooks, data, cards, strategy docs and W12 final submissions"
echo.

:: Step 5 -- push
echo [5/5] Pushing to GitHub...
git push origin main
echo.

echo ================================================================
echo  Done. Check above for any errors.
echo  Then verify at: https://github.com/kennelm2025/Mikes-Capstone
echo ================================================================
pause
