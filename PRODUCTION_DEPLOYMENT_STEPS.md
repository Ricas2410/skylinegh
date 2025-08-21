# 🚀 Production Deployment Steps - Statistics Fix

## The Problem
The statistics on your live site (skylineghana.com) are showing as 0 because the recent changes are only in the development environment. We need to deploy these changes to production.

## 🔧 Quick Fix (Recommended)

### Option 1: Automated Script
1. Upload the `deploy_statistics_fix.py` file to your production server
2. SSH into your production server
3. Navigate to your project directory
4. Run: `python deploy_statistics_fix.py`

### Option 2: Manual Steps

#### Step 1: SSH into your production server
```bash
ssh your-username@your-server-ip
cd /path/to/your/skylinegh/project
```

#### Step 2: Pull latest changes
```bash
git pull origin main
```

#### Step 3: Run database migration
```bash
python manage.py migrate
```

#### Step 4: Update site settings via Django shell
```bash
python manage.py shell
```

Then in the Django shell, run:
```python
from core.models import SiteSettings

# Get or create site settings
site_settings, created = SiteSettings.objects.get_or_create(pk=1)

# Update statistics
site_settings.projects_completed = 500
site_settings.square_feet_built = 1000000
site_settings.client_satisfaction = 98
site_settings.years_experience = 25

# Save changes
site_settings.save()

# Verify the values
print(f"Projects: {site_settings.projects_completed}")
print(f"Sq Ft: {site_settings.square_feet_built}")
print(f"Satisfaction: {site_settings.client_satisfaction}%")
print(f"Experience: {site_settings.years_experience} years")

# Exit shell
exit()
```

#### Step 5: Clear cache
```bash
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Cache cleared')"
```

#### Step 6: Collect static files
```bash
python manage.py collectstatic --noinput
```

#### Step 7: Restart your web server
```bash
# For Gunicorn + Nginx
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# OR for Apache
sudo service apache2 restart

# OR for other setups
sudo service your-web-server restart
```

## 🔍 Verification Steps

1. **Check the website**: Visit https://skylineghana.com/projects/
2. **Look for the statistics section**: Should show the numbers instead of 0s
3. **Test the admin**: Go to `/my-admin/settings/` and check the Statistics tab
4. **Clear browser cache**: If you still see 0s, clear your browser cache

## 📊 Expected Results

After deployment, the "Our Impact" section should show:
- **Projects Completed**: 500 (instead of 0)
- **Sq Ft Built**: 1,000,000 (instead of 0)
- **% Client Satisfaction**: 98 (instead of 0)
- **Years Experience**: 25 (instead of 0)

## 🎯 Customizing the Statistics

Once deployed, you can customize these numbers:

1. Go to: `https://skylineghana.com/my-admin/settings/`
2. Click the **"Statistics"** tab
3. Update the values:
   - Projects Completed: Enter your actual number
   - Square Feet Built: Enter total sq ft
   - Client Satisfaction: Enter percentage (0-100)
   - Years Experience: Enter years in business
4. Click **"Save Settings"**
5. The changes will appear immediately on the website

## 🚨 Troubleshooting

### If statistics still show as 0:

1. **Check database migration**:
   ```bash
   python manage.py showmigrations core
   ```
   Look for: `[X] 0012_sitesettings_client_satisfaction_and_more`

2. **Verify database fields**:
   ```bash
   python manage.py shell -c "from core.models import SiteSettings; s=SiteSettings.objects.first(); print(f'Stats: {s.projects_completed}, {s.square_feet_built}, {s.client_satisfaction}, {s.years_experience}' if s else 'No settings found')"
   ```

3. **Check template cache**:
   - Clear browser cache completely
   - Try incognito/private browsing mode
   - Check if template caching is enabled

4. **Restart everything**:
   ```bash
   sudo systemctl restart gunicorn nginx
   # OR
   sudo service apache2 restart
   ```

### If admin panel doesn't show Statistics tab:

1. **Clear cache**:
   ```bash
   python manage.py shell -c "from django.core.cache import cache; cache.clear()"
   ```

2. **Restart web server**:
   ```bash
   sudo systemctl restart gunicorn
   ```

## 📞 Support

If you encounter issues:

1. **Check error logs**:
   ```bash
   tail -f /var/log/nginx/error.log
   # OR
   tail -f /var/log/apache2/error.log
   ```

2. **Check Django logs** (if configured)

3. **Test locally first**: Make sure changes work in development

## ✅ Success Checklist

- [ ] Database migration applied
- [ ] Site settings updated with statistics
- [ ] Cache cleared
- [ ] Static files collected
- [ ] Web server restarted
- [ ] Website shows correct statistics
- [ ] Admin panel has Statistics tab
- [ ] Statistics can be edited in admin

## 🎯 Next Steps After Deployment

1. **Update with real numbers**: Replace default values with your actual statistics
2. **Monitor performance**: Check if site loads faster with caching
3. **SEO verification**: Verify meta tags are working properly
4. **Regular updates**: Keep statistics current as you complete more projects

---

**Note**: These changes improve both the visual display of statistics and the overall SEO/performance of your website. The statistics will now be easily manageable through the admin panel.
