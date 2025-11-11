# Deployment Notes

## Puzzle Generation on Digital Ocean

### Issue
When deploying to Digital Ocean, the "Generate New Puzzle" button may fail with an error:
```
✗ Error: Unexpected token '<', " <"... is not valid JSON
```

### Cause
This error occurs when the Flask server returns an HTML error page instead of JSON. Common causes:

1. **File Permissions**: The web server may not have write permissions to the `custom_sudoku_generator/sudoku_*_rule/` folders
2. **Path Issues**: The relative paths may be different in the production environment
3. **Module Import Errors**: The Python generator module may not be properly accessible

### Solution
The updated code now includes:

1. **Permission Checks**: Tests write access before attempting generation
2. **Better Error Handling**: Returns proper JSON errors instead of HTML error pages
3. **Detailed Error Messages**: Provides specific information about what went wrong

### Setting File Permissions on Digital Ocean

If you get a "No write permission" error, SSH into your Digital Ocean droplet and run:

```bash
# Navigate to your app directory
cd /path/to/advent_calendar

# Give write permissions to the sudoku rule folders
chmod -R 755 custom_sudoku_generator/
chown -R www-data:www-data custom_sudoku_generator/

# Or if using a different web server user (e.g., for gunicorn):
chown -R $USER:$USER custom_sudoku_generator/
```

### Alternative: Read-Only Deployment

If you prefer not to allow file writes in production, you can:

1. Pre-generate multiple puzzles locally
2. Store them in a database
3. Modify the generate endpoint to cycle through pre-generated puzzles instead of creating new ones

### Testing Generation Locally

Test the generation endpoint locally:

```bash
# In one terminal, start the server
cd website
python app.py

# In another terminal, test the endpoint
curl http://localhost:5000/generate/1
```

You should get a JSON response like:
```json
{"success": true, "message": "New puzzle generated successfully!"}
```

Or an error like:
```json
{"success": false, "message": "No write permission in rule folder. Please check file permissions on the server."}
```

